'''
This state module is intended soely for controlling concurrency of the state
execution. It maintains no other state
'''

import logging
import time

try:
    from kazoo.client import KazooClient

    from kazoo.retry import (
        KazooRetry,
        RetryFailedError,
        ForceRetryError
    )
    import kazoo.recipe.lock
    from kazoo.exceptions import CancelledError
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False

ZK_CONNECTION = None
SEMAPHORE_MAP = {}

__virtualname__ = 'zk_concurrency'


def __virtual__():
    if not HAS_DEPS:
        return False

    return __virtualname__


def _get_zk_conn(hosts):
    global ZK_CONNECTION
    if ZK_CONNECTION is None:
        ZK_CONNECTION = KazooClient(hosts=hosts)
        ZK_CONNECTION.start()

    return ZK_CONNECTION


def _close_zk_conn():
    global ZK_CONNECTION
    if ZK_CONNECTION is None:
        return

    ZK_CONNECTION.stop()
    ZK_CONNECTION = None


def lock(zk_hosts,
         path,
         max_concurrency,
         timeout=None,
         ephemeral_lease=False):
    global SEMAPHORE_MAP
    '''
    Block state execution until you are able to get the lock (or hit the timeout)

    TODO: not poll, use watches

    /path
        /slots (where the people processing are)
        /queue (queue of things that want a slot)

    Try to get a slot, if its too many release and go to queue

    when you create a queue entry, create an ephemeral sequential node, and the lowest one down gets to go
        all children in the queue should watch the one in front of them (its FIFO)
        and the one at the head of the line should watch /slots for a delete
    '''
    ret = {'name': path,
           'changes': {},
           'result': False,
           'comment': ''}

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'attempt to aqcuire lock'
        return ret

    zk = _get_zk_conn(zk_hosts)
    if path not in SEMAPHORE_MAP:
        SEMAPHORE_MAP[path] = Semaphore(zk,
                                        path,
                                        __grains__['fqdn'],
                                        max_leases=max_concurrency,
                                        ephemeral_lease=ephemeral_lease)
    # block waiting for lock acquisition
    if timeout:
        SEMAPHORE_MAP[path].acquire(timeout=timeout)
    else:
        SEMAPHORE_MAP[path].acquire()

    if SEMAPHORE_MAP[path].is_acquired:
        ret['result'] = True
        ret['comment'] = 'lock acquired'
    else:
        ret['comment'] = 'Unable to acquire lock'

    return ret


def unlock(zk_hosts, path):
    '''
    Remove lease from semaphore
    '''
    global SEMAPHORE_MAP
    ret = {'name': path,
           'changes': {},
           'result': False,
           'comment': ''}

    if __opts__['test']:
        ret['result'] = None
        ret['comment'] = 'released lock if its here'
        return ret

    if path in SEMAPHORE_MAP:
        SEMAPHORE_MAP[path].release()
        del SEMAPHORE_MAP[path]
    else:
        ret['comment'] = 'Unable to find lease for path {0}'.format(path)
        return ret

    ret['result'] = True
    return ret


# TODO: use the kazoo one, waiting for pull req: https://github.com/python-zk/kazoo/pull/206
class Semaphore(kazoo.recipe.lock.Semaphore):
    def __init__(self,
                 client,
                 path,
                 identifier=None,
                 max_leases=1,
                 ephemeral_lease=True,
                 ):
        super(Semaphore, self).__init__(client,
                                        path,
                                        identifier=identifier,
                                        max_leases=max_leases)

        self.ephemeral_lease = ephemeral_lease

    def _get_lease(self, data=None):
        # Make sure the session is still valid
        if self._session_expired:
            raise ForceRetryError("Retry on session loss at top")

        # Make sure that the request hasn't been canceled
        if self.cancelled:
            raise CancelledError("Semaphore cancelled")

        # Get a list of the current potential lock holders. If they change,
        # notify our wake_event object. This is used to unblock a blocking
        # self._inner_acquire call.
        children = self.client.get_children(self.path,
                                            self._watch_lease_change)

        # If there are leases available, acquire one
        if len(children) < self.max_leases:
            self.client.create(self.create_path, self.data, ephemeral=self.ephemeral_lease)

        # Check if our acquisition was successful or not. Update our state.
        if self.client.exists(self.create_path):
            self.is_acquired = True
        else:
            self.is_acquired = False

        # Return current state
        return self.is_acquired
