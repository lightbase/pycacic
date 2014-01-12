#!/usr/bin/env python
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

import string
import sys
import traceback
import dialog
import unicodedata
from urllib2 import URLError

def showError(text):
     dialog.msgbox("MapaCACIC - Erro", 7, 100, text)

try:
    from libmapacacic import *
except:
    showError("Erro carregando configuracoes.")
    sys.exit(1)

dict = {}
mp = None

# Frame the interface area at fixed VT100 size
def main():
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
    loop = 1
    while loop:
        auth = authDialog()
        if auth == None:
            loop = 0
        else:
            global mp
            mp = MapaCacic()
            showStatus("Autenticando")
            try:
                r = mp.auth(auth[0], auth[1])
                if r:
                    loop = 0
                    showStatus("Obtendo configuracoes")
                    mp.getInfo()
                    parseCurrentValues()
                    showPatr()
                else:
                    showError("Login ou senha invaidos.")
            except URLError, e:
                showError("Falha na comunicacaonDetalhes: %s " % e)
                loop = 0
            except Exception, e:
                showError("Falha na comunicacaonDetalhes: %s " % e)
                loop = 0
                
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
 
def showStatus(text):
     dialog.infobox("MapaCACIC", 7, 60, text)

def showInfo(text):
     dialog.msgbox("MapaCACIC - Info", 7, 100, text)

def showPatr():
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
        ret = dialog.menu("MapaCACIC - Patrimonio", "Selecione para editar", 0, 0, 0, list)
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
        showStatus("Enviando informacoes...")
        if mp.save(valores):
            showInfo("Informacoes enviadas com sucesso.")
        else:
            showInfo("Erro enviando informacoes.")
    
    #dialog.infobox("TESTE", 7, 60, ret)

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
                
def authDialog():
    c = ""
    while 1:
        msg0 = "MapaCACIC - Coletor Avulso de Informacoes Patrimoniais"
        dialog.msgbox("MapaCACIC", 7, 100, msg0)
        
        user = ''
        while user == '':
            user = dialog.inputbox("Autenticacao 7, 40, "Login:", "")
        
        if user == 0:
            return None
        
        pwd = ''
        while pwd == '':
            pwd = dialog.password("Autenticacao 7, 40, "Password:")
        
        if pwd == 0:
            return None
        
        return (user, pwd)

if __name__=='__main__':
    try:
        if os.system('dialog > /dev/null 2>&1') == 0:
            main() # Enter the main loop
        else:
            # Set everything back to normal
            print "FATAL: Moduo 'dialog' requerido mas nao disponivel."
    except:
        traceback.print_exc()
        
