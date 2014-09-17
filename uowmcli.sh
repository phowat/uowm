#! /bin/bash

SCREEN=`command -v screen`
UOWMCLI="/home/pedro/venv/bin/python /home/pedro/Code/uowm/uowm.py --cli"
if [ -n "$SCREEN" ]
then
	${SCREEN} ${UOWMCLI}
else
	$UOWMCLI
fi
