#!/bin/bash
CAMINHO="`dirname $0`"

if [ -f "$CAMINHO/gui.py" ]; then
	gksudo python "$CAMINHO/gui.py";
else
	echo 'Arquivo não encontrado';
fi