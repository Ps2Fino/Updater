# Base generator.
# All other generators inherit from this
#
# @author Daniel J. Finnegan
# @date September 2017

import os, sys
from os import path
import logging
from logging import handlers
import re
import shutil

class ProjectGenerator(object):

    def __init__(self, proj_root):
        self.initialize(proj_root)

    def initialize(self, proj_root):
        self.project_root = proj_root
        self.logger = logging.getLogger('updater_application')
        self.template_name = 'base.txt'
        self.template_keys = {
           'version_number': '1.0',
            'author_name': 'Daniel J. Finnegan',
            'installer_name': 'My-Program-Installer',
            'companyname': 'Lancophone',
            'install_description': '"Installs the application to your machine"'
        }
        self.cmake_module_files = []

    def remove_and_replace(self, lines):
        del lines[0:7]
        def replace_key_vals(match):
#            for key, value in self.template_keys.iteritems():
            for (key, value) in self.template_keys.items():
                if key in match.string:
                    return value
        regex = re.compile(r">>>>>{(\w+)}")
        lines = [regex.sub(replace_key_vals, line) for line in lines]
        return lines

    def write_cmake_file(self):
        with open (os.path.join(os.getcwd(), 'templates', 'languages', 'base.txt')) as f:
            base = f.readlines()
        base = self.remove_and_replace(base)
        with open (os.path.join(os.getcwd(), 'templates', 'languages', self.template_name)) as f:
            lines = f.readlines()
        lines = self.remove_and_replace(lines)
        templ = base + lines
        with open(os.path.join(self.project_root, 'CMakeLists.txt'), 'w') as cmake_file:
            cmake_file.writelines(templ)

    def write_installer_file(self):
        # Delete the header from the template file
        with open (os.path.join(os.getcwd(), 'templates', 'installers', 'windows_installer.txt')) as f:
            base = f.readlines()
        base = self.remove_and_replace(base)
        with open(os.path.join(self.project_root, 'scripts', 'installer.nsi'), 'w') as installer_file:
            installer_file.writelines(base)

        # Copy the license folder over
        os.mkdir(os.path.join(self.project_root, 'licenses'))
        shutil.copy(os.path.join(os.getcwd(), 'templates', 'licenses', 'BSD-3-license.txt'),
                    os.path.join(self.project_root, 'licenses'))

    def write_build_script_files(self):
        with open (os.path.join(os.getcwd(), 'templates', 'project-builders', 'cross_platform_build.txt')) as f:
            build_script = f.readlines()
        build_script = self.remove_and_replace(build_script)
        with open(os.path.join(self.project_root, 'build.py'), 'w') as installer_file:
            installer_file.writelines(build_script)

    def write_readme_file(self):
        file_contents = (
            '# ' + os.path.basename(self.project_root) +'\n'
            'Put your README information here\n'
        )

        with open(os.path.join(self.project_root, 'README.md'), 'w') as readme_file:
            readme_file.write(file_contents)

    def write_build_file(self):
        file_contents = (
            '#\n'
            '# Module automatically generated by Updater v' + str(self.template_keys['version_number']) + '\n'
            '# @author ' + self.template_keys['author_name'] + '\n'
            '#\n'
            '\n'
            'import os\n'
            'from subprocess import call\n'
            '\n'
            'UPDATER_CMAKE_ARGS = [\'-DBUILD_INSTALLER=OFF\'] # Turn this on to build the installer\n'
            'UPDATER_BUILD_CUSTOM = True # Set this to True if your project has a custom build function\n'
            '\n'
            '# Default implementation just calls cmake\n'
            '# Reimplement as you see fit\n'
            'def build_full_package(project_root):\n'
            '    if not os.path.isdir(os.path.join(project_root, \'bin\')):\n'
            '        os.mkdir(os.path.join(project_root, \'bin\'))\n'
            '\n'
            '    os.chdir(os.path.join(project_root, \'bin\'))\n'
            '    call([\'cmake\'] + UPDATER_CMAKE_ARGS + [\'..\'])\n'
            '    call([\'cmake\', \'--build\', \'.\'])\n'
            '\n####################################################################\n'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', 'build_project.py'), 'w') as build_module:
            build_module.write(file_contents)

        # Save a handy little batch file for Windows projects
        file_contents = (
            '@python build.py\n'
        )
        with open(os.path.join(self.project_root, 'make.bat'), 'w') as build_module:
            build_module.write(file_contents)

    def write_sample_source_file(self):
        pass

    def copy_generator_specific_files(self):
        pass

    def write_init_file(self):
        file_contents = (
            '# __init__ file for module\n'
            '# @author ' + self.template_keys['author_name'] + '\n'
            '\n'
            '__all__ = [\'build_project\']\n'
        )

        with open(os.path.join(self.project_root, 'scripts', 'builder', '__init__.py'), 'w') as init_module:
            init_module.write(file_contents)

    def copy_module_files(self):
        for module in self.cmake_module_files:
            with open(os.path.join(os.getcwd(), 'templates', 'cmake-modules', module), 'r') as input_f:
                input_data = input_f.readlines()
            with open(os.path.join(self.project_root, 'cmake', module), 'w') as output_f:
                output_f.writelines(input_data)

    def write_make_file(self):
        if sys.platform == 'darwin':
            file_contents = (
                'all:\n'
                '    @python build.py\n'
            )
            file_name = 'Makefile'
        else:
            file_contents = (
                '@python build.py'
            )
            file_name = 'make.bat'

        with open(os.path.join(self.project_root, file_name), 'w') as make_file:
            make_file.write(file_contents)

    def generate_project(self):
        if os.path.isdir(self.project_root):
            if os.path.isfile(os.path.join(self.project_root, 'CMakeLists.txt')):
                self.logger.info('Project already exists! Aborting...')
                return 1
        else:
            os.mkdir(self.project_root)

        # Go ahead and create the scripts folder
        os.mkdir(os.path.join(self.project_root, 'scripts'))
        os.mkdir(os.path.join(self.project_root, 'scripts', 'builder'))
        os.mkdir(os.path.join(self.project_root, 'cmake'))

        # Go ahead and write all the files to the directory
        self.write_init_file()
        self.write_readme_file()
        self.write_build_file()
        self.write_cmake_file()
        self.write_installer_file()
        self.write_build_script_files()
        self.write_sample_source_file()
        self.copy_module_files()
        self.copy_generator_specific_files()
        self.write_make_file()
        return 0

###########################################################