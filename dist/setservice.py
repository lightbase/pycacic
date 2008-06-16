# -*- coding: UTF-8 -*-

"""

    Copyright 2000, 2001, 2002, 2003, 2004, 2005 Dataprev - Empresa de Tecnologia e Informações da Previdência Social, Brasil
    
    Este arquivo é parte do programa CACIC - Configurador Automático e Coletor de Informações Computacionais
    
    O CACIC é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como 
    publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença, ou (na sua opnião) qualquer versão.
    
    Este programa é distribuido na esperança que possa ser  util, mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
    MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
    
    Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENCA.txt", junto com este programa, se não, escreva para a Fundação do Software
    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""

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

def cmd_exists(cmd):
    return os.system(cmd+' > /dev/null 2>&1') == 0

DIR = getDir()
CACIC_CONF = "/usr/share/pycacic/config/cacic.conf"
CACIC_CONF_ENC = "/usr/share/pycacic/config/cacic.dat"

def getSOLang():
    """Retorna o idioma padrão do sistema operacional"""
    so_lang = ''
    # tenta pegar idioma das variaveis de ambiente do python
    if os.environ.has_key('LANG'):
        so_lang = os.environ['LANG']
    # caso contrario pega do sistema
    else:
        so_lang = commands.getoutput('locale | grep LANG=')        
        so_lang[len('LANG='):]
    return so_lang.split('.')[0]


def writeService():
    f = open("/etc/init.d/cacic", "w")
    f.write("#!/bin/sh\n")
    f.write('if [ "$1" = "start" ]; then\n')
    Py = commands.getoutput("which python")
    f.write("(" + Py + " /usr/share/pycacic/cacic.py > /usr/share/pycacic/logs/agent.log 2>&1)&\n")
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
    content.append("Exec=/usr/share/pycacic/gui.py")
    content.append("Icon=/usr/share/pycacic/img/logo.png")
    content.append("StartupNotify=true")
    content.append("Terminal=false")
    content.append("Type=Application")
    content.append("Categories=Utility;System;") 
    # AutoStart
    if os.path.exists('/etc/xdg/autostart/'):
        f = open("/etc/xdg/autostart/pycacic.desktop", "w")
        f.write('\n'.join(content))    
        f.close()
    # Menu Item
    if os.path.exists('/usr/share/applications/'):
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
        while (not resp in ('S', 'Y', 'N')):
            resp = raw_input("Deseja gerar um novo pacote de instalação pre-configurado (Formato: .tgz) ? (Y/N)")
            resp = resp.upper()
        if resp in ('S', 'Y'):
            import os
            os.system("tar -C /usr/share -cf "+DIR+"/cacic.tar pycacic/")
            #print DIR+"/cacic.tar foi substituido pela versao configurada"
            os.system("tar -C "+DIR+"/.. -czf /tmp/pycacic-preconf.tgz pycacic/")
            print "Gerado pacote de instalacao pre-configurado: /tmp/pycacic-preconf.tgz"
        resp = ''
        while (not resp in ('S', 'Y', 'N')):
            resp = raw_input("Deseja gerar um novo pacote de instalação pre-configurado (Formato: .deb) ? (Y/N)")
            resp = resp.upper()
        if resp in ('S', 'Y'):
            import os
            resp = ''
            while (not resp in ('S', 'Y', 'N')):
                resp = raw_input("Deseja que o coletor patrimonial seja invocado automaticamente após a instalação? (Y/N)")
                resp = resp.upper()
            if resp in ('S', 'Y'):
                f = open(DIR+"/gdeb/postinst" , 'a')
                str = 'if [ "$1" = "configure" ]; then\n'
                str+= '    if [ "$DISPLAY" = "" ]; then\n'
                str+= '        (nohup python /usr/share/pycacic/mapacacic.py > /dev/null 2>&1)\n'
                str+= '    else\n'
                str+= '        (nohup python /usr/share/pycacic/guimapacacic.py > /dev/null 2>&1)&\n'
                str+= '    fi\n'
                str+= 'fi\n'
                f.write(str)
                f.close()
            os.chmod(DIR+"/gdeb/gera-deb.sh", 0755)
            os.system('cd '+DIR+'/gdeb/;'+DIR+"/gdeb/gera-deb.sh")
    else:
        print "Preconfiguracao detectada!"


def mkconfig():
    """Abre console para configuracao do PyCacic"""
    from io import Writer
    print "\n\t--- Bem-Vindo a Configuracao do PyCacic ---"
    print "\n\tapós preencher as informacoes abaixo o programa irá iniciar\n"
    op = ''
    while not op in ('S', 'Y'):
        addr = raw_input("Endereço do  Servidor ('ex: http://<endereco>/'): ").lower()
        if len(addr.split('//')) != 2:
            print "Endereco invalido"
        else:
            http = addr.split('//')[0]
            host = addr.split('//')[1]
            if not http in ('http:', 'https:') or host.strip() == '':
                print "Endereco invalido"            
            else:            
                print "Testando conexão...",
                if commands.getoutput('ping %s -c 1; echo $?' % host)[-1:] != '0':
                    print "Erro ao tentar conectar ao servidor"
                else:
                    print "[OK]"
                    user = raw_input("Usuario do Agente: ")
                    pwd = raw_input("Senha: ")
                    op = raw_input("\nOs dados estao corretos? (Y|N)").upper()
    # remove a barra do final
    if addr[len(addr)-1] == '/':
        addr = addr[:-1]
    # sava as configuracoes
    Writer.setServer('address', addr, CACIC_CONF, False)
    Writer.setServer('username', user, CACIC_CONF, False)
    Writer.setServer('password', pwd, CACIC_CONF, False)
    Writer.setPycacic('locale', getSOLang(), CACIC_CONF, False)
    
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