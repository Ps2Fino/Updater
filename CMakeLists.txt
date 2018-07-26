##
## Updater -- a cmake based template engine 
##
## @author Daniel J. Finnegan
##

cmake_minimum_required (VERSION 2.8)
cmake_policy (SET CMP0048 NEW)

project (
	Updater
	VERSION
		1.5.1
	LANGUAGES
		NONE
)

## Gather the version number and create the installer name from it
set (
	INSTALLER_NAME
	${PROJECT_NAME}_v${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}
)

if (WIN32) # We only support Windows for now

# Note that the version number and product name are passed to the NSIS script
add_custom_target (
	updater
	ALL
	COMMAND
		"C:/Program Files (x86)/NSIS/makensis.exe"
		"/XOutFile ${CMAKE_SOURCE_DIR}/${INSTALLER_NAME}.exe"
		"/X!define PRODUCT_NAME ${PROJECT_NAME}"
		${CMAKE_SOURCE_DIR}/updater-installer.nsi
	COMMENT
		"Building Updater..."
)

else () # Just echo a statement on any other system

add_custom_target (
	updater
	ALL
	COMMAND
		echo "Only supported on Windows, soz!"
)

endif()