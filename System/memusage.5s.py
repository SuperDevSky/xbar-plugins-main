#!/usr/bin/env python3

# <xbar.title>Memory usage</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Gautam krishna R</xbar.author>
# <xbar.author.github>gautamkrishnar</xbar.author.github>
# <xbar.desc>Shows the current system memmory usage.</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.abouturl>https://github.com/matryer/bitbar-plugins/blob/master/System/memusage.5s.py</xbar.abouturl>

import subprocess
import re

# Get process info
ps = subprocess.Popen(['ps', '-caxm', '-orss,comm'], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")
vm = subprocess.Popen(['vm_stat'], stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

# Iterate processes
processLines = ps.split('\n')
sep = re.compile('[\s]+')
rssTotal = 0 # kB
for row in range(1,len(processLines)):
    rowText = processLines[row].strip()
    rowElements = sep.split(rowText)
    try:
        rss = float(rowElements[0]) * 1024
    except:
        rss = 0 # ignore...
    rssTotal += rss

# Process vm_stat
vmLines = vm.split('\n')
sep = re.compile(':[\s]+')
vmStats = {}
for row in range(1,len(vmLines)-2):
    rowText = vmLines[row].strip()
    rowElements = sep.split(rowText)
    vmStats[(rowElements[0])] = int(rowElements[1].strip('\.')) * 4096

print('Wired Memory:\t\t%d MB' % ( vmStats["Pages wired down"]/1024/1024 ))
print('Active Memory:\t\t%d MB' % ( vmStats["Pages active"]/1024/1024 ))
print('Inactive Memory:\t%d MB' % ( vmStats["Pages inactive"]/1024/1024 ))
print('Free Memory:\t\t%d MB' % ( vmStats["Pages free"]/1024/1024 ))
print('Real Mem Total (ps):\t%.3f MB' % ( rssTotal/1024/1024 ))
