#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk, gtk.glade

import sys
import commands
from ger_cols import *
from config.io import * 
from egg.trayicon import TrayIcon

from socket import *


class GUI:

    ICON_PATH = "%s/img/logo.png" % sys.path[0]
    GLADE_PATH = '%s/glade/' % sys.path[0]
      
    main_visible = False
    
    def __init__(self):
        self.createTray()
        self.mw = MainWindow()
    
    def createTray(self):
        # TrayIcon
        self.tray = TrayIcon('pycacic')
        self.eventbox = gtk.EventBox()
        self.tray.add(self.eventbox)
        self.eventbox.connect("button_press_event", self.tray_icon_clicked)
        # Create the tooltip for the tray icon
        self.tooltip = gtk.Tooltips()
        # Configura imagem para o tray icon
        self.imageicon = gtk.Image()
        pixbuf = gtk.gdk.pixbuf_new_from_file(self.ICON_PATH)
        scaled_buf = pixbuf.scale_simple(23, 23, gtk.gdk.INTERP_BILINEAR)
        self.imageicon.set_from_pixbuf(scaled_buf)
        self.eventbox.add(self.imageicon)
        # Exibe o tray icon
        self.tray.show_all()
        self.tooltip.set_tip(self.tray,'pycacic')
    
    def tray_icon_clicked(self, signal, event):
        """ """
        if event.button == 3:
            PopupMenu().show_menu(event)
        else:
            self.mw.toggleWindow()

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
        # Set the socket parameters
        sock = Reader.getSocket()
        self.host = sock['host']
        self.port = int(sock['port'])
        self.buf  = int(sock['buffer'])
        self.addr = (self.host, self.port)
        self.udp_sock = socket(AF_INET, SOCK_DGRAM)
        self.udp_sock.sendto('col_hard' , self.addr)
        self.udp_sock.close()
        
    def on_window_destroy(self, button):
        self.toggleWindow()

    def on_btn_ok_clicked(self, button):
        """ """
        LOGIN_ROOT = self.root_login_xml.get_widget("txt_senha").get_text()
        if LOGIN_ROOT != '':
            self.root_login_xml.get_widget("root_login").destroy()
            

class PopupMenu(GUI):
    
    def __init__(self):     
        # Create menu items
        self.item_lang = gtk.MenuItem('Idioma', True)
        self.item_about = gtk.MenuItem('Sobre', True)
        self.item_exit = gtk.MenuItem('Sair', True)
        # Connect the events
        self.item_lang.connect('activate', self.conflang)
        self.item_about.connect('activate', self.about)                           
        self.item_exit.connect('activate', self.exit)
        # Create the menu
        self.menu = gtk.Menu()
        # Append menu items to the menu
        self.menu.append(self.item_lang)
        self.menu.append(self.item_about)        
        self.menu.append( self.item_exit)
        self.menu.show_all()

    def show_menu(self, event):
        # Display the menu
        self.menu.popup(None, None, None, event.button, event.time)
    
    def conflang(self, event):
        pass
    
    def about(self, event):
        pass               
    
    def exit(self, event):
        dialog = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO, 'Deseja realmente sair?')        
        dialog.set_title('PyCacic')                
        dialog.set_icon_from_file(self.ICON_PATH)
        dialog.width, dialog.height = dialog.get_size()
        dialog.move(gtk.gdk.screen_width()/2-dialog.width/2, gtk.gdk.screen_height()/2-dialog.height/2)
        retorno = dialog.run()              
        if retorno == gtk.RESPONSE_YES:            
            self.quit()                        
        dialog.destroy()

if __name__ == '__main__':
    try:
        GUI()
        gtk.main()
    except Exception, e:
        print e.message
