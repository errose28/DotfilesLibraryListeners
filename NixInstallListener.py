import subprocess
import os
from pathlib import Path
from robot.api import logger

ROBOT_LISTENER_API_VERSION = 2

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
            run_cmd(['nix-env', '--install', '--attr', add_prefix(package)])
            set_priorities(package)

def set_priorities(package):
    if package in package_priorities:
        priority = package_priorities[package]
        run_cmd(['nix-env', '--set-flag', 'priority', str(priority), package])

def add_prefix(package):
    os_path = Path(os.path.sep, 'etc', 'os-release')
    prefix = 'nixpkgs'

    if os_path.exists():
        with open(os_path, 'r') as os_file:
            if 'NixOS' in os_file.read():
                prefix = 'nixos'

    return prefix + '.' + package

def run_cmd(cmd):
    logger.info(__name__ + ' running: ' + str(cmd))
    completed = subprocess.run(cmd)
    if completed.returncode != 0:
        logger.error(str(cmd) + ' failed with exit code ' + str(completed.returncode))
