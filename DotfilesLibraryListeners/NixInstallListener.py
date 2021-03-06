import subprocess
import os
from pathlib import Path
from robot.api import logger

ROBOT_LISTENER_API_VERSION = 2

PKG_ALIASES = {
    # Install polybar from my nixpkgs overlay with support for extra modules enabled.
    # This means it will need to be built from source.
    'polybar': 'polybar-extra-support'
}

# Lower number means higher priority.
package_priorities = {
    # These 2 packages have a conflict for the SpaceMono-Italic font.
    # Both have original priority 5.
    'powerline-fonts': 0,
    'google-fonts': 6
}

# TODO: Use Interactive from DotfilesLibrary.
def start_keyword(name, attrs):
    if name == 'DotfilesLibrary.Emit' and attrs['args'][0] == 'Install':
        logger.debug('Registered Emit call in ' + __name__)

        for package in attrs['args'][1:]:
            nix_install(package)

def nix_install(package):
    _run_cmd(['nix-env', '--install', '--attr', _resolve(package)])
    _set_priorities(package)

def _set_priorities(package):
    if package in package_priorities:
        priority = package_priorities[package]
        _run_cmd(['nix-env', '--set-flag', 'priority', str(priority), package])

def _resolve(package):
    # Determine the prefix to use.
    os_path = Path(os.path.sep, 'etc', 'os-release')
    prefix = 'nixpkgs'

    if os_path.exists():
        with open(os_path, 'r') as os_file:
            if 'NixOS' in os_file.read():
                prefix = 'nixos'

    # Install the package by a different name if specified by PKG_ALIASES.
    return prefix + '.' + PKG_ALIASES.get(package, package)

def _run_cmd(cmd):
    logger.info(__name__ + ' running: ' + str(cmd))
    completed = subprocess.run(cmd)
    if completed.returncode != 0:
        logger.error(str(cmd) + ' failed with exit code ' + str(completed.returncode))
