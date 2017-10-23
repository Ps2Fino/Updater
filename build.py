# Build script for Updater
# @author Daniel J. Finnegan

import shutil, os, os.path, sys
from subprocess import call

if __name__ == '__main__':
	shutil.rmtree('build', ignore_errors=True)
	shutil.rmtree('dist', ignore_errors=True)
	call(['pyinstaller', 'updater.spec'])
