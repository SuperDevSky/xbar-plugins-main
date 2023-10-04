#!/usr/bin/env python3

# <xbar.title>Quod Libet Control</xbar.title>
# <xbar.version>v1.1</xbar.version>
# <xbar.author>Sean Lane</xbar.author>
# <xbar.author.github>seanlane</xbar.author.github>
# <xbar.desc>Control Quoid Libet via Bitbar</xbar.desc>
# <xbar.image>https://i.imgur.com/VA8ZEbR.png</xbar.image>
# <xbar.dependencies>quodlibet, python</xbar.dependencies>

import os, subprocess, sys

CUR_PATH = os.path.expanduser('~/.quodlibet/current')
CONTROL_PATH = os.path.expanduser('~/.quodlibet/control')

def get_current():
  with open(CUR_PATH, 'r') as cur:
    lines = cur.readlines()
  lines = [x.strip().lstrip('~').lstrip('#').split('=', 1) 
    for x in lines]
  return {x[0]: x[1] for x in lines}

def run_cmd(cmd_in):
  if cmd_in == 'delete':
    status = get_current()
    run_cmd('next')
    if os.path.exists(status['filename']):
      subprocess.check_output('mv "{}" {}'.format(
        status['filename'], os.path.expanduser('~/.Trash/')), shell=True)
  elif cmd_in == 'menu-previous':
      run_cmd('force-previous')
  elif cmd_in == 'open-ql':
    subprocess.check_output('open -a QuodLibet', shell=True)
  else:
    subprocess.check_output('echo {} > {}'.format(cmd_in, CONTROL_PATH), shell=True)

def cmd(phrase, param1):
  return '{} | bash={} param1={} terminal=false'.format(
    phrase, sys.argv[0], param1) 

if len(sys.argv) == 2:
    run_cmd(sys.argv[1])
else:
  if not os.path.exists(CUR_PATH) and not os.path.exists(CONTROL_PATH):
    print('♫')
    print('---')
    print((cmd('Open Quod Libet', 'open-ql')))
    sys.exit()

  if not os.path.exists(CUR_PATH):
    print('♫')
    print('---')
    print((cmd('Show window', 'focus')))
    sys.exit()

  status = get_current()

  print(('♫ {} - {} | length=30'.format(
    status['title'], status['artist'])))
  print('---')
  print((status['title']))
  print((status['album']))
  print((status['artist']))
  print((cmd('Play / Pause', 'play-pause')))
  print((cmd('Next', 'next')))
  print((cmd('Previous', 'menu-previous')))
  print('---')
  print((cmd('Delete', 'delete')))
