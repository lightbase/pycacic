# -*- coding: UTF-8 -*-
#!/usr/bin/env python

"""
    GUI
    
    Modulo de Interface Gráfica do PyCacic.
    
    Requisitos:
                - GTK+
                - pyGTK
                - Glade
                
                ps: StatusIcon a partir do pyGTK 2.10
    
    @author: Dataprev - ES

"""

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade, gobject

import sys
from time import strftime
from socket import *

from coletores.coletor import Coletor
from coletores.col_network import Col_Network

from config.io import Reader

from logs.log import CLog
from lang.language import Language
from globals import Globals 

_l = Language()

class GUI: 
    """
        Classe GUI
        class mae da interface grafica. Possui variaveis e metodos
        comuns para facilitar e auxiliar a interface grafica.
    """
    
    def __init__(self):
        # caminhos
        self.ICON_PATH = "%s/img/logo.png" % Globals.PATH
        self.GLADE_PATH = '%s/glade/' % Globals.PATH
        self.TITLE = _l.get('pycacic')
        # controle de janela
        self.visible = 0
        
    def show(self):
        raise NotImplementedError('%: GUI.show()' % _l.get('error_not_implemented'))
        
    def start(self):
        self.infoGeral = InfoGeral()
        self.logAtivit = LogAtividades()
        self.createTray()
        
    def connect(self):
        """Conecta ao socket para comunicar-se com o cacic.py"""
        # Set the socket parameters
        self.host, self.port, self.buf, self.addr = Globals.getSocketAttr()
        self.udp_sock = socket(AF_INET, SOCK_DGRAM)                
    
    def createTray(self):
        """Cria Icone na bandeja e menu popup (ao clicar-lo com o botao direito)"""
        # TrayIcon
        self.statusIcon = gtk.StatusIcon()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.TITLE)
        self.window.connect('delete_event', self.delete_cb, self.statusIcon)
 
        self.menu = gtk.Menu()
        
        self.menuItem = gtk.ImageMenuItem(_l.get('action_log'))
        self.menuItem.connect('activate', self.showLogAtividades)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(_l.get('settings'))
        self.menuItem.connect('activate', self.showConfiguracoes)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(_l.get('run_now'))
        self.menuItem.connect('activate', self.showExecAgora)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(_l.get('general_info'))
        self.menuItem.connect('activate', self.showInfoGeral)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(_l.get('patr_info'))
        self.menuItem.connect('activate', self.showInfoPatr)
        self.menu.append(self.menuItem)
        
        self.menuItem = gtk.ImageMenuItem(_l.get('exit'))
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.imageicon = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.ICON_PATH)
        scaled_buf = pixbuf.scale_simple(21, 23, gtk.gdk.INTERP_BILINEAR)
        self.statusIcon.set_from_pixbuf(scaled_buf)
        
        self.statusIcon.set_tooltip(self.TITLE)
        self.statusIcon.connect('activate', self.activate_icon_cb)
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(1)
    
    def delete_cb(widget, event, data = None):
        """Remove o menu popup"""
        if data:
            data.set_blinking(1)
        return 0
        
    def quit_cb(self, widget, data = None):
        """Exibe Janela Popup para confirmacao de saida."""
        if data:            
            self.showLogin(widget)
        
    def activate_icon_cb(self, widget, data = None):
        """Ao clicar com o botao esquerdo"""
        pass
    
    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)
                
    def on_window_destroy(self, widget):
        self.visible = 0
        widget.destroy()
        
    def socketSend(self):
        host, port, buf, addr = Globals.getSocketAttr()
        udp_sock = socket(AF_INET, SOCK_DGRAM)
        udp_sock.sendto('col_hard col_unid col_soft col_vamp col_network' , addr)
        udp_sock.close()
        print "ENVIADO"

    def quit(self):
        """Fecha o programa"""
        if self.showConfirm(_l.get('exit_confirm')) == gtk.RESPONSE_YES: 
            print "Bye"
            gtk.main_quit(0)
        
    def showConfirm(self, msg):
        """Exibe janela do tipo confirmacao (Cancel, OK) e retorna o valor escolhido"""
        dialog = gtk.MessageDialog(None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, msg)        
        dialog.set_title(self.TITLE)
        dialog.set_icon_from_file(self.ICON_PATH)
        dialog.width, dialog.height = dialog.get_size()
        dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
        op = dialog.run()
        dialog.destroy()
        return op
    
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
        
    def showWindow(self, widget, window):
        """Exibe a janela caso nao esteja aberta"""
        if not window.visible:
            window.show()
    
    def showLogin(self, widget):
        login = Login(self.quit)
        self.showWindow(widget, login)
        
    def showInfoGeral(self, widget):
        self.showWindow(widget, self.infoGeral)          
        
    def showLogAtividades(self, widget):
        self.showWindow(widget, self.logAtivit)           
        
    def showConfiguracoes(self, widget):
        login = Login('')
        self.showWindow(widget, login)
        
    def showExecAgora(self, widget):
        login = Login(self.socketSend)
        self.showWindow(widget, login)
        
    def showInfoPatr(self, widget):
        login = Login('')
        self.showWindow(widget, login)


class Login(GUI):
    """
        Classe Login
    """

    def __init__(self, action=''):
        GUI.__init__(self)
        self.action = action
        
    def show(self):
        self.visible = 1
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'login.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('login_window')
        self.input = self.xml.get_widget('txt_senha')
        
    def on_btn_ok_clicked(self, widget):
        """Verifica se senha informada e valida e pede confirmacao de saida"""
        from config.io import Reader
        if self.input.get_text() == Reader.getPycacic()['password']:               
            self.action()
        else:
            self.showAlert('Senha Invalida.')
        self.on_window_destroy(self.window)

class LogAtividades(GUI):
    """
        Classe LogAtividades
        Para controlar as acoes da janela correspondente a exibicao do
        log do Sistema
    """

    def __init__(self):
        GUI.__init__(self)
        
    def show(self):
        self.visible = 1
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'log_atividades.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('log_atividades')
        # Label
        self.xml.get_widget('lb_log').set_text(_l.get('action_log'))
        # TreeView
        self.tv_log = self.xml.get_widget('tv_log')
        self.tv_log_model = gtk.ListStore(str, str, str)
        self.setTreeViews()
        self.setTreeViewsValues()
        # callback
        gobject.timeout_add(10000, self.setTreeViewsValues)
        
    def setTreeViews(self):
        self.tv_log.set_model(self.tv_log_model)
        coluna1 = gtk.TreeViewColumn(_l.get('date'), gtk.CellRendererText(), text=0)
        coluna1.set_reorderable(1)
        coluna2 = gtk.TreeViewColumn(_l.get('module'), gtk.CellRendererText(), text=1)
        coluna2.set_reorderable(1)
        coluna3 = gtk.TreeViewColumn(_l.get('action'), gtk.CellRendererText(), text=2)
        coluna3.set_reorderable(1)
        coluna1.set_resizable(1)
        coluna2.set_resizable(1)
        coluna3.set_resizable(1)
        self.tv_log.append_column(coluna1)
        self.tv_log.append_column(coluna2)
        self.tv_log.append_column(coluna3)
        
    def setTreeViewsValues(self):
        self.tv_log_model.clear()
        f = CLog.getCurrentFile()
        for lines in f.split('\n'):
            values = lines.split(CLog.STRP)
            if len(values) == 3:
                self.tv_log_model.append(values)
        return 1
                        
        
class InfoGeral(GUI):
    """
        Classe InfoGeral
        Para controlar as acoes da janela correspondente a exibicao das
        Informacoes Gerais do Sistema
    """

    def __init__(self):
        GUI.__init__(self)
        self.col = Coletor(None)
        self.cn = Col_Network(None)
        
    def show(self):
        self.visible = 1
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'info_geral.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('info_geral')
        # Labels
        self.xml.get_widget('lb_main').set_text(_l.get('app_server'))
        self.xml.get_widget('lb_host_name').set_text('"%s"' % Reader.getServer()['address'])
        self.xml.get_widget('lb_tcp_ip').set_text(_l.get('network_settings'))
        self.xml.get_widget('lb_sis_monitor').set_text(_l.get('systems_monit_on'))
        self.xml.get_widget('lb_cols').set_text('%s (%s)' % (_l.get('cols_on_this_date'), strftime('%d/%m/%Y')))
        # TreeViews
        self.tv_tcp_ip = self.xml.get_widget('tv_tcp_ip')
        self.tv_tcp_model = gtk.ListStore(str, str)
        # SISTEMAS MONITORADOS
        self.tv_sis_monitor = self.xml.get_widget('tv_sis_monitor')
        self.tv_sis_model = gtk.ListStore(str, str, str)
        # COLETAS
        self.tv_cols = self.xml.get_widget('tv_cols')
        self.tv_cols_model = gtk.ListStore(str, str, str, str)
        # monta e popula as treeviews
        self.setTreeViews()
        self.setTreeViewsValues()
        
    def setTreeViews(self):
        # TCP IP
        self.tv_tcp_ip.set_model(self.tv_tcp_model)
        coluna1 = gtk.TreeViewColumn(_l.get('item'), gtk.CellRendererText(), text=0)
        coluna2 = gtk.TreeViewColumn(_l.get('value'), gtk.CellRendererText(), text=1)
        coluna1.set_resizable(1)
        coluna2.set_resizable(1)
        self.tv_tcp_ip.append_column(coluna1)
        self.tv_tcp_ip.append_column(coluna2)
        # SISTEMAS MONITORADOS
        self.tv_sis_monitor.set_model(self.tv_sis_model)
        coluna1 = gtk.TreeViewColumn(_l.get('name'), gtk.CellRendererText(), text=0)
        coluna2 = gtk.TreeViewColumn(_l.get('license'), gtk.CellRendererText(), text=1)
        coluna3 = gtk.TreeViewColumn(_l.get('version'), gtk.CellRendererText(), text=2)
        coluna1.set_resizable(1)
        coluna2.set_resizable(1)
        coluna3.set_resizable(1)
        self.tv_sis_monitor.append_column(coluna1)
        self.tv_sis_monitor.append_column(coluna2)
        self.tv_sis_monitor.append_column(coluna3)
        # COLETORES
        self.tv_cols.set_model(self.tv_cols_model)
        coluna1 = gtk.TreeViewColumn(_l.get('module'), gtk.CellRendererText(), text=0)
        coluna2 = gtk.TreeViewColumn(_l.get('start'), gtk.CellRendererText(), text=1)
        coluna3 = gtk.TreeViewColumn(_l.get('end'), gtk.CellRendererText(), text=2)
        coluna4 = gtk.TreeViewColumn(_l.get('status'), gtk.CellRendererText(), text=3)
        coluna1.set_resizable(1)
        coluna2.set_resizable(1)
        coluna3.set_resizable(1)
        coluna4.set_resizable(1)
        self.tv_cols.append_column(coluna1)
        self.tv_cols.append_column(coluna2)
        self.tv_cols.append_column(coluna3)
        self.tv_cols.append_column(coluna4)
        
    def setTreeViewsValues(self):        
        itens = {
             _l.get('host_name')            :  'te_nome_host',
             _l.get('host_ip_address')      :  'te_ip',
             _l.get('net_ip_address')       :  'te_ip_rede',
             _l.get('mac_address')          :  'te_mac',
             _l.get('net_mask')             :  'te_mascara',
             _l.get('dns_domain_server')    :  'te_dominio_dns',
             _l.get('primary_dns_server')   :  'te_dns_primario',
             _l.get('secondary_dns_server') :  'te_dns_secundario',
             _l.get('default_gateway')      :  'te_gateway',
             _l.get('dhcp_server')          :  'te_serv_dhcp',
        }
        # TCP/IP INFO
        network = self.cn.getDatToDict('/tmp/%s' % self.cn.OUTPUT_DAT)
        self.tv_tcp_model.clear()
        for i in itens.keys():
            try:
                self.tv_tcp_model.append([i, network[itens[i]]])
            except:
                pass
        # COLLECTIONS INFO
        coletores = self.col.getDatToDict('%s/cacic2.dat' % Globals.PATH, '')
        #print coletores['Coletas.Realizadas'] 


if __name__ == '__main__':
    try:
        if not Globals.INSTALLED:
            pass
            #raise Exception("O PyCacic nao esta configurado, favor configura-lo.")
        GUI().start()
        gtk.main()
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()
