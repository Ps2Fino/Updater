# This is the build script for Updater.
# This enables Updater to operate in a recursive manner; it can update itself!
#
# @author Daniel J. Finnegan
# @date July 2017

def build_project(project_root):
	os.chdir(project_root) # Move back up to the root directory
	call(['pyinstaller', 'updater.spec']) # Just ask pyinstaller to build us again