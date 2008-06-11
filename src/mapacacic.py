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

import curses
import curses.textpad
import string
import sys
import traceback
import dialog
import unicodedata

from libmapacacic import *

stdscr = curses.initscr()

hotkey_attr = curses.A_BOLD | curses.A_UNDERLINE
text_attr = curses.A_NORMAL

dict = {}
mp = None

def reinitScr():
    screen = curses.initscr()
    screen.bkgd(' ',  curses.color_pair(1))
    return screen

# Frame the interface area at fixed VT100 size
def main(stdscr):
    dict['1'] = ""
    dict['text1'] = ""
    dict['1a'] = ""
    dict['text1a'] = ""
    dict['2'] = ""
    dict['text2'] = ""
    dict['text3'] = ""
    dict['text4'] = ""
    dict['text5'] = ""
    dict['text6'] = ""
    dict['text7'] = ""
    dict['text8'] = ""
    dict['text9'] = ""
    curses.start_color()
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLUE)
    screen = stdscr.subwin(23, 79, 0, 0)
    #screen.box()
    screen.border("|", "|", "_", "_")
    screen.bkgd(' ',  curses.color_pair(1))
    screen.addstr(1, 1, "Mapa Cacic - Coletor avulso de patrimônio", curses.A_BOLD)
    screen.hline(2, 1, '_', 77)
    screen.refresh()
    loop = 1
    while loop:
        auth = authDialog(screen)
        #screen.refresh()
        if auth == None:
            loop = 0
        else:
            global mp
            mp = MapaCacic(auth[0], auth[1])
            showStatus("Autenticando")
            r = mp.auth()
            if r:
                loop = 0
                showStatus("Obtendo configuracoes")
                mp.getInfo()
                parseCurrentValues()
                showPatr(screen)
            else:
                showError("Login ou senha inválidos.")
                
def parseCurrentValues():
    global mp
    currentDict = mp.getCurrentValues()
    # seta valores ativos
    try:
        if currentDict.has_key('ID1a') and currentDict['ID1a'] != '':
            for entidade in mp.labels['1'].getValues():
                if entidade.hasItem(currentDict['ID1a']):
                    dict['text1'] = entidade.getText()
                    dict['nivel1'] = entidade
                    dict['1'] = entidade.getId()
                    
                    ldn = entidade.getSubItem(currentDict['ID1a'])
                    dict['text1a'] = ldn.getText()
                    dict['nivel1a'] = ldn
                    dict['1a'] = ldn.getId()
                    
                    orgao = ldn.getSubItem(currentDict['ID2'])
                    dict['text2'] = orgao.getText()
                    dict['nivel2'] = orgao
                    dict['2'] = orgao.getId()
    except:
        import traceback
        
        showError(traceback.format_exc())
        showError("Alguns valores recebidos estavam desatualizados e foram descartados")
    dict['text3'] = currentDict['TE_LOC_COMPL']
    dict['text4'] = currentDict['TE_INFO1']
    dict['text5'] = currentDict['TE_INFO2']
    dict['text6'] = currentDict['TE_INFO3']
    dict['text7'] = currentDict['TE_INFO4']
    dict['text8'] = currentDict['TE_INFO5']
    dict['text9'] = currentDict['TE_INFO6']
        
def showStatusCurses(screen, text):
     st = screen.subwin(4, 30, 7, 25)
     st.border("|", "|", "_", "_")
     st.addstr(1, 2, text, text_attr)
     return st
 
def showStatus(text):
     dialog.infobox("MapaCacic", 7, 60, text)

def showInfo(text):
     dialog.msgbox("MapaCacic - Info", 7, 60, text)

def showError(text):
     dialog.msgbox("MapaCacic - Erro", 7, 60, text)

def showPatr(screen):
    ret = ''
    aux = mp.labels.keys()
    aux.sort()
    while ret != 'Salvar':
        list = []
        for k in aux:
            v = mp.labels[k]
            text = normalize(v.getText())
            value = normalize(dict['text'+k])
            list.append((text, value))
        
        list.append(('', ''))
        list.append(('Salvar', 'Envia os valores para o gerente web'))
        list.append(('Sair', 'Encerra sem enviar os valores para o gerente web'))
        ret = dialog.menu("MapaCacic - Patrimônio", "Selecione para editar", 0, 0, 0, list)
        if ret == 'Salvar' or ret == 'Sair':
            break;
        selectValor(ret)
        
    if ret == 'Salvar':
        valores = {}
        valores['id_unid_organizacional_nivel1a'] = dict['1a']
        valores['id_unid_organizacional_nivel2'] = dict['2']
        valores['te_localizacao_complementar'] = dict['text3']
        valores['te_info_patrimonio1'] = dict['text4']
        valores['te_info_patrimonio2'] = dict['text5']
        valores['te_info_patrimonio3'] = dict['text6']
        valores['te_info_patrimonio4'] = dict['text7']
        valores['te_info_patrimonio5'] = dict['text8']
        valores['te_info_patrimonio6'] = dict['text9']
        showStatus("Enviando informações...")
        if mp.save(valores):
            showInfo("Informações enviadas com sucesso.")
        else:
            showInfo("Erro enviando informações.")
    
    #dialog.infobox("TESTE", 7, 60, ret)

def showPatrCurses(screen):
    loop = 1
    
    while loop:
        screen = reinitScr()
        
        scr = screen.subwin(0, 0)
        str1 = "Entidade:         "
        str2 = "Linha de Negocio: "
        str3 = "Orgao:            "
        str4 = "Secao / Sala / Ramal: "
        str5 = "PIB da CPU"
        str6 = "N Serie CPU"
        str7 = "PIB do Monitor"
        str8 = "N Serie Monitor*"
        str9 = "PIB da Impressora"
        str10 = "N Serie Impressora*"
        
        scr.addstr(4, 2, str1, curses.A_BOLD)
        valor = dict['text1']
        scr.addstr(5, 2, valor + ' '*(30 - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(7, 2, str2, curses.A_BOLD)
        valor = dict['text1a']
        scr.addstr(8, 2, valor + ' '*(30 - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(10, 2, str3, curses.A_BOLD)
        valor = dict['text2']
        scr.addstr(11, 2, valor + ' '*(30 - len(valor)), curses.A_STANDOUT)
        
        size = 40
        
            
        scr.addstr(4, 36, str4, curses.A_BOLD)
        valor = dict['text3']
        scr.addstr(5, 36, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        size = 20
        spc = 2
        
        scr.addstr(7, 36, str5, curses.A_BOLD)
        valor = dict['text4']
        scr.addstr(8, 36, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(7, 36+size+2, str6, curses.A_BOLD)
        valor = dict['text7']
        scr.addstr(8, 36+size+2, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(10, 36, str7, curses.A_BOLD)
        valor = dict['text5']
        scr.addstr(11, 36, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(10, 36+size+2, str8, curses.A_BOLD)
        valor = dict['text8']
        scr.addstr(11, 36+size+2, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(13, 36, str9, curses.A_BOLD)
        valor = dict['text6']
        scr.addstr(14, 36, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        
        scr.addstr(13, 36+size+2, str10, curses.A_BOLD)
        valor = dict['text9']
        scr.addstr(14, 36+size+2, valor+' '*(size - len(valor)), curses.A_STANDOUT)
        
        scr.vline(3, 34, "|", 13)
        scr.hline(15, 1, "_", 77)
        
        str1 = "Selecione uma opcao:"
        scr.addstr(16, 2, str1, curses.A_BOLD)
        
        str1 = "1 - Selecionar Entidade/LN/Orgao"
        scr.addstr(18, 2, str1, curses.A_BOLD)
        
        str1 = "2 - Editar Secao/Sala/Ramal"
        scr.addstr(19, 2, str1, curses.A_BOLD)
        
        str1 = "3 - Editar PIB/Serie da CPU"
        scr.addstr(20, 2, str1, curses.A_BOLD)
        
        str1 = "4 - Editar PIB/Serie do Monitor"
        scr.addstr(21, 2, str1, curses.A_BOLD)
        
        str1 = "5 - Editar PIB/Serie da Impressora"
        scr.addstr(18, 40, str1, curses.A_BOLD)
        
        curses.noecho()
        #screen.redrawwin()
        screen.refresh()
        c = -1
        while c not in range(1,5):
            try:
                c = int(chr(scr.getch()))
            except:
                c = -1
        
        if c == 1:
           selectEnt()
        
           #sys.exit()

def selectValor(selected):
    global mp, dict    
    list = []
    
    for k, v in mp.labels.items():
        text = normalize(v.getText())
        if text == selected:
            
            if k == '1':
                sub = mp.labels['1'].values
                for k1, v1 in sub.items():
                    if dict.has_key('nivel1') and dict['nivel1'].getId() == v1.getId():
                        list.append((str(k1), normalize(v1.getText()), "on" ))
                    else:
                        list.append((str(k1), normalize(v1.getText()), "off" ))
                        
                    
                nivel1 = dialog.radiolist("Selecione: ", 0, 40, 15, selected.capitalize(), list)
                if nivel1 != 0 and nivel1 != '':
                    dict['nivel1'] = sub[nivel1]
                    dict['text1'] = sub[nivel1].getText()
            elif k == '1a':
                if not dict.has_key('nivel1'):
                    showError("Selecione '"+normalize(mp.labels['1'].getText())+"' primeiro")
                else:
                    sub = dict['nivel1'].subitems
                    for k1, v1 in sub.items():
                        if dict.has_key('nivel1a') and dict['nivel1a'].getId() == v1.getId():
                            list.append((str(k1), normalize(v1.getText()), "on" ))
                        else:
                            list.append((str(k1), normalize(v1.getText()), "off" ))
                    
                    nivel1a = dialog.radiolist("Selecione: ", 0, 40, 15, selected.capitalize(), list)
                    if nivel1a != 0 and nivel1a != '':
                        dict['nivel1a'] = sub[nivel1a]
                        dict['text1a'] = sub[nivel1a].getText()
                        dict['1a'] = nivel1a
            elif k == '2':
                if not dict.has_key('nivel1a'):
                    if not dict.has_key('nivel1'):
                        showError("Selecione '"+normalize(mp.labels['1'].getText())+"' primeiro")
                    else:
                        showError("Selecione '"+normalize(mp.labels['1a'].getText())+"' primeiro")
                else:
                    sub = dict['nivel1a'].subitems
                    for k1, v1 in sub.items():
                        if dict.has_key('nivel2') and dict['nivel2'].getId() == v1.getId():
                            list.append((str(k1), normalize(v1.getText()), "on" ))
                        else:
                            list.append((str(k1), normalize(v1.getText()), "off" ))
                    
                    nivel2 = dialog.radiolist("Selecione: ", 0, 40, 15, selected.capitalize(), list)
                    if nivel2 != 0 and nivel2 != '':
                        dict['nivel2'] = sub[nivel2]
                        dict['text2'] = sub[nivel2].getText()
                        dict['2'] = nivel2
            else:
                dict['text'+k] = dialog.inputbox("Entrada", 7, 40, selected.capitalize(), dict['text'+k])
            break;

def normalize(text):
    try:
        return unicodedata.normalize('NFKD', unicode(text)).encode('ASCII', 'ignore')    
    except:
        return unicodedata.normalize('NFKD', unicode(text, 'latin_1', 'ignore')).encode('ASCII', 'ignore')
    
def selectEnt():
    global mp, dict
    
    list = []
    nivel1 = None
    sub = mp.labels['1'].values
    for k, v in sub.items():
        list.append((str(k), v.getText(), "off" ))
    nivel1 = dialog.radiolist("Selecione Entidade", 0, 40, 15, "Entidades:", list)
    
    if nivel1 != 0:
        dict['text1'] = sub[nivel1].getText()
    
        list = []
        sub = sub[nivel1].subitems
        for k, v in sub.items():
            list.append((str(k), v.getText(), "off" ))
        nivel1a = dialog.radiolist("Selecione Linha de Negocio", 0, 40, 15, "", list)
        
        if nivel1a != 0:
            dict['text1a'] = sub[nivel1a].getText()
            
            list = []
            sub = sub[nivel1a].subitems
            for k, v in sub.items():
                list.append((str(k), v.getText(), "off" ))
                
            nivel2 = dialog.radiolist("Selecione Orgao", 0, 40, 15, "", list)
            if nivel2 != 0:
                dict['text2'] = sub[nivel2].getText()
                
def authDialog(screen):
    ad = screen.subwin(10, 40, 7, 20)
    ad.border("|", "|", "_", "_")
    c = ""
    while 1:
        msg0 = "MapaCacic - Coletor Avulso de Patrimônio\n\nPor favor informe um login de nivel 'tecnico'"
        dialog.msgbox("MapaCacic", 7, 60, msg0)
        
        user = ''
        while user == '' or user == 0:
            user = dialog.inputbox("Autenticação", 7, 40, "Login:", "")
            
        pwd = ''
        while pwd == '' or pwd == 0:
            pwd = dialog.password("Autenticação", 7, 40, "Password:")
        
        return (user, pwd)
        
def authDialogOld(screen):
    ad = screen.subwin(10, 40, 7, 20)
    ad.border("|", "|", "_", "_")
    c = ""
    while 1:
        str0 = "Autenticacao"
        ad.addstr(1, (30 - len(str0))/2, str0, curses.A_BOLD)
        str1 = "LOGIN:    "
        ad.addstr(2, 2, str1, curses.A_BOLD)
        ad.addstr(2, len(str1) + 3, ' '*20, curses.A_STANDOUT)
        
        str2 = "PASSWORD: "
        ad.addstr(4, 2, str2, curses.A_BOLD)
        ad.addstr(4, len(str2) + 3, ' '*20, curses.A_STANDOUT)
        
        str3 = "O login deve possuir nivel 'tecnico'"
        ad.addstr(6, 2, str3, curses.color_pair(2) | curses.A_BOLD)
        
        str3 = "Sair"
        str4 = "Corrigir"
        str5 = "OK"
        
        ad.standout()
        user = ad.getstr(2, len(str1) + 3)
        pwd = ad.getstr(4, len(str2) + 3)
        ad.standend()
        
        r = 30 - 2
        ad.addstr(8, r - len(str3) , str3[0:1], hotkey_attr)
        ad.addstr(8, r - len(str3) + 1, str3[1:], text_attr)    
        r = r - len(str3) - 2
        
        ad.addstr(8, r - len(str4) , str4[0:1], hotkey_attr)
        ad.addstr(8, r - len(str4) + 1, str4[1:], text_attr)    
        r = r - len(str4) - 2
        
        ad.addstr(8, r - len(str5) , str5[0:1], hotkey_attr)
        ad.addstr(8, r - len(str5) + 1, str5[1:], text_attr)    
        r = r - len(str5) - 2
        
        while c.upper() not in (str3[0:1].upper(), str4[0:1].upper(), str5[0:1].upper()):
               c = chr(ad.getch())
        
        if c.upper() in (str5[0:1].upper()):
            ad.clear()
            return (user , pwd)
        #elif c.upper() == upper(str4[0:1]):
        #    pass
        elif c.upper() == str3[0:1].upper():
            ad.clear()
            return None
    
    
    
    

if __name__=='__main__':
    try:
        # Initialize curses
        stdscr=curses.initscr()
        #curses.start_color()
        # Turn off echoing of keys, and enter cbreak mode,
        # where no buffering is performed on keyboard input
        #curses.noecho()
        curses.cbreak()
        # In keypad mode, escape sequences for special keys
        # (like the cursor keys) will be interpreted and
        # a special value like curses.KEY_LEFT will be returned
        stdscr.keypad(1)
        if os.system('dialog') == 0:
            main(stdscr) # Enter the main loop
            # Set everything back to normal
            stdscr.keypad(0)
            curses.echo();
            curses.nocbreak()
            curses.endwin()  
        else:
            # Set everything back to normal
            stdscr.keypad(0)
            curses.echo();
            curses.nocbreak()
            curses.endwin()  
            print "FATAL: Módulo 'dialog' requerido mas não está disponível."
                       # Terminate curses
    except:
        # In the event of an error, restore the terminal
        # to a sane state.
        stdscr.keypad(0)
        curses.echo()
        curses.nocbreak()
        curses.endwin()
        traceback.print_exc()
        