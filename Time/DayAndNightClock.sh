#!/bin/bash

# <xbar.title>DayAndNightClock</xbar.title>
# <xbar.version>v1.0</xbar.version>
# <xbar.author>FusionX</xbar.author>
# <xbar.author.github>FusionX13</xbar.author.github>
# <xbar.desc>A clock that can do many things.</xbar.desc>
# <xbar.image>https://i.ibb.co/6YQYS0k/Screen-Shot-2020-04-24-at-11-38-18-AM.png</xbar.image>
# <xbar.dependencies>bash</bitbar.dependencies>
# <xbar.abouturl>https://github.com/FusionX13/</xbar.abouturl>

# Gets Emoji Moon
get_phase_day () {
  local lp=2551443
  local now=$(date -ju +"%s")
  local newmoon=592500
  local phase=$((($now - $newmoon) % $lp))
  echo $(((phase / 86400) + 1))
}

# Gets Emoji Moon
get_moon_icon () {
  local phase_number=$(get_phase_day)
  # Multiply by 100000 so we can do integer comparison.  Go Bash!
  local phase_number_biggened=$((phase_number * 100000))

  if   [ $phase_number_biggened -lt 184566 ];  then date "+%l:%M:%S %p 🌑"  # new
  elif [ $phase_number_biggened -lt 553699 ];  then date "+%l:%M:%S %p 🌒"  # waxing crescent
  elif [ $phase_number_biggened -lt 922831 ];  then date "+%l:%M:%S %p 🌓"  # first quarter
  elif [ $phase_number_biggened -lt 1291963 ]; then date "+%l:%M:%S %p 🌔"  # waxing gibbous
  elif [ $phase_number_biggened -lt 1661096 ]; then date "+%l:%M:%S %p 🌕"  # full
  elif [ $phase_number_biggened -lt 2030228 ]; then date "+%l:%M:%S %p 🌖"  # waning gibbous
  elif [ $phase_number_biggened -lt 2399361 ]; then date "+%l:%M:%S %p 🌗"  # last quarter
  elif [ $phase_number_biggened -lt 2768493 ]; then date "+%l:%M:%S %p 🌘"  # waning crescent
  else                                     date "+%l:%M:%S %p 🌑"  # new
  fi
}

# Determines what time it is and what to show
H=$(date +%H)
if (( 6 <= 10#$H && 10#$H < 12 )); then
    date "+%l:%M:%S %p ☀️⇡"
elif (( 13 <= 16#$H && 10#$H < 16 )); then
    date "+%l:%M:%S %p ☀️⇣"
elif (( 13 <= 10#$H && 10#$H < 23 )); then
    get_moon_icon
else  
    get_moon_icon
fi

echo "---"
font="Monaco"
color="yellow"

# The month, date, and year
date "+%b-%d-%Y"

# Determines what time it is and what to show for a nice greeting
H=$(date +%H)
if (( 8 <= 10#$H && 10#$H < 12 )); then
    echo Good Morning
elif (( 13 <= 16#$H && 10#$H < 16 )); then
    echo Good Afternoon
elif (( 13 <= 10#$H && 10#$H < 23 )); then
    echo Good Evening
else
    echo Good Night
fi

echo "---"
font="Monaco"
color="yellow"

# Calendar script
cal |awk 'NF'|while IFS= read -r i; do echo " $i"|perl -pe '$b="\b";s/ _$b(\d)_$b(\d) /(\1\2)/' |perl -pe '$b="\b";s/_$b _$b(\d) /(\1)/' |sed 's/ *$//' |sed "s/$/|trim=false font=$font color=$color/"; done


echo "---"
font="Monaco"
color="yellow"

# Change your name
echo "Hello User"
font="Monaco"
color="yellow"
