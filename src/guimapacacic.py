# -*- coding: UTF-8 -*-
#!/usr/bin/env python

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

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, gobject

from globals import Globals
from libmapacacic import MapaCacic

class GUIMapaCacic:
    """ 
        Classe de interface gráfica para o MapaCacic - Coletor Avulso de Patrimônio
    """
    
    def __init__(self, mc):
        # caminhos
        self.mc = mc
        self.ICON_PATH = "%s/img/logo.png" % Globals.PATH
        self.GLADE_PATH = '%s/glade/' % Globals.PATH
        self.TITLE = 'PyCacic - Coletor de Informações Patrimoniais'
        self.selected1 = None
        self.selected1a = None
        self.selected2 = None
        
    def show(self):
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'mapacacic.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('mapacacic')
        self.window.set_title(self.TITLE)
        
        # Labels
        for k, v in self.mc.labels.items():
            label = self.xml.get_widget('label'+k)
            label.set_text(unicode(v.getText(), 'latin_1', 'ignore'))
        
        # Valores atuais
        dict = self.mc.getCurrentValues()
        
        self.entry1 = self.xml.get_widget('entry1')
        self.entry2 = self.xml.get_widget('entry2')
        self.entry3 = self.xml.get_widget('entry3')
        self.entry4 = self.xml.get_widget('entry4')
        self.entry5 = self.xml.get_widget('entry5')
        self.entry6 = self.xml.get_widget('entry6')
        self.entry7 = self.xml.get_widget('entry7')
        
        self.entry1.set_text(dict['TE_LOC_COMPL'])
        self.entry2.set_text(dict['TE_INFO1'])
        self.entry3.set_text(dict['TE_INFO2'])
        self.entry4.set_text(dict['TE_INFO3'])
        self.entry5.set_text(dict['TE_INFO4'])
        self.entry6.set_text(dict['TE_INFO5'])
        self.entry7.set_text(dict['TE_INFO6'])
        
        self.combobox1 = self.xml.get_widget('combobox1')
        self.combobox1a = self.xml.get_widget('combobox1a')
        self.combobox2 = self.xml.get_widget('combobox2')
        liststore1 = gtk.ListStore(str)
        cell = gtk.CellRendererText()
        
        self.liststore1a = gtk.ListStore(str)
        self.liststore2 = gtk.ListStore(str)
        
        self.combobox1.pack_start(cell)
        self.combobox1.add_attribute(cell, 'text', 0)
        self.combobox1.set_model(liststore1)
        
        self.combobox1a.pack_start(cell)
        self.combobox1a.add_attribute(cell, 'text', 0)
        self.combobox1a.set_model(self.liststore1a)
        
        self.combobox2.pack_start(cell)
        self.combobox2.add_attribute(cell, 'text', 0)
        self.combobox2.set_model(self.liststore2)
        
        self.combo1list = []
        self.combo1alist = []
        self.combo2list = []
        idx = 0
        for v in self.mc.labels['1'].getValues():
            self.combo1list.append(v)
            liststore1.append([ v.getText() ])
            v.index = idx
            idx = idx + 1
            
        # seta valores ativos nos combox
        try:
            if dict.has_key('ID1a') and dict['ID1a'] != '':
                for entidade in self.mc.labels['1'].getValues():
                    if entidade.hasItem(dict['ID1a']):
                        self.combobox1.set_active(entidade.index)
                        ldn = entidade.getSubItem(dict['ID1a'])
                        self.combobox1a.set_active(ldn.index)
                        orgao = ldn.getSubItem(dict['ID2'])
                        self.combobox2.set_active(orgao.index)
        except:
            import traceback
            traceback.print_exc()
            self.showAlert("Alguns valores recebidos estão desatualizados e foram descartados")
                        
    def normalize(self, text):
        import unicodedata
        return unicodedata.normalize('NFKD', unicode(text, 'latin_1', 'ignore')).encode('latin_1', 'ignore')
        
    def showAlert(self, msg):
        """Exibe janela do tipo Alert"""
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)        
        dialog.set_title(self.TITLE)
        dialog.set_icon_from_file(self.ICON_PATH)
        dialog.width, dialog.height = dialog.get_size()
        dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
        op = dialog.run()
        dialog.destroy()
        return op
    
    def showInfo(self, msg):
        """Exibe janela do tipo Alert"""
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_INFO, gtk.BUTTONS_CLOSE, msg)        
        dialog.set_title(self.TITLE)
        dialog.set_icon_from_file(self.ICON_PATH)
        dialog.width, dialog.height = dialog.get_size()
        dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
        op = dialog.run()
        dialog.destroy()
        return op
    
    def on_mapacacic_destroy(self, widget):
        gtk.main_quit()
    
    def on_combobox1_changed(self, widget):
        idx = self.combobox1.get_active()
        sel = self.combo1list[idx]
        self.selected1 = sel
        self.combo1alist = []
        index = 0
        for v in sel.getSubItems():
            self.combo1alist.append(v)
            self.liststore1a.append([ v.getText() ])
            v.index = index
            index = index + 1
            
    def on_combobox1a_changed(self, widget):
        idx = self.combobox1a.get_active()
        sel = self.combo1alist[idx]
        self.selected1a = sel
        self.combo2list = []
        index = 0
        for v in sel.getSubItems():
            self.combo2list.append(v)
            self.liststore2.append([ v.getText() ])
            v.index = index
            index = index + 1
    
    def on_combobox2_changed(self, widget):
        idx = self.combobox2.get_active()
        sel = self.combo2list[idx]
        self.selected2 = sel
            
    def on_button1_clicked(self, widget):
        valores = {}
        if self.selected1a == None or self.selected2 == None:
            self.showAlert("Existem campos requeridos que não foram preenchidos.")
            return
        
        valores['id_unid_organizacional_nivel1a'] = self.selected1a.getId()
        valores['id_unid_organizacional_nivel2'] = self.selected2.getId()
        valores['te_localizacao_complementar'] = self.entry1.get_text()
        valores['te_info_patrimonio1'] = self.entry2.get_text()
        valores['te_info_patrimonio2'] = self.entry3.get_text()
        valores['te_info_patrimonio3'] = self.entry4.get_text()
        valores['te_info_patrimonio4'] = self.entry5.get_text()
        valores['te_info_patrimonio5'] = self.entry6.get_text()
        valores['te_info_patrimonio6'] = self.entry7.get_text()
        if self.mc.save(valores):
            self.showInfo("Informações enviadas com sucesso!")
            gtk.main_quit()
        else:
            self.showAlert("Falha no envio das informações")
            gtk.main_quit()
        

class GUIMapaCacicAuth:
    """ 
        Classe de interface gráfica para o MapaCacic - Coletor Avulso de Patrimônio
    """
    
    def __init__(self):
        self.infoLabel = None
        self.infoWindow = None
        self.state = 0
        # caminhos
        self.ICON_PATH = "%s/img/logo.png" % Globals.PATH
        self.GLADE_PATH = '%s/glade/' % Globals.PATH
        self.TITLE = 'PyCacic - Coletor de Informações Patrimoniais'
        
    def show(self):
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'mapacacic_auth.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('mapacacic_auth')
        self.window.set_title(self.TITLE)
        
    def showAlert(self, msg):
        """Exibe janela do tipo Alert"""
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, msg)        
        dialog.set_title(self.TITLE)
        dialog.set_icon_from_file(self.ICON_PATH)
        dialog.width, dialog.height = dialog.get_size()
        dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
        op = dialog.run()
        dialog.destroy()
        return op
    
    def showInfo(self, txt):
        if self.infoWindow == None:
            self.infoWindow = self.xml.get_widget('infoWindow')
            self.infoLabel = self.xml.get_widget('label33')
        self.infoLabel.set_text(txt)
        if not self.infoWindow.props.visible:
            self.infoWindow.show_now()
        return self.infoWindow
    
    def on_mapacacic_auth_destroy(self, widget):
        if not state:
            gtk.main_quit()
        
    def on_buttonSair_clicked(self, widget):
        gtk.main_quit()
    
    def on_buttonOk_clicked(self, widget):
        entry1 = self.xml.get_widget("entry1")
        user = entry1.get_text();
        entry2 = self.xml.get_widget("entry2")
        pswd = entry2.get_text();
        infoWindow = self.showInfo("Autenticando...")
        
        mc = MapaCacic(user, pswd)
        if mc.auth():
            mc.getInfo()
            infoWindow.destroy()
            
            self.state = 1
            self.window.destroy()
            self.showPatr(mc)
        else:
            infoWindow.destroy()
            
            self.showAlert("Login incorreto.")
    
    def showPatr(self, mc):
        GUIMapaCacic(mc).show()
        
if __name__ == '__main__':
    try:
        GUIMapaCacicAuth().show()
        gtk.main()
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()