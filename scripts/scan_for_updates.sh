#!/bin/bash
# Adapted by Yohann Bacha for DG2R (2017)

PATH=/bin:/usr/bin:/usr/local/bin

MOUNTEDPATH="$1"

if [ -e "$MOUNTEDPATH/UPDATE.dg2r" ]
then
    dt=$(date '+%d/%m/%Y %H:%M:%S');
    echo "$dt" > /usr/local/bin/logscan.txt
    echo "$(date '+%d/%m/%Y %H:%M:%S')" > /usr/local/bin/logscan.txt
    echo "Debut de lappli" >> /usr/local/bin/logscan.txt
    dg2r_update_daemon "$MOUNTEDPATH" &>> /usr/local/bin/logscan.txt
    echo "Ca marche !\n" >> /usr/local/bin/logscan.txt
else
    echo "Pas de fichier dedans" >> /usr/local/bin/logscan.txt
fi
