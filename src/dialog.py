#! /usr/local/bin/python

# 	$Id: DIALOG.py,v 1.5 1999/06/30 07:43:13 pkruse Exp $	
# written by Peter Kruse <pete@netzblick.de>
# Availability: http://www.brigadoon.de/peter/DIALOG.py
# Availability of dialog: search the directory
#                  ftp://sunsite.unc.edu/pub/Linux/utils/shell
# at the moment noone is maintaining this program (or is there?)

"""This module should define some standard dialogs.
It contains an interface to the dialog-program.
The following functions are provided with some having their own __doc__:

y_or_n_p(prompt)
    this is just a command-line question

screensize()

menu(title,menuname,height,width,menuheight,menuentries)

msgbox(title,height,width,message)

yesno(title,height,width,question)

password(title,height,width,text)
    the current standard dialogs do not have this option, so don't use it.

inputbox(title,height,width,text,initstring="")

infobox(title,height,width,message)

textbox(title,height,width,filename)

checklist(title,height,width,listheight,menuname,list)

radiolist(title,height,width,listheight,menuname,list)

guage(title,height,width,percent,message)
    if you want to use the guage widget, you must call this function
    first and guage_stop() last

guage_update(percent)

guage_message(message,percent)

guage_stop()
"""

import sys, tty, termios, curses, string, os, types

def y_or_n_p(prompt):
    """Ask user a "y or n" question.  Return 1 if answer is "y", 0 otherwise.
Takes one argument, which is the string to display to ask the question.
It should end in a space; `y_or_n_p' adds `(y or n) ' to it.
No confirmation of the answer is requested; a single character is enough."""
    fd=sys.stdin.fileno()
    save_attributes=termios.tcgetattr(fd)
    tty.setcbreak(fd)
    sys.stdout.write(prompt + "(y or n) ")
    try:
	c=sys.stdin.read(1)
    except:
	termios.tcsetattr(fd,termios.TCSAFLUSH,save_attributes)
	print "abort"
	return 0
    termios.tcsetattr(fd,termios.TCSAFLUSH,save_attributes)
    if c == "y":
	print "yes"
	return 1
    else:
	print "no"
	return 0

def screensize():
    """usage: (height,width,menuheight)=DIALOG.screensize()
    if DIALOG.yesno("spam",height,width,"eggs?"):
        print "eggs"
    else:
        print "no eggs\""""
    w=curses.initscr()
    (height,width)=w.getmaxyx()
    curses.endwin()
    minwidth=80
    minheight=24
    minmenuheight=17
    if width < minwidth:
	minwidth=width
    if height < minheight:
	minheight=height
	maxmenuheight=height - 7
	if maxmenuheight < minmenuheight:
	    minmenuheight=maxmenuheight
    return(minheight,minwidth,minmenuheight)


def menu(title,menuname,height,width,menuheight,menuentries):
    """function expects the following arguments:
    title: string
    menuname: string
    height: number
    width: number
    menuheight: number
    menuentries: list of tuples with two entries,
    which items should be either string or number"""
    command="dialog --clear --title \"" + title + "\" --menu \"" + menuname + \
	     "\" " + `height` + " " + `width` + " " + `menuheight`
    for menu in menuentries:
	if type(menu[0]) is not types.StringType:
	    menu0=`menu[0]`
	else:
	    menu0=menu[0]
	if type(menu[1]) is not types.StringType:
	    menu1=`menu[1]`
	else:
	    menu1=menu[1]
	command=command + " \"" + menu0 + "\" \"" + menu1 + "\""
    command=command + " 2>&1 > /dev/tty"
    diag=os.popen(normalize(command))
    ans=diag.read()
    # close seems to give us a return status
    r=diag.close()
    if r:
	return 0
    # which unfortunately maybe 256 that
    # calculates to 0 in the shell
    else:
	return ans

def normalize(text):
    import unicodedata
    return unicodedata.normalize('NFKD', unicode(text, 'latin_1', 'ignore')).encode('ASCII', 'ignore')

def msgbox(title,height,width,message):
    command="dialog --clear --title \"" + title + "\" --msgbox \"" + \
	     message + "\" " + `height` + " " + `width` + \
	     " 2>&1 > /dev/tty"
    return os.system(command)

def yesno(title,height,width,question):
    command="dialog --clear --title \"" + title + "\" --yesno \"" + \
	     question + "\" " + `height` + " " + `width` + \
	     " 2>&1 > /dev/tty"
    if os.system(command):
	return 0
    else:
	return 1
    
def password(title,height,width,text):
    """We modified dialog so it understands the --password argument."""
    command="dialog --clear --title \"" + title + "\" --passwordbox \"" + \
	     text + "\" " + `height` + " " + `width` + \
	     " 2>&1 > /dev/tty"
    diag=os.popen(command)
    ans=diag.read()
    r=diag.close()
    if r:
	return 0
    else:
	return ans

def inputbox(title,height,width,text,initstring=""):
    command="dialog --clear --title \"" + title + "\" --inputbox \"" + \
	     text + "\" " + `height` + " " + `width` + " \"" + \
	     initstring + "\"" + \
	     " 2>&1 > /dev/tty"
    diag=os.popen(command)
    ans=diag.read()
    r=diag.close()
    if r:
	return 0
    else:
	return ans

def infobox(title,height,width,message):
    command="dialog --title \"" + title + "\" --infobox " + \
	     "\"" + message + "\" " + \
	     `height` + " " + `width` + \
	     " 2>&1 > /dev/tty"
    diag=os.system(command)
    if diag:
	return 0
    else:
	return diag
    

def textbox(title,height,width,filename):
    command="dialog --title \"" + title + "\" --textbox " + \
	     "\"" + filename + "\" " + \
	     `height` + " " + `width` + \
	     " 2>&1 > /dev/tty"
    diag=os.system(command)
    if diag:
	return 0
    else:
	return diag
    

def checklist(title,height,width,listheight,menuname,list):
    # list should be like [["tag","item","on|off"],...]
    command="dialog --clear --title \"" + title + "\" --checklist \"" + \
	     menuname + \
	     "\" " + `height` + " " + `width` + " " + `listheight`
    for menu in list:
	if type(menu[0]) is not types.StringType:
	    menu0=`menu[0]`
	else:
	    menu0=menu[0]
	if type(menu[1]) is not types.StringType:
	    menu1=`menu[1]`
	else:
	    menu1=menu[1]
	menu2=menu[2]
	command=command + " \"" + menu0 + "\" \"" + menu1 + "\" \"" + \
		 menu2 + "\""
    command=command + " 2>&1 > /dev/tty"
    diag=os.popen(command)
    ans=diag.read()
    # close seems to give us a return status
    r=diag.close()
    if r:
	return 0
    # which maybe 256 which unfortunately
    # calculates to 0 in the shell
    else:
	return ans

def radiolist(title,height,width,listheight,menuname,list):
    # list should be like [["tag","item","on|off"],...]
    command="dialog --clear --title \"" + title + "\" --radiolist \"" + \
	     menuname + \
	     "\" " + `height` + " " + `width` + " " + `listheight`
    for menu in list:
	if type(menu[0]) is not types.StringType:
	    menu0=`menu[0]`
	else:
	    menu0=menu[0]
	if type(menu[1]) is not types.StringType:
	    menu1=`menu[1]`
	else:
	    menu1=menu[1]
	menu2=menu[2]
	command=command + " \"" + menu0 + "\" \"" + menu1 + "\" \"" + \
		 menu2 + "\""
    command=command + " 2>&1 > /dev/tty"
    diag=os.popen(command)
    ans=diag.read()
    # close seems to give us the return status
    r=diag.close()
    if r:
	return 0
    # which maybe 256 which unfortunately
    # calculates to 0 in the shell
    else:
	return ans

def guage(title,height,width,percent,message):
    global GUAGE
    cmd="dialog --title \"" + title + "\" --guage \"" + message + "\" " + \
	 `height` + " " + `width` + " " + `percent` + " 2>&1 >/dev/tty"
    GUAGE=os.popen(cmd,'w')

def guage_update(percent):
    GUAGE.write(`percent` + "\n")
    GUAGE.flush()

def guage_message(message,percent):
    GUAGE.write("XXX\n" + `percent` + "\n" + message + "\nXXX\n")
    GUAGE.flush()

def guage_stop():
    GUAGE.close()

