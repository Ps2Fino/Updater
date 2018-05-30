# Updater
Updater is a template engine: when you execute its operation on a directory on your machine, it will create a directory structure along with boilerplate files.
These files and direectory structure are configured to enable Updater to build the project with one click!

I use it to create project templates for all my students at the [University of Bath](www.bath.ac.uk).
If you use it and find it helpful, please send me an email and write a message on the wiki.

# Adding new templates
Whenever you add a new template to the engine, be sure to update the `hiddenimports` list in the `Analysis` list in the `updater.spec` file.
You also need to modify `pyhooks/hook-generators.base_gen.py` and of course, the `__init__.py` file in the generators pacakge.

## Dependencies
- Pyinstaller
- py2app
- Tkinter
- Python 2.7

## Includes
The Windows build of Updater includes pre-built binaries of git and cmake for installation.
However, as these are quite old, I would recommend users to install later versions of git and cmake separately rather than relying on me to update them over time.
One important thing to keep in mind: *make sure git and cmake are added to the PATH variable on Windows!*.
Otherwise, Updater won't be able to call them.

## Known issues
I recommend installing python from the official python distribution.
Homebrew installations don't seem to work very well.
Another issue is a script to automatically setup a project in the correct directory format for future projects to be added.
Also, see the issues with OSX Sierra and pyinstaller [here](https://github.com/pyinstaller/pyinstaller/issues/1350).
The fix for this is to actually just use py2app instead, which seems to create a standalone executable just fine.
Instructions for using py2app are available [here](https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file)
Yet another issue is the recursive nature of updater; currently updater cannot be used to build itself.
This is likely an issue with paths, namely the binary not having the relevant directories in its own path at the build time of updater.
There is also an issue with building Updater configured projects. Due to issues between the sys.path variable in python and Updater's implementation, it is currently only possible to build one project at a time. To build another project, quit Updater and restart it again specifying the directory of the other project.

## Missing features
- A HTTP service for querying available projects hosted on github.bath.ac.uk
- A method for ensuring all dependencies are accounted for.
This might take the form of simply maintaing the script to account for all dependencies that future projects need.
This would get a little cumbersome though, so best to look for an alternative solution


## TODO
- Modify the template engine to actually load the keys etc. from a config file already placed in the target directory. Then the project chooser can choose a directory containing a config file, and build from there. It will create a project if a CMakeLists.txt file is not found, and will update a project if one is found
- I need to fix the experience of the unity template. Unity always creates a new folder for a project with the name of the project as the root directory, rather than just using the folder chosen by the user. I need to get Unity to choose the current existing folder chosen
- At the moment, the template header is removed simply by removing the first 7 lines from the template. This should be fixed to accommodate headers of arbitrary length
