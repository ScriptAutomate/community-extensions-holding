# -*- coding: utf-8 -*-

# Import Python libs
import copy
import logging
import re

# Import Salt libs
from salt.serializers import json
from salt.exceptions import CommandExecutionError

log = logging.getLogger(__name__)

# Don't shadow built-in's.
__func_alias__ = {
    'list_': 'list'
}


class HelmExecutionError(CommandExecutionError):
    def __init__(self, cmd, error):
        self.cmd = cmd
        self.error = error


def _prepare_cmd(binary='helm', commands=[], flags=[], kvflags={}):
    '''

    :param binary:
    :param commands:
    :param flags:
    :param kvflags:
    :return:
    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd = (binary,)

    for command in commands:
        cmd += (command,)

    for arg in flags:
        if not re.search(r'^--.*', arg):
            arg = '--' + arg
        cmd += (arg,)

    for key, val in kvflags.items():
        if not re.search(r'^--.*', key):
            key = '--' + key
        cmd += (key, val,)

    return cmd


def _exec_cmd(commands=[], flags=[], kvflags={}):
    '''

    :param commands:
    :param flags:
    :param kvflags:
    :return:
    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)

    cmd = _prepare_cmd(commands=commands, flags=flags, kvflags=kvflags)
    cmd_string = " ".join(cmd)

    try:
        result = __salt__['cmd.run_all'](cmd=cmd)
        result.update({'cmd': cmd_string})
        return result
    except CommandExecutionError as e:
        raise HelmExecutionError(cmd_string, e)


def completion(shell, flags=[], kvflags={}):
    '''
    Generate auto-completions script for Helm for the specified shell (bash or zsh).
    Return the shell auto-completion content.

    shell
        (string) One of ['bash', 'zsh'].

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.completion bash

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['completion', shell], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def create(name, flags=[], kvflags={}):
    '''
    Creates a chart directory along with the common files and directories used in a chart.
    Return True if succeed, else the error message.

    name
        (string) The chart name to create.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.create NAME

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['create', name], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def dependency_build(chart, flags=[], kvflags={}):
    '''
    Build out the charts/ directory from the Chart.lock file.
    Return True if succeed, else the error message.

    chart
        (string) The chart name to build dependency.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.dependency_build CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['dependency', 'build', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def dependency_list(chart, flags=[], kvflags={}):
    '''
    List all of the dependencies declared in a chart.
    Return chart dependencies if succeed, else the error message.

    chart
        (string) The chart name to list dependency.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.dependency_list CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['dependency', 'list', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def dependency_update(chart, flags=[], kvflags={}):
    '''
    Update the on-disk dependencies to mirror Chart.yaml.
    Return True if succeed, else the error message.

    chart
        (string) The chart name to update dependency.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.dependency_update CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['dependency', 'update', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def env(flags=[], kvflags={}):
    '''
    Prints out all the environment information in use by Helm.
    Return Helm environments variables if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.env

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['env'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def get_all(release, flags=[], kvflags={}):
    '''
    Prints a human readable collection of information about the notes, hooks, supplied values, and generated manifest file of the given release.
    Return release information if succeed, else the error message.

    release
        (string) Release name to get information from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.get_all RELEASE

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['get', 'all', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def get_hooks(release, flags=[], kvflags={}):
    '''
    Prints a human readable collection of information about the hooks of the given release.
    Return release hooks information if succeed, else the error message.

    release
        (string) Release name to get hooks information from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.get_hooks RELEASE

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['get', 'hooks', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def get_manifest(release, flags=[], kvflags={}):
    '''
    Prints a human readable collection of information about the manifest of the given release.
    Return release manifest information if succeed, else the error message.

    release
        (string) Release name to get manifest information from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.get_manifest RELEASE

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['get', 'manifest', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def get_notes(release, flags=[], kvflags={}):
    '''
    Prints a human readable collection of information about the notes of the given release.
    Return release notes information if succeed, else the error message.

    release
        (string) Release name to get notes information from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.get_notes RELEASE

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['get', 'notes', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def get_values(release, flags=[], kvflags={}):
    '''
    Prints a human readable collection of information about the values of the given release.
    Return release values information if succeed, else the error message.

    release
        (string) Release name to get values information from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.get_values RELEASE

        # In YAML format
        salt '*' helm.get_values RELEASE kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['get', 'values', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def help(command, flags=[], kvflags={}):
    '''
    Provides help for any command in the application.
    Return the full help if succeed, else the error message.

    command
        (string) Command to get help. ex: 'get'

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.help COMMAND

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['help', command], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def history(release, flags=[], kvflags={}):
    '''
    Prints historical revisions for a given release.
    Return release historic if succeed, else the error message.

    release
        (string) Release name to get history from.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.history RELEASE

        # In YAML format
        salt '*' helm.history RELEASE kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['history', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def install(release, chart, flags=[], kvflags={}):
    '''
    Installs a chart archive.
    Return True if succeed, else the error message.

    release
        (string) Release name to get values information from.

    chart
        (string) Chart name to install.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.install RELEASE CHART

        # With values file.
        salt '*' helm.install RELEASE CHART kvflags="{'values': '/path/to/values.yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['install', release, chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def lint(path, flags=[], kvflags={}):
    '''
    Takes a path to a chart and runs a series of tests to verify that the chart is well-formed.
    Return True if succeed, else the error message.

    path
        (string) The path to the chart to lint.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.lint PATH

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['lint', path], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def list_(flags=[], kvflags={}):
    '''
    Lists all of the releases. By default, it lists only releases that are deployed or failed.
    Return the list of release if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.list

        # In YAML format
        salt '*' helm.list kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['list'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def package(chart, flags=[], kvflags={}):
    '''
    Packages a chart into a versioned chart archive file. If a path is given, this will look at that path for a chart
    (which must contain a Chart.yaml file) and then package that directory.
    Return True if succeed, else the error message.

    chart
        (string) Chart name to package. Can be an absolute path.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.package CHART

        # With destination path.
        salt '*' helm.package CHART kvflags="{'destination': '/path/to/the/package'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['package', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def plugin_install(path, flags=[], kvflags={}):
    '''
    Install a Helm plugin from a url to a VCS repo or a local path.
    Return True if succeed, else the error message.

    path
        (string) Path to the local plugin. Can be an url.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.plugin_install PATH

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['plugin', 'install', path], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def plugin_list(flags=[], kvflags={}):
    '''
    List installed Helm plugins.
    Return the plugin list if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.plugin_list

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['plugin', 'list'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def plugin_uninstall(plugin, flags=[], kvflags={}):
    '''
    Uninstall a Helm plugin.
    Return True if succeed, else the error message.

    plugin
        (string) The plugin to uninstall.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.plugin_uninstall PLUGIN

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['plugin', 'uninstall', plugin], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def plugin_update(plugin, flags=[], kvflags={}):
    '''
    Update a Helm plugin.
    Return True if succeed, else the error message.

    plugin
        (string) The plugin to update.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.plugin_update PLUGIN

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['plugin', 'update', plugin], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def pull(package, flags=[], kvflags={}):
    '''
    Retrieve a package from a package repository, and download it locally.
    Return True if succeed, else the error message.

    package
        (string) The package to pull. Can be url or repo/chartname.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.pull PACKAGE

        # With destination path to write the chart.
        salt '*' helm.pull PACKAGE kvflags="{'destination': '/path/to/the/chart'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['pull', package], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_add(name, url, flags=[], kvflags={}):
    '''
    Add a chart repository.
    Return True if succeed, else the error message.

    name
        (string) The local name of the repository to install. Have to be unique.

    url
        (string) The url to the repository.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.repo_add NAME URL

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['repo', 'add', name, url], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_index(directory, flags=[], kvflags={}):
    '''
    Read the current directory and generate an index file based on the charts found.
    Return True if succeed, else the error message.

    directory
        (string) The path to the index.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.index DIRECTORY

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['repo', 'index', directory], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_list(flags=[], kvflags={}):
    '''
    List a chart repository.
    Return the repository list if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.repo_list

        # In YAML format
        salt '*' helm.repo_list kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    log.error(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['repo', 'list'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_remove(name, flags=[], kvflags={}):
    '''
    Remove a chart repository.
    Return True if succeed, else the error message.

    name
        (string) The local name of the repository to remove.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.repo_remove NAME

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['repo', 'remove', name], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_update(flags=[], kvflags={}):
    '''
    Update all charts repository.
    Return True if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.repo_update

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['repo', 'update'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def repo_manage(present=[], absent=[], prune=False, flags=[], kvflags={}):
    '''
    Manage charts repository.
    Return the summery of all actions.

    present
        (list) List of repository to be present. It's a list of dict: [{'name': 'local_name', 'url': 'repository_url'}]

    absent
        (list) List of local name repository to be absent.

    prune
        (boolean - default: False) If True, all repository already present but not in the present list would be removed.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.repo_manage present="[{'name': 'LOCAL_NAME', 'url': 'REPO_URL'}]" absent="['LOCAL_NAME']"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    repos_present = repo_list(flags=flags, kvflags=kvflags)
    if not isinstance(repos_present, list):
        repos_present = []
    result = {
        "present": [],
        "added": [],
        "absent": [],
        "removed": [],
        "failed": []
    }

    for repo in present:
        log.error(repo)
        if ('name', 'url') in repo.keys():
            raise CommandExecutionError("Parameter present have to be formatted like "
                                        "[{'name': '<myRepoName>', 'url': '<myRepoUrl>'}]")

        already_present = False
        for (index, repo_present) in enumerate(repos_present):
            if repo.get('name') == repo_present.get('name') and repo.get('url') == repo_present.get('url'):
                result['present'].append(repo)
                repos_present.pop(index)
                already_present = True
                break

        if not already_present:
            repo_add_status = repo_add(repo.get('name'), repo.get('url'), flags=flags, kvflags=kvflags)
            if isinstance(repo_add_status, bool) and repo_add_status:
                result['added'].append(repo)
            else:
                result['failed'].append(repo)

    for repo in repos_present:
        if prune:
            absent.append(repo.get('name'))
        elif not repo.get('name') in absent:
            result['present'].append(repo)

    for name in absent:
        remove_status = repo_remove(name)
        if isinstance(remove_status, bool) and remove_status:
            result['removed'].append(name)
        else:
            result['absent'].append(name)

    return result


def rollback(release, revision, flags=[], kvflags={}):
    '''
    Rolls back a release to a previous revision.
    To see release revision number, execute the history module.
    Return True if succeed, else the error message.

    release
        (string) The name of the release to managed.

    revision
        (string) The revision number to roll back to.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.rollback RELEASE REVISION

        # In dry-run mode.
        salt '*' helm.rollback RELEASE REVISION flags=['dry-run']

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['rollback', release, revision], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def search_hub(keyword, flags=[], kvflags={}):
    '''
    Search the Helm Hub or an instance of Monocular for Helm charts.
    Return the research result if succeed, else the error message.

    keyword
        (string) The keyword to search in the hub.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.search_hub KEYWORD

        # In YAML format
        salt '*' helm.search_hub KEYWORD kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    log.error(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['search', 'hub', keyword], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def search_repo(keyword, flags=[], kvflags={}):
    '''
    Search reads through all of the repositories configured on the system, and looks for matches. Search of these
    repositories uses the metadata stored on the system.
    Return the research result if succeed, else the error message.

    keyword
        (string) The keyword to search in the repo.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.search_hub KEYWORD

        # In YAML format
        salt '*' helm.search_hub KEYWORD kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    log.error(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['search', 'repo', keyword], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def show_all(chart, flags=[], kvflags={}):
    '''
    Inspects a chart (directory, file, or URL) and displays all its content (values.yaml, Charts.yaml, README).
    Return chart information if succeed, else the error message.

    chart
        (string) The chart to inspect.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.show_all CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['show', 'all', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def show_chart(chart, flags=[], kvflags={}):
    '''
    Inspects a chart (directory, file, or URL) and displays the contents of the Charts.yaml file.
    Return chart information if succeed, else the error message.

    chart
        (string) The chart to inspect.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.show_chart CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['show', 'chart', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def show_readme(chart, flags=[], kvflags={}):
    '''
    Inspects a chart (directory, file, or URL) and displays the contents of the README file.
    Return chart information if succeed, else the error message.

    chart
        (string) The chart to inspect.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.show_readme CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['show', 'readme', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def show_values(chart, flags=[], kvflags={}):
    '''
    Inspects a chart (directory, file, or URL) and displays the contents of the values.yaml file.
    Return chart information if succeed, else the error message.

    chart
        (string) The chart to inspect.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.show_values CHART

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['show', 'values', chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def status(release, flags=[], kvflags={}):
    '''
    Show the status of the release.
    Return the release status if succeed, else the error message.

    release
        (string) The release to status.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.status RELEASE

        # In YAML format
        salt '*' helm.status RELEASE kvflags="{'output': 'yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    if not ('output' in kvflags.keys() or '--output' in kvflags.keys()):
        kvflags.update({'output': 'json'})
    cmd_result = _exec_cmd(commands=['status', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        if kvflags.get('output') == 'json' or kvflags.get('--output') == 'json':
            result = json.deserialize(cmd_result.get('stdout', ''))
        else:
            result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def template(name, chart, flags=[], kvflags={}):
    '''
    Render chart templates locally and display the output.
    Return the chart renderer if succeed, else the error message.

    name
        (string) The template name.

    chart
        (string) The chart to template.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.template NAME CHART

        # With values file.
        salt '*' helm.template NAME CHART kvflags="{'values': '/path/to/values.yaml', 'output-dir': 'path/to/output/dir'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['template', name, chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def test(release, flags=[], kvflags={}):
    '''
    Runs the tests for a release.
    Return the test result if succeed, else the error message.

    release
        (string) The release name to test.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.test RELEASE

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['test', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result


def uninstall(release, flags=[], kvflags={}):
    '''
    Uninstall the release name.
    Return True if succeed, else the error message.

    release
        (string) The name of the release to managed.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.uninstall RELEASE

        # In dry-run mode.
        salt '*' helm.uninstall RELEASE flags=['dry-run']

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['uninstall', release], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def upgrade(release, chart, flags=[], kvflags={}):
    '''
    Upgrades a release to a new version of a chart.
    Return True if succeed, else the error message.

    release
        (string) The name of the release to managed.

    chart
        (string) The chart to managed.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.upgrade RELEASE CHART

        # In dry-run mode.
        salt '*' helm.upgrade RELEASE CHART flags=['dry-run']

        # With values file.
        salt '*' helm.upgrade RELEASE CHART kvflags="{'values': '/path/to/values.yaml'}"

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['upgrade', release, chart], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def verify(path, flags=[], kvflags={}):
    '''
    Verify that the given chart has a valid provenance file.
    Return True if succeed, else the error message.

    path
        (string) The path to the chart file.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.verify PATH

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['verify', path], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = True
    else:
        result = cmd_result.get('stderr', '')
    return result


def version(flags=[], kvflags={}):
    '''
    Show the version for Helm.
    Return version information if succeed, else the error message.

    flags
        (list) Flags in argument of the command without values. ex: ['help', '--help']

    kvflags
        (dict) Flags in argument of the command with values. ex: {'v': 2, '--v': 4}

    CLI Example:

    .. code-block:: bash

        salt '*' helm.version

    '''
    flags = copy.deepcopy(flags)
    kvflags = copy.deepcopy(kvflags)
    cmd_result = _exec_cmd(commands=['version'], flags=flags, kvflags=kvflags)
    if cmd_result.get('retcode', -1) == 0:
        result = cmd_result.get('stdout', '')
    else:
        result = cmd_result.get('stderr', '')
    return result
