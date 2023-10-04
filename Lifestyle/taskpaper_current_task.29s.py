#!/usr/bin/python
# -*- coding: utf-8 -*-

#
# <xbar.title>Taskpaper Current Task</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Marcin Biegun</xbar.author>
# <xbar.author.github>marcinbiegun</xbar.author.github>
# <xbar.desc>This plugin will display first task in your file having the specified tag</xbar.desc>
# <xbar.image>https://i.imgur.com/2I3eU0D.png</xbar.image>
# <xbar.dependencies>python</xbar.dependencies>
#

import os
import re
import sys

taskpaper_file = '~/todo.taskpaper'
tag = 'now'
emoji_prefix = '🍅'

try:
    file = open(os.path.expanduser(taskpaper_file), 'r')
except IOError:
    sys.stdout.write('Taskpaper File Not Found\n---\n'
                     + 'Currently selected file is %s\n' % taskpaper_file
                     + 'To select a different file, edit %s|href=file://%s\n'
                     % (sys.argv[0], sys.argv[0]))
    sys.exit(1)

item = ''

for line in file:

    # Save header (e.g. "Work:")
    if line.endswith(':\n'):
        header = line.strip()[:-1]

    # Find line containing the tag but not @done
    elif ' @%s' % tag in line and ' @done' not in line:
        # Remove all tags
        # Remove dash
        # Remove whitespace
        item += '%s (%s)\n' % (re.sub(' @%s ?' %
                                      tag, ' ', line).strip()[2:], header)
        break

file.close()

if item != '':
    if emoji_prefix != '':
        item = emoji_prefix + ' ' + item
    sys.stdout.write(item)
