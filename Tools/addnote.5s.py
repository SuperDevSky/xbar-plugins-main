#!/usr/bin/env python3

# <xbar.title>Add Note</xbar.title>
# <xbar.author>Frak Nuaimy</xbar.author>
# <xbar.author.github>frakman1</xbar.author.github>
# <xbar.image>http://i.imgur.com/608LQ25.png</xbar.image>
# <xbar.desc>Add a note to Apple Notes app.</xbar.desc>
# <xbar.dependencies>python</xbar.dependencies>
# <xbar.version>v1.1</xbar.version>

import os, sys
import argparse
import subprocess
import shlex

def run_script(script):
    return (subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0].strip()).decode("utf-8").replace("'", "’")

def run_script2(script):
    return (subprocess.Popen([script], stdout=subprocess.PIPE, shell=True).communicate()[0])

fullPathFileName = os.path.realpath(__file__)


parser = argparse.ArgumentParser()
parser.add_argument('-n', action='store', dest='localnote', help='Create Note Flag')
results = parser.parse_args()


if(len(sys.argv) >= 2):
    if (sys.argv[1] == "-n"):
        cmd = "osascript -e \'set theString to text returned of (display dialog \"Please Enter The Note To Add \" with icon note default answer \"\n\n\n\" buttons {\"OK\",\"Cancel\"} default button 1) \'"
        note = run_script(cmd)
        if len(note) == 0:
             sys.exit(1)
        if "\n" in note:
            i = note.index('\n')
            header = note.splitlines(True)[0]
            body = note[i+1:]
        else:
            header = note
            body = ""
        cmd2 = "osascript -e 'tell application \"Notes\" \n tell account \"iCloud\" \n make new note at folder \"Notes\" with properties {name:\"%s\", body:\"%s\"} \n end tell \n end tell'" % (header, body)
        run_script2(cmd2)
        sys.exit(1)

print("📔")
print("---")
print("Add Note | trim=false color=yellow bash=" + shlex.quote(fullPathFileName) +  " param1=-n param2=null terminal=false refresh=true")
