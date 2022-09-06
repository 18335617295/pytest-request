#!/bin/bash
. /etc/profile
# shellcheck disable=SC1090
cd /auto_test/gd_aep/ || exit
git pull
/usr/local/bin/python3.7 main.py