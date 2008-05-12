#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade

import sys
from globals import Globals 

from socket import *


class GUI:

    ICON_PATH = "%s/img/logo.png" % Globals.PATH
    GLADE_PATH = '%s/glade/' % Globals.PATH
    TITLE = 'PyCacic'
      
    main_visible = False
    
    def __init__(self):
        self.createTray()
        self.mw = MainWindow()        
    
    def createTray(self):
        # TrayIcon
        self.statusIcon = gtk.StatusIcon()
        
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title(self.TITLE)
        self.window.connect('delete_event', self.delete_cb, self.statusIcon)
 
        self.menu = gtk.Menu()
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_ABOUT)
        self.menuItem.connect('activate', self.activate_icon_cb)
        self.menu.append(self.menuItem)
        self.menuItem = gtk.ImageMenuItem(gtk.STOCK_QUIT)
        self.menuItem.connect('activate', self.quit_cb, self.statusIcon)
        self.menu.append(self.menuItem)
        
        self.imageicon = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.ICON_PATH)
        scaled_buf = pixbuf.scale_simple(21, 23, gtk.gdk.INTERP_BILINEAR)
        self.statusIcon.set_from_pixbuf(scaled_buf)
        
        self.statusIcon.set_tooltip(self.TITLE)
        self.statusIcon.connect('activate', self.activate_icon_cb)
        self.statusIcon.connect('popup-menu', self.popup_menu_cb, self.menu)
        self.statusIcon.set_visible(True)
    
    def delete_cb(widget, event, data = None):
        if data:
            data.set_blinking(True)
        return False
        
    def quit_cb(self, widget, data = None):
        if data:
            dialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, 'Deseja realmente sair?')        
            dialog.set_title(self.TITLE)                
            dialog.set_icon_from_file(self.ICON_PATH)
            dialog.width, dialog.height = dialog.get_size()
            dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
            retorno = dialog.run()              
            if retorno == gtk.RESPONSE_YES:    
                self.quit()
            dialog.destroy()
            data.set_visible(False)
    
        
    def activate_icon_cb(self, widget, data = None):
        self.mw.toggleWindow()    
    
    def popup_menu_cb(self, widget, button, time, data = None):
        if button == 3:
            if data:
                data.show_all()
                data.popup(None, None, None, 3, time)


    def quit(self):
        """Fecha o programa"""
        print "Bye"
        gtk.main_quit(0)


class MainWindow(GUI):

    LOGIN_ROOT = ''
    
    visible = False
    current_text = ''

    def __init__(self):
        self.pre = '>'
        self.xml = gtk.glade.XML(self.GLADE_PATH + 'main_window.glade')
        self.xml.signal_autoconnect(self)
        self.window = self.xml.get_widget('main_window')
        self.connect()
    
    def connect(self):
        # Set the socket parameters
        self.host, self.port, self.buf, self.addr = Globals.getSocketAttr()
        self.udp_sock = socket(AF_INET, SOCK_DGRAM)
            
    
    def show(self):
        self.window.show()       
        
    def hide(self):
        self.window.hide()    
        
    def toggleWindow(self):
        """Exibe ou Esconde a janela principal"""
        if self.visible:
            self.hide()
        else:
            self.show()
        self.visible = not self.visible  

    def on_btn_executar_clicked(self, button):
        """Executa o ger_cols"""
        self.udp_sock.sendto('col_hard' , self.addr)
        self.udp_sock.close()
        
    def on_window_destroy(self, button):
        self.toggleWindow()

    def on_btn_ok_clicked(self, button):
        """ """
        LOGIN_ROOT = self.root_login_xml.get_widget("txt_senha").get_text()
        if LOGIN_ROOT != '':
            self.root_login_xml.get_widget("root_login").destroy()
            

if __name__ == '__main__':
    try:
        if not Globals.INSTALLED:
            raise Exception("O PyCacic nao esta configurado, favor configura-lo.")
        GUI()
        gtk.main()
    except Exception, e:
        print e
        import traceback
        traceback.print_exc()
