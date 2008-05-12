#!/bin/bash
CAMINHO="`dirname $0`"

nome1="rogerio"
nome2="rogerio"

if [ "$nome1" = "$nome2" ]; then
	echo "Hahaiee";
fi

if [ -f "$CAMINHO/gui.py" ]; then
	echo 'a'
	#gksudo python "$CAMINHO/gui.py";	
else
	echo 'Arquivo não encontrado';
fi