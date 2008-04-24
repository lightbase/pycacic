# -*- coding: UTF-8 -*-
import re
import sys
import commands
from time import strftime
from coletor import *
from lib.computador import * 

class Col_Hard(Coletor):
    """Classe responsavel por coletar os dados de Hardware"""

    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_hard.dat'

    def __init__(self):
        Coletor.__init__(self)
        self.computer = Computador()

    def start(self):
        self.setDicionario()
        self.createDat(self.dicionario, self.PATH + self.OUTPUT_DAT, 'Col_Hard.')

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        inicio = strftime("%H:%M:%S")
        # iniciando a coleta
        self.computer.coletar()
        # CPUs
        CPUs = '#CPU#'.join(['#FIELD#'.join(['te_cpu_desc###%s' % i.getDescricao(), 'te_cpu_fabricante###%s' % i.getFabricante(), 'te_cpu_serial###%s' % i.getSerial(), 'te_cpu_frequencia###%s' % i.getFrequencia()]) for i in self.computer.getCPU()])
        self.addChave('v_Tripa_CPU', CPUs)
        # Placas/Configuracoes de Redes
        TCPIP = '#TCPIP#'.join(['#FIELD#'.join(['te_placa_rede_desc###%s' % i.getDescricao(), 'te_node_address###%s' % i.getMAC().replace(':','-'), 'te_ip###%s' % i.getIP(), 'te_mascara###%s' % i.getMascara(), 'te_gateway###%s' % '', 'te_serv_dhcp###%s' % '']) for i in self.computer.getPlacaRede()])
        self.addChave('v_Tripa_TCPIP', TCPIP)
        # CD/DVD ROM
        ROMs = '#CDROM#'.join(['te_cdrom_desc###%s' % i for i in self.computer.getRom()])
        self.addChave('v_Tripa_CDROM', ROMs)
        # Placa Mae
        self.addChave('te_placa_mae_fabricante', self.computer.getVideo()[0].getDescricao())
        self.addChave('te_placa_mae_desc', self.computer.getPlacaMae())
        # Placas de Video
        self.addChave('qt_placa_video_cores', self.computer.getVideo()[0].getCores())
        self.addChave('te_placa_video_desc', self.computer.getVideo()[0].getDescricao())
        self.addChave("qt_placa_video_mem", self.computer.getVideo()[0].getRam())
        # Placas de Som
        self.addChave('te_placa_som_desc', self.getFirst(self.computer.getAudio()))
        # Memoria RAM
        self.addChave('qt_mem_ram', self.computer.getRam().getTamanho())
        self.addChave('te_mem_ram_desc', self.computer.getRam().getDescricao())
        # Bios
        self.addChave('te_bios_fabricante', self.computer.getBios().getFabricante())
        self.addChave('te_bios_data', self.computer.getBios().getData())
        self.addChave('te_bios_desc', self.computer.getBios().getDescricao())
        # Dispositivos
        self.addChave("te_teclado_desc", self.computer.getTeclado())
        self.addChave("te_mouse_desc", self.computer.getMouse())
        # Modem
        self.addChave("te_modem_desc", self.getFirst(self.computer.getModem()))
        # Ultimo Valor Coletado
        self.addChave('UVC', self.getUVC(self.dicionario))
        # INICIO-FIM
        self.addChave('Inicio', inicio)
        self.addChave('Fim', strftime("%H:%M:%S"))

    
    def dictToPost(self):
        """Devolve um dicionario para ser enviado para o Gerente Web"""
        d = {}        
        d['te_tripa_tcpip']           = self.encripta(self.dicionario['v_Tripa_TCPIP'])
        d['te_tripa_cpu']             = self.encripta(self.dicionario['v_Tripa_CPU'])
        d['te_tripa_cdrom']           = self.encripta(self.dicionario['v_Tripa_CDROM'])
        d['te_mem_ram_desc']          = self.encripta(self.dicionario['te_mem_ram_desc'])
        d['qt_mem_ram']               = self.encripta(self.dicionario['qt_mem_ram'])
        d['te_bios_desc']             = self.encripta(self.dicionario['te_bios_desc'])
        d['te_bios_data']             = self.encripta(self.dicionario['te_bios_data'])
        d['te_bios_fabricante']       = self.encripta(self.dicionario['te_bios_fabricante'])
        d['te_placa_mae_fabricante']  = self.encripta(self.dicionario['te_placa_mae_fabricante'])
        d['te_placa_mae_desc']        = self.encripta(self.dicionario['te_placa_mae_desc'])
        d['te_placa_video_desc']      = self.encripta(self.dicionario['te_placa_video_desc'])
        d['qt_placa_video_cores']     = self.encripta(self.dicionario['qt_placa_video_cores'])
        d['qt_placa_video_mem']       = self.encripta(self.dicionario['qt_placa_video_mem'])
        d['te_placa_som_desc']        = self.encripta(self.dicionario['te_placa_som_desc'])
        d['te_teclado_desc']          = self.encripta(self.dicionario['te_teclado_desc'])
        d['te_modem_desc']            = self.encripta(self.dicionario['te_modem_desc'])
        d['te_mouse_desc']            = self.encripta(self.dicionario['te_mouse_desc'])
        return d
    
    def getFirst(self, lista):
        """Retorna o primeiro elemento da lista, caso nao exista retorna '' """
        if len(lista) > 0:
            return lista[0]
        return ''
