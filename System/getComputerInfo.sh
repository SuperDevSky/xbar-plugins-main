#!/bin/bash

# <xbar.title>Get Computer Info</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>Sarah Keenan</xbar.author>
# <xbar.author.github>SKeenan07</xbar.author.github>
# <xbar.desc>This plugin gets the IP address and the computer name.</xbar.desc>
# <xbar.image>https://github-production-user-asset-6210df.s3.amazonaws.com/5545555/239567139-d0546624-25e9-4630-9ab6-1e42cf77861f.png</xbar.image>

activeNetworkAdapter=$(echo 'show State:/Network/Global/IPv4' | scutil | grep PrimaryInterface | awk -F " . " '{ print $2 }')

computerName=$(system_profiler SPSoftwareDataType | grep "Computer Name")

batteryCondition=$(system_profiler SPPowerDataType | grep "Condition")

echo "🖥"

echo "---"

echo "${computerName:21}"

echo "---"

# Batery conditions can be Normal, Replace Soon, Replace Now, and Service Battery
echo "Battery Condition: ${batteryCondition:21}"

echo "---"

# If the active network adapter is empty, then the Mac isn't connected to the internet
if [[ -z "$activeNetworkAdapter" ]]; then
    echo "Not connected to the internet."
else
    IPAddress=$(ifconfig "$activeNetworkAdapter" | grep "inet " | awk '{ print $2 }')
    echo "$IPAddress"
fi
