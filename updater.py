from subprocess import call
import os, sys
from os import path
from Tkinter import *
import Tkinter
from threading import *
import tkFileDialog
import tkMessageBox
import logging
from logging import handlers
import csv

# Include the generators
sys.path.append(os.getcwd())
print sys.path
import generators.base_gen

## This file implements the project downloadeer.
## It is used for pulling and building all of my software
##
## @author Daniel J. Finnegan
## @date July 2017

####################################################################

class App(Tk):

    def __init__(self, master):
    	self.frame = Frame(master, height=640, width=480)
        self.menu = Menu(master)

        if sys.platform == 'darwin':
            self.appmenu = Menu(self.menu, name = 'apple') # Some extra fiddling about for OSX
            self.menu.add_cascade(menu=self.appmenu)
            self.appmenu.add_command(label='About Updater')

    	self.initialize()

    def initialize(self):
    	self.frame.grid()
    	self.init_vars()
    	self.init_controls()
        self.init_menu()
    	self.init_gui()

    def init_vars(self):
        self.project_table = {'': ''} # Empty table
        self.project_titles = sorted(self.project_table.keys()) # Get a sorted list of the keys

        self.branches = ['master', 'testing']
        self.generators = ['Unity', 'C++']
        
        if sys.platform == 'darwin':
            self.project_root = '/home/'
        else:
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

        self.generators_var = StringVar()
        self.generators_var.set(self.generators[0])

    def init_menu(self):
        if sys.platform == 'darwin': # We need to use the appmenu object for OSX applications
            self.appmenu.add_command(label='Quit', command=self.frame.quit)
            self.appmenu.add_command(label='Load Projects File', command=self.load_projects)
            self.appmenu.add_separator()
        else:
            self.menu.add_command(label='Quit', command=self.frame.quit)
            self.menu.add_command(label='Load Projects File', command=self.load_projects)

        root.config(menu=self.menu)

    def load_projects(self, *args):
        projects_file = tkFileDialog.askopenfilename(filetypes=[('project files', 'txt')], parent=self.frame)
        if projects_file is None or projects_file == '':
            return

        self.project_table = {} # clear the existing table
        with open(projects_file) as proj_file: # read in the projects from the file
            reader = csv.DictReader(proj_file)
            for row in reader:
                self.project_table[row['Project Name']] = row['Project URL']

        # TODO: Catch errors here in the file reader

        self.project_titles = sorted(self.project_table.keys()) # Get a sorted list of the keys
        self.project_titles_var.set(self.project_titles[0])
        menu = self.projects_options['menu']
        menu.delete(0, 'end')
        for project in self.project_titles: # Repopulate
            menu.add_command(label=project, command=lambda title=project: self.project_titles_var.set(title))

    def init_gui(self):
    	# Option box for selecting the project to install
        self.project_label = Label(self.frame, text='Project to Install or Update:')
        self.projects_options = OptionMenu(self.frame, self.project_titles_var, '')
    	self.project_label.grid(column=0, row=0, sticky='W')
    	self.projects_options.grid(column=1, columnspan=3, row = 0, sticky='W')

        # Option box for selecting the project to install
        self.branch_label = Label(self.frame, text='Branch to Install or Update:')
        self.project_branches = OptionMenu(self.frame, self.branches_var, *self.branches)
        self.branch_label.grid(column=0, row=1, sticky='W')
        self.project_branches.grid(column=1, columnspan=3, row = 1, sticky='W')

    	# Entry for specifying the directory to install the project
    	# Complete with side label and action button
    	self.directory_label = Label(self.frame, text='Project Directory to Install or Update:')
    	self.directory_entry = Entry(self.frame, textvariable=self.project_root_text, width=50)
    	self.set_directory_button = Button(self.frame, text="Set Directory", command=self.find_dir)
    	self.directory_label.grid(column=0, row=2, sticky='EW')
    	self.directory_entry.grid(column=1, columnspan=2, row=2, sticky='EW')
    	self.set_directory_button.grid(column=3, row=2, sticky='EW')

        # Action button for creating
        self.create_button = Button(self.frame, text='Create', command=self.create_project)
        self.project_generators = OptionMenu(self.frame, self.generators_var, *self.generators)
        self.create_button.grid(column=0, row=3, sticky='EW')
        self.project_generators.grid(column=1, columnspan=2, row = 3, sticky='EW')

        # Action button for updating
        self.build_button = Button(self.frame, text='Build', command=self.do_build_task)
        self.build_button.grid(column=0, row=4, sticky='EW')
        self.update_button = Button(self.frame, text='Update', command=self.do_task)
        self.update_button.grid(column=1, row=4, columnspan=2, sticky='EW')

        # Text box for log output
        self.log = Text(self.frame, height=20, takefocus=0)
        self.log.grid(column=0, columnspan=4, row=5, sticky='EW')

    def find_dir(self):
    	self.project_root = tkFileDialog.askdirectory()
    	if self.project_root is None:
            return

    	self.project_root_text.set(self.project_root)

    def build_project(self, project_to_build_dir=None):
        if project_to_build_dir is None:
            project_to_build_dir = self.project_root

        self.log_message('Building the software package...')
        sys.path.append(os.path.join(project_to_build_dir, 'scripts'))
        os.chdir(os.path.join(project_to_build_dir))

        # Import the build script as a python module and then build it
        # If no custom build operation is specified, then make a standard call to cmake
        from builder import build_project
        if build_project.UPDATER_BUILD_CUSTOM:
            build_project.build_full_package(project_to_build_dir) # Pass in the root directory 
        else:
            if os.path.isdir(os.path.join(project_to_build_dir, 'bin')):
                shutil.rmtree(os.path.join(project_to_build_dir, 'bin'))

            os.mkdir(os.path.join(project_to_build_dir, 'bin'))
            os.chdir(os.path.join(project_to_build_dir, 'bin'))
            rc = call(['cmake'] + build_project.UPDATER_CMAKE_ARGS + ['..'])
            if rc != 0:
                self.log_message(message='Project is missing a CMakeLists.txt file. Contact the package maintainer')
            else:
                call(['cmake', '--build', '.'])

        self.log_message('Check project directory for build output files.')

    def update_project(self):
        self.log_message(message='Updating the software package...')
        call(['git', '-C', self.project_root, 'checkout', '--', '.']) # Clear any local changes
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the master branch
        call(['git', '-C', self.project_root, 'pull', 'origin', self.branches_var.get()]) # Pull the changes made in the project from the repo
        self.log_message('Software updated!')

    def download_project(self):
        self.log_message(message='Downloading the software...')
        project_url = self.project_table[self.project_titles_var.get()]
        call(['git', '-C', self.project_root, 'clone', project_url, self.project_titles_var.get()]) # Clone the project from the remote repo
        
        self.project_root = os.path.join(self.project_root, self.project_titles_var.get()) # Update the directory name to reflect the downloaded package
        call(['git', '-C', self.project_root, 'checkout', self.branches_var.get()]) # Checkout the branch
        self.log_message('Software downloaded!')

    def do_task(self):

        # Check if the current selected project is empty
        if self.project_titles_var.get() == '':
            tkMessageBox.showerror(title='Missing Project', message='Please load the projects list file')
            return

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
                self.create_button.config(state=DISABLED)
                self.build_button.config(state=DISABLED)

                self.update_project()
                self.build_project() # Pass in the project root folder

                self.update_button.config(state=ACTIVE)
                self.create_button.config(state=ACTIVE)
                self.build_button.config(state=ACTIVE)
                return

            thread = Thread(target=update_in_thread)
            thread.start()
            return thread
    	else:
            def download_in_thread():
                self.update_button.config(state=DISABLED)
                self.create_button.config(state=DISABLED)
                self.build_button.config(state=DISABLED)

                self.download_project()
                self.build_project()

                self.update_button.config(state=ACTIVE)
                self.create_button.config(state=ACTIVE)
                self.build_button.config(state=ACTIVE)
                return

            thread = Thread(target=download_in_thread)
            thread.start()
            return thread

    def create_project(self):
        def create_in_thread():
            self.update_button.config(state=DISABLED)
            self.create_button.config(state=DISABLED)
            self.build_button.config(state=DISABLED)

            if self.generators_var.get() == 'Unity':
                project_generator = unity.UnityGenerator(self.project_root_text.get())
            elif self.generators_var.get() == 'C++':
                project_generator = cpp.CppGenerator(self.project_root_text.get())
            # elif self.generators_var.get() == '<insert_new_generator_here>':
            #     project_generator = <New>Generator(self.project_root_text.get())
            else:
                project_generator = base_gen.ProjectGenerator(self.project_root_text.get())

            self.log_message(message='Generating the project...')
            rc = project_generator.generate_project()
            if rc == 0:
                self.log_message('Project generated!')
            else:
                self.log_message('Project not generated. Check log for issues')

            self.update_button.config(state=ACTIVE)
            self.create_button.config(state=ACTIVE)
            self.build_button.config(state=ACTIVE)

        thread = Thread(target=create_in_thread)
        thread.start()
        return thread

    def do_build_task(self):
        def create_in_thread():
            self.update_button.config(state=DISABLED)
            self.create_button.config(state=DISABLED)
            self.build_button.config(state=DISABLED)

            print 'Building the project at', self.project_root_text.get()
            self.build_project(self.project_root_text.get()) # Pass in the project root folder

            self.update_button.config(state=ACTIVE)
            self.create_button.config(state=ACTIVE)
            self.build_button.config(state=ACTIVE)

        thread = Thread(target=create_in_thread)
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
    # root.title('Experiment Updater (Testing branch)')
	app = App(root)
	root.mainloop()
	# root.destroy()
