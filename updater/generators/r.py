# R generator
#
# @author Daniel J. Finnegan
# @date April 2018

import os
from os import path
import logging
from logging import handlers
import generators.base_gen as base_gen

class RGenerator(base_gen.ProjectGenerator):

    def __init__(self, proj_root):
        super(RGenerator, self).__init__(proj_root)
        self.template_name = 'latex.txt'
        self.template_keys['projname'] =  'R-Updater-Project'
        self.template_keys['appname'] =  'DanDan\'s-Application'
        self.template_keys['proj_languages'] = 'NONE'
        self.cmake_module_files = ['FindR.cmake']

    def write_sample_source_file(self):
        os.mkdir(os.path.join(self.project_root, 'src'))
        file_contents = (
            '%%\n'
            '%% Automatically generated by Updater v' + str(self.template_keys['version_number']) + '\n'
            '%% @author ' + self.template_keys['author_name'] + '\n'
            '%%\n'
            '\n'
            '---\n'
            'title: "' + self.template_keys['projname'] + '"\n'
            'output:\n'
            '    html_notebook: default\n'
            '    pdf_document: default\n'
            '---\n\n'
            '```{r, warnings=FALSE}\n'
            'library (\'rmarkdown\');\n'
            'library (\'dplyr\');\n'
            'library (\'ggplot2\');\n'
            'library (\'reshape2\');\n'
            '```\n\n'
            'To begin...'
            )

        with open(os.path.join(self.project_root, 'src', 'main.Rmd'), 'w') as sample_source:
            sample_source.write(file_contents)