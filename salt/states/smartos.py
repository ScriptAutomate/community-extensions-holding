# -*- coding: utf-8 -*-
'''
Management of SmartOS Standalone Compute Nodes
TODO:
 - docs (mention set null to remove property (pidfal with vlan_id), mention hostname, mac and path ID's...)
'''
from __future__ import absolute_import

# Import Python libs
import logging
import os

# Import Salt libs
import salt.utils
import salt.utils.files
from salt.utils.odict import OrderedDict

log = logging.getLogger(__name__)

# Define the state's virtual name
__virtualname__ = 'smartos'


def __virtual__():
    '''
    Provides smartos state provided for SmartOS
    '''
    return __virtualname__ if 'vmadm.create' in __salt__ else False


def _load_config():
    '''
    Loads and parses /usbkey/config
    '''
    config = {}

    if os.path.isfile('/usbkey/config'):
        with open('/usbkey/config', 'r') as config_file:
            for optval in config_file:
                if optval[0] == '#':
                    continue
                if '=' not in optval:
                    continue
                optval = optval.split('=')
                config[optval[0].lower()] = optval[1].strip()
    log.debug('read /usbkey/config: {0}'.format(config))
    return config


def _write_config(config):
    '''
    writes /usbkey/config
    '''
    with open('/usbkey/config.salt', 'w') as config_file:
        config_file.write("#\n# This file was generated by salt\n#\n")
        for prop in OrderedDict(sorted(config.items())):
            config_file.write("{0}={1}\n".format(prop, config[prop]))

    if os.path.isfile('/usbkey/config.salt'):
        try:
            salt.utils.files.rename('/usbkey/config.salt', '/usbkey/config')
        except IOError:
            return False
        log.debug('wrote /usbkey/config: {0}'.format(config))
        return True
    else:
        return False


def config_present(name, value):
    '''
    Ensure configuration property is present in /usbkey/config

    name : string
        name of property
    value : string
        value of property

    '''
    name = name.lower()
    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # load confiration
    config = _load_config()

    # handle bool and None value
    if isinstance(value, (bool)):
        value = 'true' if value else 'false'
    if not value:
        value = ""

    if name in config:
        if config[name] == value:
            # we're good
            ret['result'] = True
            ret['comment'] = 'property {0} already has value "{1}"'.format(name, value)
        else:
            # update property
            ret['result'] = True
            ret['comment'] = 'updated property {0} with value "{1}"'.format(name, value)
            ret['changes'][name] = value
            config[name] = value
    else:
        # add property
        ret['result'] = True
        ret['comment'] = 'added property {0} with value "{1}"'.format(name, value)
        ret['changes'][name] = value
        config[name] = value

    # apply change if needed
    if not __opts__['test'] and len(ret['changes']) > 0:
        ret['result'] = _write_config(config)

    return ret


def config_absent(name):
    '''
    Ensure configuration property is absent in /usbkey/config

    name : string
        name of property

    '''
    name = name.lower()
    ret = {'name': name,
           'changes': {},
           'result': None,
           'comment': ''}

    # load configuration
    config = _load_config()

    if name in config:
        # delete property
        ret['result'] = True
        ret['comment'] = 'property {0} deleted'.format(name)
        ret['changes'][name] = None
        del config[name]
    else:
        # we're good
        ret['result'] = True
        ret['comment'] = 'property {0} is absent'.format(name)

    # apply change if needed
    if not __opts__['test'] and len(ret['changes']) > 0:
        ret['result'] = _write_config(config)

    return ret

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
