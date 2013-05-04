'''
Support for GRUB Legacy
'''

# Import python libs
import os

# Import salt libs
import salt.utils
from salt.exceptions import CommandExecutionError


def __virtual__():
    '''
    Only load the module if grub is installed
    '''
    conf = _detect_conf()
    if os.path.exists(conf):
        return 'grub'
    return False


@salt.utils.memoize
def _detect_conf():
    '''
    GRUB conf location differs depending on distro
    '''
    if __grains__['os_family'] == 'RedHat':
        return '/boot/grub/grub.conf'
    # Defaults for Ubuntu, Debian, Arch, and others
    return '/boot/grub/menu.lst'


def version():
    '''
    Return server version from grub --version

    CLI Example::

        salt '*' grub.version
    '''
    cmd = '/sbin/grub --version'
    out = __salt__['cmd.run'](cmd)
    return out


def conf():
    '''
    Parse GRUB conf file

    CLI Example::

        salt '*' grub.conf
    '''
    stanza = ''
    stanzas = []
    in_stanza = False
    ret = {}
    pos = 0
    try:
        with salt.utils.fopen(_detect_conf(), 'r') as _fp:
            for line in _fp:
                if line.startswith('#'):
                    continue
                if line.startswith('\n'):
                    in_stanza = False
                    if 'title' in stanza:
                        stanza += 'order {0}'.format(pos)
                        pos += 1
                        stanzas.append(stanza)
                    stanza = ''
                    continue
                if line.startswith('title'):
                    in_stanza = True
                if in_stanza:
                    stanza += line
                if not in_stanza:
                    key, value = _parse_line(line)
                    ret[key] = value
            if in_stanza:
                if not line.endswith('\n'):
                    line += '\n'
                stanza += line
                stanza += 'order {0}'.format(pos)
                pos += 1
                stanzas.append(stanza)
    except (IOError, OSError) as exc:
        msg = "Could not read grub config: {0}"
        raise CommandExecutionError(msg.format(str(exc)))

    ret['stanzas'] = []
    for stanza in stanzas:
        mydict = {}
        for line in stanza.strip().splitlines():
            key, value = _parse_line(line)
            mydict[key] = value
        ret['stanzas'].append(mydict)
    return ret


def _parse_line(line=''):
    '''
    Used by conf() to break config lines into
    name/value pairs
    '''
    parts = line.split()
    key = parts.pop(0)
    value = ' '.join(parts)
    return key, value
