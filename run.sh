#!/bin/bash
# Author: jiujue
# Created Time: Fri 11 Oct 2019 04:28:54 PM CST
timestamp=$(date "+%Y%m%d%H%M%S")
nohup python3 manage.py runserver 0.0.0.0:80 >> log $timestamplog &
echo $timestamp
