# -*- coding: utf-8 -*-
'''
Interface with a Junos device via proxy-minion.
'''

# Import python libs
from __future__ import absolute_import
from __future__ import print_function
import logging
import copy

# Import 3rd-party libs
try:
    HAS_JUNOS = True
    import jnpr.junos
    import jnpr.junos.utils
    import jnpr.junos.utils.config
    import jnpr.junos.utils.sw
except ImportError:
    HAS_JUNOS = False

__proxyenabled__ = ['junos']

thisproxy = {}

log = logging.getLogger(__name__)

# Define the module's virtual name
__virtualname__ = 'junos'


def __virtual__():
    '''
    Only return if all the modules are available
    '''
    if not HAS_JUNOS:
        return False, 'Missing dependency: The junos proxy minion requires the \'jnpr\' Python module.'

    return __virtualname__


def init(opts):
    '''
    Open the connection to the Junos device, login, and bind to the
    Resource class
    '''
    log.debug('Opening connection to junos')
    args = { "host" : opts['proxy']['host'] }
    optional_args= ['user',
                    'password'
                    'port',
                    'gather_facts', 
                    'mode',
                    'baud',
                    'attempts',
                    'auto_probe',
                    'ssh_private_key',
                    'ssh_config',
                    'normalize'
                   ]
    for arg in optional_args:
        if arg in opts['proxy'].keys():
            args[arg] = opts['proxy'][arg]

    thisproxy['conn'] = jnpr.junos.Device(**args)
    thisproxy['conn'].open()
    thisproxy['conn'].bind(cu=jnpr.junos.utils.config.Config)
    thisproxy['conn'].bind(sw=jnpr.junos.utils.sw.SW)
    thisproxy['initialized'] = True


def initialized():
    return thisproxy.get('initialized', False)


def conn():
    return thisproxy['conn']


def proxytype():
    '''
    Returns the name of this proxy
    '''
    return 'junos'


def id(opts):
    return thisproxy['conn'].facts['hostname']


def grains():
    thisproxy['grains'] = copy.deepcopy(thisproxy['conn'].facts)
    thisproxy[
        'grains'][
        'version_info'] = thisproxy[
        'grains'][
        'version_info'].v_dict
    return thisproxy['grains']


def ping():
    '''
    Ping?  Pong!
    '''
    return thisproxy['conn'].connected


def shutdown(opts):
    '''
    This is called when the proxy-minion is exiting to make sure the
    connection to the device is closed cleanly.
    '''

    log.debug('Proxy module {0} shutting down!!'.format(opts['id']))
    try:
        thisproxy['conn'].close()

    except Exception:
        pass
