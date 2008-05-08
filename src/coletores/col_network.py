from coletor import *
from lib.computador import Rede
from lib.computador import Computador
import socket
import struct

class Col_Network(Coletor):
    """Classe responsavel por coletar os dados de TCP IP"""

    def __init__(self, computer):
        Coletor.__init__(self, computer)
        self.computer = computer

    def getName(self):
        return "col_network"
    
    def start(self):
        self.setDicionario()

    def setDicionario(self):
        """Monta o dicionario"""        
        for nw in self.computer.getPlacaRede():
            if nw.getIP() == self.computer.ip_ativo:
                net = nw
                break
        self.dicionario.clear()
        self.addChave("te_ip", self.computer.ip_ativo)        
        self.addChave('te_dns_primario', net.getDNS()[0])
        self.addChave('te_dns_secundario', net.getDNS()[1])
        self.addChave('te_dominio_dns', net.getDNSDomain())
        self.addChave('te_mascara', net.getMascara())
        self.addChave('te_nome_host', self.computer.getHostName())
        self.addChave('te_gateway', net.getGateway())
        self.addChave("te_serv_dhcp", net.getDHCP())
    
    