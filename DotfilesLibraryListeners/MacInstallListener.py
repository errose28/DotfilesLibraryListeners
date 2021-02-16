"""
Installs packages for MacOS using a combination of nix, homebrew, and pip as necessary.
Uses nix by default, but if a package is present as a key in one of the dictionaries,
the corresponding value will be installed by that package manager instead.
"""

import subprocess
from robot.api import logger
from . import NixInstallListener

ROBOT_LISTENER_API_VERSION = 2

# Map names used in setup robot files to names used by these package managers.

HOMEBREW_PKGS = {
    # Not in nixpkgs.
    'cliclick': 'cliclick',
    # No MacOS build in nixpkgs.
    'ffmpegthumbnailer': 'ffmpegthumbnailer',
    # Install from homebrew for icon that appears in launchpad.
    'alacritty': 'alacritty',
    # No MacOS build in nixpkgs.
    'google-chrome': 'google-chrome',
    # No MacOS build in nixpkgs.
    'jetbrains.idea-community': 'intellij-idea-ce'
}

PIP_PKGS = {
    # nixpkgs build is broken for MacOS.
    # Not present in homebrew.
    'powerline': 'powerline-status'
}

# TODO: Use Interactive from DotfilesLibrary.
def start_keyword(name, attrs):
    if name == 'DotfilesLibrary.Emit' and attrs['args'][0] == 'Install':
        logger.debug('Registered Emit call in ' + __name__)

        for package in attrs['args'][1:]:
            if package in HOMEBREW_PKGS:
                brew_pkg = HOMEBREW_PKGS[package]
                logger.debug('Installing ' + brew_pkg + ' using homebrew')
                _run_cmd(['brew', 'install', brew_pkg])
            elif package in PIP_PKGS:
                pip_pkg = PIP_PKGS[package]
                logger.debug('Installing ' + pip_pkg + ' using pip')
                _run_cmd(['pip', 'install', pip_pkg])
            else:
                logger.debug('Forwarding install of ' + package + ' to NixInstallListener')
                NixInstallListener.nix_install(package)

def _run_cmd(cmd):
    logger.info(__name__ + ' running: ' + str(cmd))
    completed = subprocess.run(cmd)
    if completed.returncode != 0:
        logger.error(str(cmd) + ' failed with exit code ' + str(completed.returncode))
