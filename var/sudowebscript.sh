#!/bin/bash
#
# web script allowing user www-data to run commands with root privilegs
# shell_exec('/var/sudowebscript.sh PARAMETER snapshot-filename')

case "$1" in
  run_healthsync) # $2 are the manual values
              python3 /opt/multiplatform-health-sync/main.py $2      ;;
