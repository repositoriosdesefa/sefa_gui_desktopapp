#!/bin/bash

DIA=`date +"%d/%m/%Y"`
HORA=`date +"%H:%M"`

echo -e "\033[0;32mUpdating main...\033[0m"
git add --all
git commit -m "Actualizacion automatica del $DIA a las $HORA"
git push origin