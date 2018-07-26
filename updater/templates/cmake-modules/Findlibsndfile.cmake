# libsndfile
# This module helps find the libsndfile installation.
#
# @author Daniel J. Finnegan
# @date November 2017

if (WIN32)

	find_path ( # libsndfile header directory
		LSNDFILE_INCLUDE_DIRS
		NAMES
			sndfile.h
			sndfile.hh
		PATHS
			"C:/Program Files/Mega-Nerd/libsndfile/include"
			"C:/Program Files (x86)/Mega-Nerd/libsndfile/include"
			"${CMAKE_SOURCE_DIR}/dependencies/libsndfile/include"
		DOC
			"Directory containing libsndfile headers"
	)

	find_path ( # libsndfile lib directory
		LSNDFILE_LIBRARY_DIRS
		NAMES
			libsndfile-1.lib
			libsndfile.lib
		PATHS
			"C:/Program Files/Mega-Nerd/libsndfile/lib"
			"C:/Program Files (x86)/Mega-Nerd/libsndfile/lib"
			"${CMAKE_SOURCE_DIR}/dependencies/libsndfile/lib"
		DOC
			"Directory containing libsndfile libraries"
	)

	find_path ( # libsndfile binary directory
		LSNDFILE_BIN_DIRS
		NAMES
			libsndfile-1.dll
			libsndfile.dll
		PATHS
			"C:/Program Files/Mega-Nerd/libsndfile/bin"
			"C:/Program Files (x86)/Mega-Nerd/libsndfile/bin"
			"${CMAKE_SOURCE_DIR}/dependencies/libsndfile/bin"
		DOC
			"Directory containing the shared compiled library for libsndfile"
	)

	find_library (
		LSNDFILE_LIB
		NAMES
			libsndfile
			libsndfile-1
		PATHS
			${LSNDFILE_LIBRARY_DIRS}
	)

else ()

	find_package (PkgConfig)
	pkg_check_modules (
		PC_LSNDFILE
		QUIET
		sndfile
	)

	find_path (
		LSNDFILE_INCLUDE_DIRS
		NAMES
			sndfile.h
			sndfile.hh
		HINTS
			${PC_LSNDFILE_INCLUDEDIR}
			${PC_LSNDFILE_INCLUDE_DIRS}
		PATHS
			/usr/local/include
			/usr/local/Cellar/libsndfile/1.0.28/include
	)

	find_path (
		LSNDFILE_LIBRARY_DIRS
		NAMES
			libsndfile.1.dylib
			libsndfile.dylib
			libsndfile.1.so
			libsndfile.so
		HINTS
			${PC_LSNDFILE_LIBRARYDIR}
			${PC_LSNDFILE_LIBRARY_DIRS}
		PATHS
			/usr/local/lib
			/usr/local/Cellar/libsndfile/1.0.28/lib
	)

	find_library (
		LSNDFILE_LIB
		NAMES
			sndfile
			sndfile.1
		PATHS
			${LSNDFILE_LIBRARY_DIRS}
	)

endif ()



include (
	FindPackageHandleStandardArgs
)

if (WIN32)

	find_package_handle_standard_args (
		libsndfile
		FOUND_VAR
			libsndfile_FOUND
		REQUIRED_VARS
			LSNDFILE_INCLUDE_DIRS
			LSNDFILE_LIBRARY_DIRS
			LSNDFILE_BIN_DIRS
			LSNDFILE_LIB
		FAIL_MESSAGE
			"Couldn't find libsndfile."
	)

else ()

	find_package_handle_standard_args (
		libsndfile
		FOUND_VAR
			libsndfile_FOUND
		REQUIRED_VARS
			LSNDFILE_INCLUDE_DIRS
			LSNDFILE_LIBRARY_DIRS
			LSNDFILE_LIB
		FAIL_MESSAGE
			"Couldn't find libsndfile."
	)

endif ()

########################################