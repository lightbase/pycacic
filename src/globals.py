# -*- coding: UTF-8 -*-

"""

    Modulo globals
    
    Modulo contendo variáveis globais do sistema
    
    @author: Dataprev - ES

"""

import sys
import os
from config.io import Reader

class Globals:
        
    VERSION = "1.0.0"
    PATH = ""
    INSTALLED = False
    PC_XML = ""
    
    def __init__(self):
        pass
# fim classe

# staticos
def getDir():
    va = sys.argv[0]
    if va[0] == "/":
        return os.path.dirname(va)
    else:
        return os.path.dirname(os.getcwd()+"/"+va)
        
def getArgs():
    for arg in sys.argv:
        if arg[0:4] == "-xml":
            Globals.PC_XML = arg[5:]

def isInstalled():
    return (Reader.getStatus('installed')['value'] == 'yes')


    
Globals.PATH = getDir()
Globals.INSTALLED = isInstalled()


getArgs()