# Updater
A build utility/package manager that presents a GUI for easy, cross platform installation of my software

## Dependencies
- Pyinstaller
- Tkinter
- Python 2.7

## Known issues
I recommend installing python from the official python distribution.
Homebrew installations don't seem to work very well.
Another issue is a script to automatically setup a project in the correct directory format for future projects to be added.
Yet another issue is the recursive nature of updater; currently updater cannot be used to build itself.
This is likely an issue with paths, namely the binary not having the relevant directories in its own path at the build time of updater.

## Missing features
- A HTTP service for querying available projects hosted on github.bath.ac.uk
- A method for ensuring all dependencies are accounted for.
This might take the form of simply maintaing the script to account for all dependencies that future projects need.
This would get a little cumbersome though, so best to look for an alternative solution
