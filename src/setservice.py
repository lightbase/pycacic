# -*- coding: UTF-8 -*-

import sys
import os
import commands
import md5
import re

from ccrypt import CCrypt

def getDir():
    va = sys.argv[0]
    if va[0] == "/":
        return os.path.dirname(va)
    else:
        return os.path.dirname(os.getcwd()+"/"+va)

DIR = getDir()
CACIC_CONF = "/usr/share/pycacic/config/cacic.conf"
CACIC_CONF_ENC = "/usr/share/pycacic/config/cacic.dat"

def writeService():
    f = open("/etc/init.d/cacic", "w")
    f.write("#!/bin/sh\n")
    f.write('if [ "$1" = "start" ]; then\n')
    Py = commands.getoutput("which python")
    f.write("(" + Py + " /usr/share/pycacic/cacic.py)&\n")
    f.write('fi\n')
    f.close()
    os.chmod("/etc/init.d/cacic", 0755)
    
def writeStartLink(number):
    commands.getoutput("ln -sf /etc/init.d/cacic /etc/rc%s.d/S99cacic" % number)
    

def writeCron():
    f = open("/etc/cron.hourly/chksis", "w")
    f.write("#!/bin/sh\n")
    f.write("# Cacic process monitor\n")
    f.write("\n")
    f.write("Cacic=''\n")
    f.write("Cacic=`ps x | grep cacic.py | grep -v grep 2> /dev/null`\n")
    f.write('if [ "$Cacic" = "" ]; then\n')
    f.write("(python /usr/share/pycacic/cacic.py)&\n")
    f.write("fi")
    f.close()
    os.chmod("/etc/cron.hourly/chksis", 0755)
    
def writeMD5():
    f = open(DIR+"/cacic.tar")
    content = f.read()
    f.close()
    hexmd5 = md5.new(content).hexdigest()
    f = open("/usr/share/pycacic/config/MD5SUM", "w")
    f.write(hexmd5)
    f.close()
    
def writeGnomeAutoStart():
    content = []
    content.append("[Desktop Entry]")
    content.append("Name=PyCacic")
    content.append("Comment=Configurador Automático e Coletor de Informações Computacionais")
    content.append("Exec=python /usr/share/pycacic/gui.py")
    content.append("Icon=/usr/share/pycacic/img/logo.png")
    content.append("StartupNotify=true")
    content.append("Terminal=false")
    content.append("Type=Application")
    content.append("Categories=Utility;System;") 
    # AutoStart
    f = open("/etc/xdg/autostart/pycacic.desktop", "w")
    f.write('\n'.join(content))    
    f.close()
    # Menu Item
    f = open("/usr/share/applications/pycacic.desktop", "w")
    f.write('\n'.join(content))
    f.close()
    
def install():
    print "Installing PyCacic Service...",
    writeService()
    writeStartLink(2)
    writeStartLink(3)
    writeStartLink(4)
    writeStartLink(5)
    print "[OK]"
    configAndPackage()
    print "Generating Version Hash",
    writeMD5()
    print "[OK]"
    print "Adding to cron ",
    writeCron()
    print "[OK]"
    print "Adding to Gnome AutoStart ",
    writeGnomeAutoStart()
    print "[OK]"

def isPreconfigured():
    return not os.path.exists("/usr/share/pycacic/config/cacic.conf") and os.path.exists("/usr/share/pycacic/config/cacic.dat")

def configAndPackage(force = 0):
    """ Configura e opcionalmente gera um novo pacote """
    if not isPreconfigured() or force:
        mkconfig()
        resp = ''
        while (not resp in ('S', 'Y')) and resp != 'N':
            resp = raw_input("Deseja gerar um novo pacote de instalacao pre-configurado com esta config? (Y/N)")
            resp = resp.upper()
        if resp in ('S', 'Y'):
            import os
            os.system("tar -C /usr/share -cf "+DIR+"/cacic.tar pycacic/")
            #print DIR+"/cacic.tar foi substituido pela versao configurada"
            os.system("tar -C "+DIR+"/.. -czf /tmp/pycacic-preconf.tar.gz pycacic/")
            print "Gerado pacote de instalacao pre-configurado: /tmp/pycacic-preconf.tar.gz"
    else:
        print "Preconfiguracao detectada!"


def mkconfig():
    """Abre console para configuracao do PyCacic"""
    from io import Writer
    print "\n\t--- Bem-Vindo a Configuracao do PyCacic ---"
    print "\n\tapos preencher as informacoes abaixo o programa ira iniciar\n"
    op = ''
    while not op in ('S', 'Y'):
        addr = raw_input("End. do  Servidor ('ex: http://10.0.0.1'): ")
        p = re.compile('[0-9]{1,3}(?:\.[0-9]{1,3}){3}')
        if len(p.findall(addr)) == 0:
            print "Endereco invalido"
            mkconfig()
            return 
        ip = p.findall(addr)[0]
        print "Testando conexão...",
        if commands.getoutput('ping %s -c 1; echo $?' % ip)[-1:] != '0':
            print "Erro ao tentar conectar ao servidor"
            mkconfig()
            return
        print "[OK]"
        user = raw_input("Usuario do Servidor: ")
        pwd = raw_input("Senha: ")
        op = raw_input("\nOs dados estao corretos? (Y|N)").upper()
    
    if addr[len(addr)-1] == '/': addr = addr[:-1]
    Writer.setServer('address', addr, CACIC_CONF, False)
    Writer.setServer('username', user, CACIC_CONF, False)
    Writer.setServer('password', pwd, CACIC_CONF, False)
    print "\t--- Configuracao concluida com sucesso ---\n\n"
    
    f = open(CACIC_CONF)
    content = f.read()
    f.close()
    
    cipher = CCrypt()
    crypted = cipher.encrypt(content)
    
    f = open(CACIC_CONF_ENC, "w")
    f.write(crypted)
    f.close()
    
    os.unlink(CACIC_CONF)
    print "\t--- Configuracao encryptada com sucesso ---\n\n"

if __name__ == '__main__':
    install()