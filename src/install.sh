#!/bin/sh
# 13/05/2008
# PyCacic installer
progdir=$( 
  cd -P -- "$(dirname -- "$0")" && 
    pwd -P 
)


cmd_found()
{
	type $1 > /dev/null 2>&1;
}

install_python()
{
	if (cmd_found apt-get) then
		apt-get install python
	else 
		if (cmd_found yum) then
			yum install python
		else
			echo "ERROR: Python not installed. "
			exit
		fi
	fi
}

install_cacic()
{
	# rename install crypt file
	#mv $progdir/ccrypt.pycomp $progdir/ccrypt.pyc > /dev/null 2>&1
	
	tar -xf $progdir/cacic.tar -C /usr/share
	
	#rename final crypt files
	#mv /usr/share/pycacic/coletores/lib/ccrypt.pycomp /usr/share/pycacic/coletores/lib/ccrypt.pyc > /dev/null 2>&1
	
	python $progdir/setservice.py
}

start_cacic()
{
	echo -n "Starting PyCacic... "
	(python /usr/share/pycacic/cacic.py > /dev/null 2>&1)&
	echo "[OK]"
}

scpwd=`pwd`

echo -ne "Checking Python... "
if !(cmd_found python) then
	echo ""
	install_python
else
	echo "[OK]"
fi
install_cacic;
start_cacic
