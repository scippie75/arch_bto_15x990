#!/usr/bin/python

import sys
import subprocess

display = subprocess.check_output("xrandr | grep primary | awk '{ print $1 }'", shell=True).decode('utf-8').strip()

brightness = 1.0
try:
  with open('/home/dirk/.brightness', 'r') as f:
    brightness = float(f.read())
except:
  pass

if len(sys.argv) == 2:
  p = sys.argv[1]
  if p[0] == '+':
    brightness = brightness + float(p[1:])
  elif p[0] == '-':
    brightness = brightness - float(p[1:])
  else:
    brightness = float(p)

brightness = max(0.0, min(1.0, brightness))

subprocess.run(['xrandr', '--output', display, '--brightness', str(brightness)])

with open('/home/dirk/.brightness', 'w') as f:
  f.write(str(brightness))

print(brightness)
