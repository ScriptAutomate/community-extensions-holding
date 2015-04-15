# -*- coding: utf-8 -*-
'''
Grains for junos.
NOTE this is a little complicated--junos can only be accessed via salt-proxy-minion.
Thus, some grains make sense to get them from the minion (PYTHONPATH), but others
don't (ip_interfaces)
'''
import logging
import json
__proxyenabled__ = ['junos']

__virtualname__ = 'junos'

log = logging.getLogger(__name__)

def __virtual__():
    if 'proxy' not in __opts__:
        return False
    else:
        return __virtualname__

def _remove_complex_types(dictionary):
    '''
    Linode-python is now returning some complex types that
    are not serializable by msgpack.  Kill those.
    '''

    for k, v in dictionary.iteritems():
        if isinstance(v, dict):
            dictionary[k] = remove_complex_types(v)
        elif hasattr(v, 'to_eng_string'):
            dictionary[k] = v.to_eng_string()

def defaults():
    return {'os': 'proxy', 'kernel':'unknown', 'osrelease':'proxy'}

def facts():
    log.debug('----------- Trying to get facts')
    facts = __opts__['proxymodule']['junos.facts']()
    facts['version_info'] = 'override'
    return facts
    log.debug('----------- Facts call to junos returned')

def os_family():
    return {'os_family': 'junos'}

