# -*- coding: UTF-8 -*-

"""

    Modulo col_hard
    
    Modulo com finalidade de coletar as informacoes
    de hardware e passar para o gerente de coletas (Ger_Cols)
    e o mesmo repassar ao servidor
    
    @author: Dataprev - ES
    
"""

import re
import sys
import commands
from coletor import *

class Col_Hard(Coletor):
    """Classe responsavel por coletar os dados de Hardware"""

    # nome do arquivo de saida (DAT)
    OUTPUT_DAT = 'col_hard.dat'

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        
    def getName(self):
        return "col_hard"
    
    def getUVCKey(self):
        return 'Coleta.Hardware'
    
    def isReady(self, dat):
        return self.getUVCDat(dat, self.getUVCKey()) != self.getChave('UVC')

    def setDicionario(self):
        """Monta o dicionario"""
        self.dicionario.clear()
        # INICIO
        self.addChave('Inicio', strftime("%H:%M:%S"))
        # CPUs
        # removido frequencia [old]=> CPUs = '#CPU#'.join(['#FIELD#'.join(['te_cpu_desc###%s' % i.getDescricao(), 'te_cpu_fabricante###%s' % i.getFabricante(), 'te_cpu_serial###%s' % i.getSerial(), 'te_cpu_frequencia###%s' % i.getFrequencia()]) for i in self.computer.getCPU()])
        CPUs = '#CPU#'.join(['#FIELD#'.join(['te_cpu_desc###%s' % i.getDescricao(), 'te_cpu_fabricante###%s' % i.getFabricante(), 'te_cpu_serial###%s' % i.getSerial()]) for i in self.computer.getCPU()])
        self.addChave('te_Tripa_CPU', CPUs)
        # Placas/Configuracoes de Redes
        TCPIP = '#TCPIP#'.join(['#FIELD#'.join(['te_placa_rede_desc###%s' % i.getDescricao(), 'te_node_address###%s' % i.getMAC().replace(':','-'), 'te_ip###%s' % i.getIP(), 'te_mascara###%s' % i.getMascara(), 'te_gateway###%s' % i.getGateway(), 'te_serv_dhcp###%s' % i.getDHCP()]) for i in self.computer.getPlacaRede()])
        self.addChave('te_Tripa_TCPIP', TCPIP)
        # CD/DVD ROM
        ROMs = '#CDROM#'.join(['te_cdrom_desc###%s' % i for i in self.computer.getRom()])
        self.addChave('te_Tripa_CDROM', ROMs)
        # Placa Mae
        self.addChave('te_placa_mae_fabricante', self.computer.getPlacaMae().getFabricante())
        self.addChave('te_placa_mae_desc', self.computer.getPlacaMae().getDescricao())
        # Placas de Video
        if len(self.computer.getVideo()) > 0:
            video = self.computer.getVideo()[0]
            cores = video.getCores()
            desc = video.getDescricao()
            vmem = video.getRam()
            resolucao = video.getResolucao()
        else:
            cores , desc, vmem, resolucao = '', '', '', ''
        self.addChave('qt_placa_video_cores', cores)
        self.addChave('te_placa_video_desc', desc)
        self.addChave('te_placa_video_resolucao', resolucao)
        self.addChave("qt_placa_video_mem", vmem)
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
        # FIM
        self.addChave('Fim', strftime("%H:%M:%S"))
    
    def getFirst(self, list):
        """Retorna o primeiro item da lista"""
        if len(list) > 0:
            return list[0]
        return ''
    
    