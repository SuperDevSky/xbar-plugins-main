#!/bin/bash

# <xbar.title>Screen Lock</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Chris Tomkins-Tinch</xbar.author>
# <xbar.author.github>tomkinsc</xbar.author.github>
# <xbar.desc>This plugin displays a menu with an item to lock the screen with one click (lock or login screen).</xbar.desc>
# <xbar.image>https://cloud.githubusercontent.com/assets/53064/12120421/e515718c-b39e-11e5-830b-bebe1c6445fc.png</xbar.image>
# <xbar.dependencies></xbar.dependencies>

if [ "$1" = 'lock' ]; then
  OSVER=$(sw_vers -productVersion | awk -F. '{print $1}')
  if [[ "$OSVER" -ge 13 ]]; then
    # The first time you run this will prompt to grant xbar access in the Accessibility features settings.
    osascript -e 'tell app "System Events" to key code 12 using {control down, command down}'
  else
    # To perform a sleep action
    # Requires "password after sleep or screen saver begins" to be set in Security preferences
    #osascript -e 'tell application "Finder" to sleep'

    # To perform a lock (login screen) action
    # Requires "Fast User Switching" to be enabled in system Login preferences
    /System/Library/CoreServices/Menu\ Extras/User.menu/Contents/Resources/CGSession -suspend
  fi

  exit
fi

echo "🔒"
echo '---'
echo "Lock Now | bash='$0' param1=lock terminal=false"
