#!/usr/bin/env bash
#
# <xbar.title>Ejector</xbar.title>
# <xbar.version>v1.2</xbar.version>
# <xbar.author>Carlson Orozco && Brian Hartvigsen && Matt Sephton</xbar.author>
# <xbar.author.github>carlsonorozco</xbar.author.github>
# <xbar.desc>Ejector is a plugin for BitBar that enables you to eject all mounted disk / drive / installers / USB connected drives and volumes instantly.</xbar.desc>
# <xbar.image>https://raw.githubusercontent.com/carlsonorozco/ejector/master/image.png</xbar.image>
# <xbar.abouturl>https://github.com/carlsonorozco/ejector</xbar.abouturl>


mapfile -t drives < <(df -Hl | grep /Volumes/ | grep -v "/System/Volumes/Data"| grep -v "/System/Volumes/VM" | grep -v "/System/Volumes/Preboot" | grep -v "/System/Volumes/Update" | grep -v "/Volumes/Recovery" | sed 's/.*\/Volumes\/*//')

IFS=$'**********'
for details in $( diskutil info -all ); do
    mapfile -t -O "${#drives[@]}" drives <  <(echo "$details" | grep -A1000 "Device Node" | grep -B1000 "Mounted:[[:space:]]*No$" | grep "Volume Name" | grep -v "Boot\|Backup\|Macintosh\|EFI\|Preboot\|Recovery" | awk '{print $3}')
done

if [ "$1" = 'eject' ]; then
    status=$(diskutil eject "$2" | sed -e 's/\/Volumes\///g')
    if [ "$status" = "" ]; then
        osascript -e "display notification \"Disk $2 failed to eject\" with title \"Ejector\""
    else
        osascript -e "display notification \"$status\" with title \"Ejector\""
    fi

    exit
fi

if [ "$1" = 'mount' ]; then
    status=$(diskutil mount "$2")
    if [ "$status" = "" ]; then
        osascript -e "display notification \"Disk $2 failed to mount\" with title \"Ejector\""
    else
        osascript -e "display notification \"$status\" with title \"Ejector\""
    fi

    exit
fi

if [ "$1" = 'unmount' ]; then
    status=$(diskutil unmount "$2")
    if [ "$status" = "" ]; then
        osascript -e "display notification \"Disk $2 failed to unmount\" with title \"Ejector\""
    else
        osascript -e "display notification \"$status\" with title \"Ejector\""
    fi

    exit
fi

if [ "$1" = 'ejectall' ]; then
    if [ -z "$2" ]; then
        osascript -e '
        try
            tell application "Finder"
                eject the disks
                display notification "Successfully ejected disks." with title "Ejector"
            end tell
        on error
            display notification "Unable to eject all disks." with title "Ejector"
        end try'

        exit
    fi

    protocol_type=$2
    protocol_type="${protocol_type/dmgs/Disk Image}"
    protocol_type="${protocol_type/usbs/USB}"

    IFS=$'**********'
    for details in $( diskutil info -all ); do
        name=$(echo "$details" | grep "Volume Name:" | sed 's/.*Volume Name:[[:space:]]*//')
        ! [[ ${drives[*]} =~ $name ]] && continue
        protocol=$(echo "$details" | grep "Protocol:" | sed 's/.*Protocol:[[:space:]]*//')
        mount_point=$(echo "$details" | grep "Mount Point:" | sed 's/.*Mount Point:[[:space:]]*//')
        [[ "$protocol_type" = "$protocol" ]] && ./"$0" eject "$mount_point"
    done
    exit
fi

total_dmg=0
total_usb=0

if [ ${#drives[@]} = 0 ]; then
    echo "⏏ | color=gray"
    exit
fi

echo "⏏"
echo '---'

IFS=$'**********'
for details in $( diskutil info -all ); do
    name=$(echo "$details" | grep "Volume Name:" | sed 's/.*Volume Name:[[:space:]]*//')
    ! [[ ${drives[*]} =~ $name ]] && continue

    device_node=$(echo "$details" | grep "Device Node:" | sed 's/.*Device Node:[[:space:]]*//')
    mount_point=$(echo "$details" | grep "Mount Point:" | sed 's/.*Mount Point:[[:space:]]*//')
    free_space=$(echo "$details" | grep -E "Volume (Available|Free) Space:" | sed 's/.*Volume Free Space:[[:space:]]*//;s/.*Volume Available Space:[[:space:]]*//' | cut -d ' ' -f -2)
    total_size=$(echo "$details" | grep -E "(Disk|Total) Size:" | sed 's/.*Total Size:[[:space:]]*//;s/.*Disk Size:[[:space:]]*//' | cut -d ' ' -f -2)
    protocol=$(echo "$details" | grep "Protocol:" | sed 's/.*Protocol:[[:space:]]*//')

    [[ $protocol = 'Disk Image' ]] && ((total_dmg++))
    [[ $protocol = 'USB' ]] && ((total_usb++))

    if [ "$mount_point" != '' ]; then
        echo "$name | bash='$0' param1=eject param2='$mount_point' terminal=false"
        echo "$name [unmount] | alternate=true bash='$0' param1=unmount param2='$mount_point' terminal=false"
        echo "├─ Available: $free_space"
        echo "└─ Capacity: $total_size"
    else
        echo "$name | bash='$0' param1=mount param2=$device_node terminal=false"
        echo "└─ Unmounted: $device_node"
    fi
done

if [ ${#drives[@]} -ge 2 ]; then
    echo '---'
    [ $((total_dmg)) -ge 2 ] && echo "Eject All Disk Images | color=red bash='$0' param1=ejectall param2=dmgs terminal=false"
    [ $((total_usb)) -ge 2 ] && echo "Eject All Physical Volumes | color=red bash='$0' param1=ejectall param2=usbs terminal=false"
    echo "Eject All | color=red bash='$0' param1=ejectall terminal=false"
fi
