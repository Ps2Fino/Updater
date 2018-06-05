# FMOD
# This module helps find FMOD installation.
#
# @author Daniel J. Finnegan
# @date October 2017

find_path ( # FMOD header
	FMOD_INCLUDE_DIRS
	NAMES
		fmod.h
		fmod.hpp
	PATHS
		"C:/Program Files (x86)/FMOD SoundSystem/FMOD Studio API Windows/api"
		"C:/Program Files/FMOD SoundSystem/FMOD Studio API Windows/api"
		"${CMAKE_SOURCE_DIR}/dependencies/FMOD Programmers API/api"
	PATH_SUFFIXES
		lowlevel/inc
		fsbank/inc
		studio/inc
	DOC
		"Directory containing FMOD headers"
)

find_path ( # FMOD library directory
	FMOD_LIBRARY_DIRS
	NAMES
		fmod.dll
		libfmod.dylib
	PATHS
		"C:/Program Files (x86)/FMOD SoundSystem/FMOD Studio API Windows/api"
		"C:/Program Files/FMOD SoundSystem/FMOD Studio API Windows/api"
		"${CMAKE_SOURCE_DIR}/dependencies/FMOD Programmers API/api"
	PATH_SUFFIXES
		lowlevel/lib
		fsbank/lib
		studio/lib
	DOC
		"Directory containing FMOD libraries"
)

if (WIN32)

	set (
		FMOD_LIB_NAMES
			fmod_vc
			fmod64_vc
			fmodL64_vc
	)

elseif (APPLE)

	set (
		FMOD_LIB_NAMES
			fmod
			fmodL
	)

endif ()

set (
	FMOD_LIBS
		""
)

foreach (FMOD_LIB ${FMOD_LIB_NAMES})

	find_library (
		FOUND_LIB_${FMOD_LIB}
		${FMOD_LIB}
		PATHS
			"C:/Program Files (x86)/FMOD SoundSystem/FMOD Studio API Windows/api"
			"C:/Program Files/FMOD SoundSystem/FMOD Studio API Windows/api"
			"${CMAKE_SOURCE_DIR}/dependencies/FMOD Programmers API/api"
		PATH_SUFFIXES
			lowlevel/lib
			fsbank/lib
			studio/lib
	)

	list (
		APPEND
			FMOD_LIBS
				${FOUND_LIB_${FMOD_LIB}}
	)

	mark_as_advanced (
		${FOUND_LIB_${FMOD_LIB}}
	)

endforeach ()

include (
	FindPackageHandleStandardArgs
)

find_package_handle_standard_args (
	fmod
	FOUND_VAR
		fmod_FOUND
	REQUIRED_VARS
		FMOD_LIBS
		FMOD_INCLUDE_DIRS
		FMOD_LIBRARY_DIRS
	FAIL_MESSAGE
		"Couldn't find fmod."
)

mark_as_advanced (
	FMOD_LIB_NAMES
	FMOD_LIBS
)

set (
	FMOD_LIBRARIES
		${FMOD_LIBS}
)

########################################