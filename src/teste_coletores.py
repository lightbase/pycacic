# -*- coding: utf-8 -*-
 
import os;
import sys;
from lang.language import *
from coletores.col_hard import *;


class Coletores:
    """Aplicativo para testar os coletores (modo texto)"""

    lang = Language()

    def __init__(self):
        self.clearConsole()
        self.printHeader()
        self.printMenu()
        option = raw_input()
        if option == '1':
            self.clearConsole()
            self.initColHard()
            self.returnMenu()
        elif option == '2':
            self.clearConsole()
            self.initColSoft()
            self.returnMenu()
        elif option == '3':
            self.clearConsole()
            self.initColPat()
            self.returnMenu()
        elif option == '4':
            self.chooseLanguage()
        elif option == '5':
            self.clearConsole()
            return
        self.__init__()

    
    def clearConsole(self):
        """Limpa o console"""
        os.system(['clear','cls'][os.name == 'nt'])


    def returnMenu(self):
        """
            Exibe mensagem para pressionar tecla e
            retorna ao menu principal
        """
        key = self.lang.getMessagesHitKeys()
        print '\n>>>>>>> %s <<<<<<<' % key['enter']
        raw_input()


    def printHeader(self):
        """Imprime o cabecalho do programa"""
        header = self.lang.getHeader()
        print '\t' + '='*55
        print '\t______  ___    ___   ___   _____       ____   __   ____ ' 
        print '\t|  _  \ \  \  /  / /  __| |    \     / ___| |  | /  __| ' 
        print '\t| |_/  | \  \/  / / /     | |\ \   | /     |  | |  /    '
        print '\t|  ___/   \   /  | |   _ |   _  \  | |   _ |  | | |   _ ' 
        print '\t|  |      /  /   | \_/ | |  | \  \ |  \_/ ||  | | \_/ | '
        print '\t|__|     /__/    \____/ |__|  \__\ \____/ |__|  \____/  '
        print '\n\t\t %s ' % header['welcome']
        print '\t\t %s ' % header['description']
        print '\t\t %s \n' % self.lang.language
        print '\t' + '='*55


    def printMenu(self):
        """Imprime o menu do programa"""
        menu = self.lang.getMenu()
        print '\n';
        print '\t1 - %s' % menu['col_hard']
        print '\t2 - %s' % menu['col_soft']
        print '\t3 - %s' % menu['col_patr']
        print '\t4 - %s' % 'Choose Language'
        print '\t5 - %s' % menu['exit']

        
    def chooseLanguage(self):
        self.clearConsole()
        self.printHeader()
        print '\n';
        print '\t1 - Português'
        print '\t2 - Português (Brasil)'
        print '\t3 - Inglês'
        op = raw_input()
        if op == '1':
            self.lang.chooseLang('pt_PT')
        elif op == '2':
            self.lang.chooseLang('pt_BR')
        elif op == '3':
            self.lang.chooseLang('en_US')
        else:
            self.chooseLanguage()
            

    def initColHard(self):
        """Inicia o Coletor de Hardware"""
        c = Col_Hard()
        c.start()
        print "===============\n%s\n===============" % c.getChave('Col_Hard.UVC')
        print c.computer.toString()

    
    def initColSoft(self):
        """Inicia o Coletor de Software"""
        pass
    
    def initColPat(self):
        """Inicia o Coletor de Patrimonio"""
        pass



if __name__ == "__main__":
    cs = Coletores()
    
    