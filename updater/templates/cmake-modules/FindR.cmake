# FindR.cmake
#
# This module tries to find the R installation path
# Specifically, it searches for the path to the bin directory of the R executable.
# Note that it will do its best, but it expects R to be installed somewhere in the C drive
#
# @author Daniel J. Finnegan
# @date March 2018

# Be good to the environment!
if (NOT DEFINED R_HOME)

	if (WIN32)

		file (
			GLOB_RECURSE
			R_EXE_PATH
			"C:/Program Files/R/R.exe"
		)

	else ()

		file (
			GLOB_RECURSE
			R_EXE_PATH
			"/usr/bin/*R"
		)

	endif ()

	foreach (
		file_path
		${R_EXE_PATH}
	)

		get_filename_component (
			path_comp
			${file_path}
			DIRECTORY
		)

		if (WIN32)

			find_path (
				R_BIN_DIR
				NAMES
					R.exe
					Rscript.exe
				PATHS
					${path_comp}
				DOC
					"Directory containing the R executable"
			)

		else ()

			find_path (
				R_BIN_DIR
				NAMES
					R
					Rscript
				PATHS
					${path_comp}
				DOC
					"Directory containing the R executable"
			)

		endif ()

		if (R_BIN_DIR-FOUND)

			break ()

		endif ()

	endforeach ()

	if (WIN32)

		find_program (
			R_EXECUTABLE
				R.exe
			PATHS
				${R_BIN_DIR}
		)

		find_program (
			RSCRIPT_EXECUTABLE
				Rscript.exe
			PATHS
				${R_BIN_DIR}
		)

	else ()

		find_program (
			R_EXECUTABLE
				R
			PATHS
				${R_BIN_DIR}
		)

		find_program (
			RSCRIPT_EXECUTABLE
				Rscript
			PATHS
				${R_BIN_DIR}
		)

	endif ()

	get_filename_component (
		R_HOME
		${R_BIN_DIR}
		DIRECTORY
	)

	set (
		R_HOME
		${R_HOME}
		CACHE
		PATH
		"Path to the R home directory"
	)

	include (
		FindPackageHandleStandardArgs
	)

	# This command automatically sets the cache variables too, which is useful
	find_package_handle_standard_args (
		R_HOME
		FOUND_VAR
			R_HOME_FOUND
		REQUIRED_VARS
			R_HOME
			R_BIN_DIR
			R_EXECUTABLE
			RSCRIPT_EXECUTABLE
		FAIL_MESSAGE
			"Couldn't find R."
	)

endif ()

########################################