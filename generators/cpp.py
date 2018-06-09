# Base generator.
# All other generators inherit from this
#
# @author Daniel J. Finnegan
# @date September 2017

import os
from os import path
import logging
from logging import handlers
import base_gen

class CppGenerator(base_gen.ProjectGenerator):

    def __init__(self, proj_root):
        super(CppGenerator, self).__init__(proj_root)
        self.template_name = 'cpp.txt'
        self.template_keys['projname'] =  'C++-Updater-Project'
        self.template_keys['appname'] =  'DanDan\'s-Application'
        self.template_keys['proj_languages'] = 'CXX'
        self.cmake_module_files = ['Findfftw.cmake', 'FindFMOD.cmake', 'Findlibsndfile.cmake']

    def write_sample_source_file(self):
        os.mkdir(os.path.join(self.project_root, 'src'))
        file_contents = (
            '/**\n'
            '    Automatically generated by Updater v' + str(self.template_keys['version_number']) + '\n'
            '    @author ' + self.template_keys['author_name'] + '\n'
            '*/\n'
            '\n'
            '#include <iostream>\n'
            '\n'
            'int main(int argc, char **argv)\n'
            '{\n'
            '    std::cout << \"Hello World\" << std::endl;\n'
            '    return 0;\n'
            '}\n'
        )

        with open(os.path.join(self.project_root, 'src', 'main.cpp'), 'w') as sample_source:
            sample_source.write(file_contents)

###########################################################