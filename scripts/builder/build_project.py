# This is the build script for Updater.
# This enables Updater to operate in a recursive manner; it can update itself!
#
# @author Daniel J. Finnegan
# @date July 2017

import os
from subprocess import call

UPDATER_CMAKE_ARGS = [] # Required CMake arguments for Updater
UPDATER_BUILD_CUSTOM = True # Whether or not this project has a custom build module

def build_full_package(project_root):
	os.chdir(project_root) # Move back up to the root directory
	call(['pyinstaller', 'updater.spec']) # Just ask pyinstaller to build us again

#######################################################

if __name__=='__main__':
	build_full_package('.')

