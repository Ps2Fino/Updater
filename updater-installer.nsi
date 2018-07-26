##                                                                               ##
# Updater installer for Windows                                                   #
# Installs dependencies and the application itself                                #
##                                                                               ##
## @author Daniel J. Finnegan                                                    ##
## @date September 2017                                                          ##
##                                                                               ##

!define COMPANY_NAME "Lancophone"
!define APP_NAME "Updater"

!define REGUNINSTKEY "${COMPANY_NAME}_${PRODUCT_NAME}"
!define REGSTARTMENUKEY "${COMPANY_NAME}_${PRODUCT_NAME}"
!define REGHKEY HKLM
!define REGPATH_UNINSTALL "Software\Microsoft\Windows\CurrentVersion\Uninstall"
!define UNINSTALLER_NAME "Updater-Uninstaller"

# Installation directory settings
InstallDir "$PROGRAMFILES\${COMPANY_NAME}\${PRODUCT_NAME}"
InstallDirRegKey "${REGHKEY}" "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" "InstallLocation"

RequestExecutionLevel admin # Require admin rights on NT6+ (When UAC is turned on)
Name "Updater"
ShowInstDetails show # Show the installer details by default

##                     ##
# Program Variables     #

Var StartMenuFolder

##                     ##
# Modern UI definitions #

!include "MUI2.nsh"
!include "FileFunc.nsh" # Needed for estimating file size

!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE 'LICENSE'
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY

;Start Menu Folder Page Configuration
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "${REGHKEY}" 
!define MUI_STARTMENUPAGE_REGISTRY_KEY "Software\${REGSTARTMENUKEY}" 
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"

!insertmacro MUI_PAGE_STARTMENU Application $StartMenuFolder

!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

# Uninstall pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

##         ##
# Languages #

!insertmacro MUI_LANGUAGE "English"

##         ##
# Functions #

# Mutex check for multiple instances of installer running concurrently
Function .onInit
	System::Call 'kernel32::CreateMutex(i 0, i 0, t "${COMPANY_NAME}:${APP_NAME}") ?e'
	Pop $R0
	StrCmp $R0 0 +3
		MessageBox MB_OK "The installer is already running."
		Abort
FunctionEnd

##        ##
# Sections #

!if /FileExists ".\dependencies\cmake.msi"

# Install CMake
Section /o "Install CMake" cmake_install
	SetOutPath "$INSTDIR\dependencies"
	DetailPrint "Booting the cmake installer..."
	File ".\dependencies\cmake.msi"
	ExecWait 'msiexec /i "$INSTDIR\dependencies\cmake.msi"'
SectionEnd
!endif

!if /FileExists ".\dependencies\git.exe"

Section /o "Install Git" git_install
	SetOutPath "$INSTDIR\dependencies"
	DetailPrint "Booting the git installer..."
	File ".\dependencies\git.exe"
	ExecWait '$INSTDIR\dependencies\git.exe'
SectionEnd

!endif

Section "Install Updater" updater_install
	SetOutPath "$INSTDIR"
	WriteUninstaller $INSTDIR\${UNINSTALLER_NAME}.exe
	DetailPrint "Installing Updater and its dependencies..."
	File /r updater\templates
	File /r updater\scripts
	File /r updater\generators
	File ".\updater\dist\updater.exe"

	# Write registry keys for uninstallation and Add/Remove Control Panel access
	WriteRegStr ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" \
	"DisplayName" "${APP_NAME} -- cmake template engine"
	WriteRegStr ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" \
	"InstallLocation" "$\"$INSTDIR$\""
	WriteRegStr ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" \
	"UninstallString" "$\"$INSTDIR\${UNINSTALLER_NAME}.exe$\""
	WriteRegStr ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" \
	"Publisher" "${COMPANY_NAME}"

	!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
    
    	;Create shortcuts
    	CreateDirectory "$SMPROGRAMS\$StartMenuFolder"
    	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\Updater.lnk" "$INSTDIR\updater.exe"
    	CreateShortcut "$SMPROGRAMS\$StartMenuFolder\${UNINSTALLER_NAME}.lnk" "$INSTDIR\${UNINSTALLER_NAME}.exe"
  
	!insertmacro MUI_STARTMENU_WRITE_END

	# Write the estimated size
	${GetSize} "$INSTDIR" "/S=0K" $0 $1 $2
	IntFmt $0 "0x%08X" $0
	WriteRegDWORD ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}" \
	"EstimatedSize" "$0"
SectionEnd

Section "Uninstall"
	Delete "$INSTDIR\${UNINSTALLER_NAME}.exe" # works because uninstaller is copied to system temp folder
	Delete "$INSTDIR\updater.exe"
	RMDir /r "$INSTDIR\scripts"
	RMDir /r "$INSTDIR\templates"
	RMDir /r "$INSTDIR\generators"
	RMDir $INSTDIR
	DeleteRegKey ${REGHKEY} "${REGPATH_UNINSTALL}\${REGUNINSTKEY}"

	# Delete the start menu bit
	!insertmacro MUI_STARTMENU_GETFOLDER Application $StartMenuFolder
	Delete "$SMPROGRAMS\$StartMenuFolder\${UNINSTALLER_NAME}.lnk"
	Delete "$SMPROGRAMS\$StartMenuFolder\Updater.lnk"
	RMDir "$SMPROGRAMS\$StartMenuFolder"
	DeleteRegKey /ifempty ${REGHKEY} "Software\${REGSTARTMENUKEY}"
SectionEnd

##                                 ##
# Set descriptions for each section #

LangString DESC_cmake_install ${LANG_ENGLISH} "Launches the CMake installer. For Updater to work, CMake needs to be callable from powershell/cmd. Ensure that CMake is added to your PATH variable."

LangString DESC_git_install ${LANG_ENGLISH} "Launches the git installer. Git is needed to pull down project source code from remote repositories. Ensure that git is added to your PATH variable."

LangString DESC_updater_install ${LANG_ENGLISH} "Installs Updater."

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN

!if /FileExists ".\dependencies\cmake.msi"
  !insertmacro MUI_DESCRIPTION_TEXT ${cmake_install} $(DESC_cmake_install)
!endif

!if /FileExists ".\dependencies\git.exe"
  !insertmacro MUI_DESCRIPTION_TEXT ${git_install} $(DESC_git_install)
!endif

  !insertmacro MUI_DESCRIPTION_TEXT ${updater_install} $(DESC_updater_install)
!insertmacro MUI_FUNCTION_DESCRIPTION_END
####################################################

## TODO: Add Uninstaller
## TODO: Add the generators to the actual source code, not as a zipped dependency