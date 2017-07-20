from subprocess import call
import os, sys
from os import path
from Tkinter import *
from threading import *
import tkFileDialog
import logging
from logging import handlers

## This class implements the project downloadeer.
## This is version 1.0
## Future revisions will make this a standalone script that I will
## use for pulling and building all of my software
##
## @author Daniel J. Finnegan
## @date July 2017

class App(Tk):

    def __init__(self, master):
    	self.frame = Frame(master, height=640, width=480)
    	self.initialize()

    def initialize(self):
    	self.frame.grid()
    	self.init_vars()
    	self.init_controls()
    	self.init_gui()

    def init_vars(self):
        self.project_table = {
            'Spatiotemporal-Study': 'https://github.bath.ac.uk/djf32/spatiotemporal_study.git',
            'Updater': 'https://github.bath.ac.uk/djf32/Updater.git',
            'Test': 'https://github.bath.ac.uk/djf32/Test.git'
        }
        self.project_titles = sorted(self.project_table.keys()) # Get a sorted list of the keys

        self.branches = ['master', 'testing']
        self.project_root = 'C:\\'

        # Set the logger      
        if sys.platform == 'darwin':
            self.logger = logging.getLogger()
            syslogH = handlers.SysLogHandler(address='/var/run/syslog', facility='local1')
            syslogH.ident = 'updater_application:'
            self.logger.addHandler(syslogH)
        else: # Handle the Windows case
            self.logger = logging.getLogger('updater_application')

        self.logger.setLevel(logging.INFO)

    def init_controls(self):
    	self.project_root_text = StringVar()
    	self.project_root_text.set(self.project_root)

    	self.project_titles_var = StringVar()
    	self.project_titles_var.set(self.project_titles[0])

        self.branches_var = StringVar()
        self.branches_var.set(self.branches[0])

    def init_gui(self):
    	# Option box for selecting the project to install
    	self.project_label = Label(self.frame, text='Branch to Install or Update:')
    	self.projects_options = OptionMenu(self.frame, self.project_titles_var, *self.project_titles)
    	self.project_label.grid(column=0, row=0, sticky='W')
    	self.projects_options.grid(column=1, columnspan=3, row = 0, sticky='W')

        # Option box for selecting the project to install
        self.project_label = Label(self.frame, text='Project to Install or Update:')
        self.projects_options = OptionMenu(self.frame, self.branches_var, *self.branches)
        self.project_label.grid(column=0, row=1, sticky='W')
        self.projects_options.grid(column=1, columnspan=3, row = 1, sticky='W')

    	# Entry for specifying the directory to install the project
    	# Complete with side label and action button
    	self.directory_label = Label(self.frame, text='Project Directory to Install or Update:')
    	self.directory_entry = Entry(self.frame, textvariable=self.project_root_text, width=50)
    	self.set_directory_button = Button(self.frame, text="Set Directory", command=self.find_dir)
    	self.directory_label.grid(column=0, row=2, sticky='EW')
    	self.directory_entry.grid(column=1, columnspan=2, row=2, sticky='EW')
    	self.set_directory_button.grid(column=3, row=2, sticky='EW')

    	# Action button for updating
    	# self.update_button = Button(self.frame, text='Update', fg='red', command=self.frame.quit)
    	self.update_button = Button(self.frame, text='Update', fg='red', command=self.do_task)
    	self.update_button.grid(column=0, row=3, sticky='EW')

        # Text box for log output
        self.log = Text(self.frame, height=20, takefocus=0)
        self.log.grid(column=0, columnspan=4, row=4, sticky='EW')

    def find_dir(self):
    	self.project_root = tkFileDialog.askdirectory()
    	if self.project_root is None:
            return

    	self.project_root_text.set(self.project_root)

    def build_project(self):
        self.log_message('Building the software package...')
        os.chdir(self.project_root) # Move to the root of the directory

        self.log_message('Building the project...')
        sys.path.append(os.getcwd() + '/scripts/')

        # Import the build script as a python module and then build it
        # If no custom build operation is specified, then make a standard call to cmake
        from builder import build_project
        if build_project.UPDATER_BUILD_CUSTOM:
            build_project.build_full_package(self.project_root) # Pass in the root directory 
        else:
            if os.path.isdir(os.path.join(self.project_root, 'bin')):
                shutil.rmtree(os.path.join(self.project_root, 'bin'))

            os.mkdir(os.path.join(self.project_root, 'bin'))
            os.chdir(os.path.join(self.project_root, 'bin'))
            rc = call(['cmake'] + build_project.UPDATER_CMAKE_ARGS + ['..'])
            if rc != 0:
                self.log_message(message='Project is missing a CMakeLists.txt file. Contact the package maintainer')
            else:
                call(['cmake', '--build', '.'])

        self.log_message('Project built!')

    def update_project(self):
        self.log_message(message='Updating the software package...')
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the master branch
        call(['git', '-C', self.project_root, 'pull', 'origin', self.branches_var.get()]) # Pull the changes made in the project from the repo
        self.log_message('Software updated!')

    def download_project(self):
        self.log_message(message='Downloading the software...')
        project_url = self.project_urls[self.project_titles_var.get()]
        call(['git', '-C', self.project_root, 'clone', self.project_table[self.project_titles_var.get()], self.project_titles_var.get()]) # Clone the project from the remote repo
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the branch
        self.project_root = os.path.join(self.project_root, self.project_titles_var.get()) # Update the directory name to reflect the downloaded package
        self.log_message('Software downloaded!')

    def do_task(self):

        # Add paths
        if sys.platform == 'darwin':
            # sys.path.append('/usr/local/bin')
            os.environ['PATH'] += ':' + '/usr/local/bin' # Patch for homebrew installations
        elif sys.platform == 'win32':
            self.log_message(message='Windows is buggy. Please report any issues')
        else:
            self.log_message(message='Platform unsupported. Aborting')
            return

    	rc = call(['git', '-C', self.project_root, 'status']) # Run git status
    	if rc == 0:
            def update_in_thread():
                self.update_button.config(state=DISABLED)

                self.update_project()
                self.build_project() # Pass in the project root folder

                self.update_button.config(state=ACTIVE)
                return

            thread = Thread(target=update_in_thread)
            thread.start()
            return thread
    	else:
            def download_in_thread():
                self.update_button.config(state=DISABLED)

                self.download_project()
                self.build_project()

                self.update_button.config(state=ACTIVE)
                return

            thread = Thread(target=download_in_thread)
            thread.start()
            return thread

    def log_message(self, message=''):
        self.logger.info(message) # Log to the logger too
    	self.log.insert(INSERT, message)
        self.log.insert(INSERT, '\n')
    	self.log.see(END)

if __name__ == '__main__':
	root = Tk()
	root.title('Experiment Updater')
	app = App(root)
	root.mainloop()
	# root.destroy()