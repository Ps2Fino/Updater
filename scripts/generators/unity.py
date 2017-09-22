# This is the build script for Updater.
# This enables Updater to operate in a recursive manner; it can update itself!
#
# @author Daniel J. Finnegan
# @date July 2017

import base
import os
from os import path
import logging
from logging import handlers

class UnityGenerator(base.ProjectGenerator):

    def __init__(self, proj_root):
        self.initialize(proj_root)

    def initialize(self, proj_root):
        self.project_root = proj_root
        self.logger = logging.getLogger('updater_application')

    def write_cmake_file(self):
        file_contents = (
            '# Automatically generated by Updater v' + str(base.version_number) + '\n'
            '# @author ' + base.author_name + '\n'
            '\n'
            'cmake_minimum_required (VERSION 2.8)\n'
            'cmake_policy (SET CMP0048 NEW)\n'
            '\n'
            'project (\n'
            '\t\"Test\"\n'
            '\tVERSION\n'
            '\t\t1.0\n'
            ')\n'
            '\n'
            'set (\n'
            '\tSOURCE_FILES\n'
            '\t\t\"src/main.cpp\"\n'
            ')\n'
            '\n'
            'add_executable (\n'
            '\tmain\n'
            '\t${SOURCE_FILES}\n'
            ')\n'
        )

        with open(os.path.join(self.project_root, 'CMakeLists.txt'), 'w') as cmake_lists:
            cmake_lists.write(file_contents)

    def write_sample_source_file(self):
        os.mkdir(os.path.join(self.project_root, 'Unity'))
        file_contents = (
            'Automatically generated by Updater v' + str(base.version_number) + '\n'
            '@author ' + base.author_name + '\n\n'
            '# Generate your Unity Project here\n'
        )

        with open(os.path.join(self.project_root, 'Unity', 'README.txt'), 'w') as sample_source:
            sample_source.write(file_contents)

###########################################################