#!/bin/bash
# This script is used with BitBar for uRad Monitor

# <xbar.title>uRadMonitor view</xbar.title>
# <xbar.version>v1.2</xbar.version>
# <xbar.author>Martin LBB</xbar.author>
# <xbar.author.github>martinlbb</xbar.author.github>
# <xbar.desc>Extract radiation value from uRadMonitor and show it.</xbar.desc>
# <xbar.dependencies>curl,grep,egrep,sed, bc</xbar.dependencies>
# <xbar.image>https://user-images.githubusercontent.com/4921816/33482707-a26cf0e6-d69a-11e7-8b72-f9c389f24bc6.png</xbar.image>

IP="192.168.0.251"

#Script begin here
#Retrieve value from uRad device
uradhtml=$(curl -s http://$IP)


#Determine detector and ratio for uSv
if echo "$uradhtml" | grep -q "SBM20"; then
  ratio=0.006315
  detector="SBM20"
elif echo "$uradhtml" | grep -q "SI29BG"; then
  ratio=0.010000
  detector="SI29BG"
elif echo "$uradhtml" | grep -q "SBM19"; then
  ratio=0.001500
  detector="SBM19"
elif echo "$uradhtml" | grep -q "STS5"; then
  ratio=0.006666
  detector="STS5"
elif echo "$uradhtml" | grep -q "SI22G"; then
  ratio=0.001714
  detector="SI22G"
elif echo "$uradhtml" | grep -q "SI3BG"; then
  ratio=0.631578
  detector="SI3BG"
elif echo "$uradhtml" | grep -q "SBM21"; then
  ratio=0.048000
  detector="SBM21"
elif echo "$uradhtml" | grep -q "LND712"; then
  ratio=0.005940
  detector="LND712"
elif echo "$uradhtml" | grep -q "SBT9"; then
  ratio=0.010900
  detector="SBT9"
elif echo "$uradhtml" | grep -q "SI1G"; then
  ratio=0.006000
  detector="SI1G"
fi

#Get latest CPM
cpm=$(echo "$uradhtml" | grep -o "radiation:[0-9]*CPM" | egrep -o '[0-9]{1,9}')

#Get average CPM
avgcpm=$(echo "$uradhtml" | grep -o "average:[0-9].*CPM" | egrep -o "[0-9]{1,9}.[0-9]{2}")

#Get Temperature (Degree Only today)
temp=$(echo "$uradhtml" | grep -o "temperature:[0-9].*C" | egrep -o "[0-9]{1,3}.[0-9]{2}")

#Get Unit number
unit=$(echo "$uradhtml" | grep -o "uRADMonitor [0-9]*" | egrep -o "[0-9]{8,9}")

#Get voltage
volt=$(echo "$uradhtml" | grep -o "voltage:[0-9]*V" | egrep -o "[0-9]{1,4}")

#Compute uSiverts
#usv=$(echo "$ratio*$cpm" | bc | sed 's/\./\,/g' | sed 's/^\,/0,/')
usv=$(echo "$ratio*$cpm" | bc | sed 's/^\./0./')

#Determine color based on actual radiation
#Color taken form uRad Website
if (( $(echo "$usv < 0.03" |bc -l) )); then
   color="#00ff00"
elif (( $(echo "$usv < 0.06" |bc -l) )); then
   color="#33ff00"
elif (( $(echo "$usv < 0.09" |bc -l) )); then
   color="#66ff00"
elif (( $(echo "$usv < 0.12" |bc -l) )); then
   color="#99ff00"
elif (( $(echo "$usv < 0.15" |bc -l) )); then
   color="#ccff00"
elif (( $(echo "$usv < 0.18" |bc -l) )); then
   color="#ffff00"
elif (( $(echo "$usv < 0.21" |bc -l) )); then
   color="#ffcc00"
elif (( $(echo "$usv < 0.24" |bc -l) )); then
   color="#ff9900"
elif (( $(echo "$usv < 0.27" |bc -l) )); then
   color="#ff6600"
else
   color="#ff3300"
fi


#Display all values
printf '%3.2f µSv/h | color=%s\n' "$usv" "$color"

#If you enable following values, BitBar will show several values
echo "---"
printf '%s CPM\n' "$cpm"
printf '%s CPM (avg)\n' "$avgcpm"
printf '%s °C\n' "$temp"
echo "---"
printf 'Unit %s | bash='/usr/bin/open' param1="https://www.uradmonitor.com/?open=%s" terminal=false\n' "$unit" "$unit"
printf '%s (%s V)\n' "$detector" "$volt"

