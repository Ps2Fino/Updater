# fftw
# On Windows, this project ships with the prebuilt libs.
# Therefore, on Windows, the directory is simply setup.
# On different systems, the installed copy of fftw will be searched for
#
# @author Daniel J. Finnegan
# @date October 2017

include (
	FindPackageHandleStandardArgs
)

if (WIN32)

	set (
		FFTW_INCLUDE_DIRS
			${FFTW_GENERATED_DIR}/include
	)

	set (
		FFTW_LIBRARY_DIRS
			${FFTW_GENERATED_DIR}/lib
	)

	set (
		FFTW_LIBRARIES
			${FFTW_LIBRARY_DIRS}/libfftw3-3.lib
			${FFTW_LIBRARY_DIRS}/libfftw3f-3.lib
			${FFTW_LIBRARY_DIRS}/libfftw3l-3.lib
	)

	# Set the bin directory too for actually running 
	# in the debugger
	set (
		FFTW_BIN_DIRS
			${FFTW_LIBRARY_DIRS}
	)

	find_package_handle_standard_args (
		fftw
		FOUND_VAR
			fftw_FOUND
		REQUIRED_VARS
			FFTW_INCLUDE_DIRS
			FFTW_LIBRARY_DIRS
			FFTW_LIBRARIES
		FAIL_MESSAGE
			"Couldn't find fftw."
	)

else ()

	# For OSX, just piggyback onto pkg-config

	find_package (PkgConfig)
	pkg_check_modules (
		PC_FFTW
		QUIET
		fftw3
	)

	find_path (
		FFTW_INCLUDE_DIRS
		NAMES
			fftw3.h
			fftw3.hpp
		HINTS
			${PC_FFTW_INCLUDEDIR}
			${PC_FFTW_INCLUDE_DIRS}
		PATHS
			/usr/local/include
			/usr/local/Cellar/fftw/include # I advocate homebrew...
	)

	find_path (
		FFTW_LIBRARY_DIRS
		NAMES
			libfftw3.dylib
			libfftw3.so
			libfftw3.a
		HINTS
			${PC_FFTW_LIBRARYDIR}
			${PC_FFTW_LIBRARY_DIRS}
		PATHS
			/usr/local/lib
			/usr/local/Cellar/fftw/lib
	)

	if (APPLE)

		set (
			FFTW_LIB_NAMES
				fftw3
				fftw3f
				fftw3l
		)

		set (
			FFTW_LIBS
				""
		)

		foreach (FFTW_LIB ${FFTW_LIB_NAMES})

			find_library (
				FOUND_LIB_${FFTW_LIB}
				${FFTW_LIB}
				PATHS
					/usr/local/lib
					/usr/local/Cellar/fftw/lib
				HINTS
					${PC_FFTW_LIBRARYDIR}
					${PC_FFTW_LIBRARY_DIRS}
			)

			list (
				APPEND
					FFTW_LIBS
						${FOUND_LIB_${FFTW_LIB}}
			)

		endforeach ()

	else ()

		find_library (
			FOUND_LIB_FFTW
			fftw3
			PATHS
				/usr/local/lib
				/usr/local/Cellar/fftw/lib
			HINTS
				${PC_FFTW_LIBRARYDIR}
				${PC_FFTW_LIBRARY_DIRS}
		)

		set (
			FFTW_LIBS
			FOUND_LIB_FFTW
		)

	endif ()



	find_package_handle_standard_args (
		fftw
		FOUND_VAR
			fftw_FOUND
		REQUIRED_VARS
			FFTW_INCLUDE_DIRS
			FFTW_LIBRARY_DIRS
			FFTW_LIBS
		FAIL_MESSAGE
			"Couldn't find fftw."
	)

	mark_as_advanced (
		FFTW_LIBS
	)

	if (PC_FFTW_FOUND)

		set (
			FFTW_LIBRARIES
				${PC_FFTW_LDFLAGS}
		)

	else ()

		set (
			FFTW_LIBRARIES
				${FFTW_LIBS}
		)

	endif ()

endif ()

########################################