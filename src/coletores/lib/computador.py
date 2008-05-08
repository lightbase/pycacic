# -*- coding: UTF-8 -*-

"""

	Modulo computador from Linux
	
	Modulo com finalidade de coletar informacoes sobre
	o computador (hardware, SO, network) utilizando o aplicativo
	lshw e comandos Linux.  
	
	@author: Dataprev - ES
	@version: 1.2.0 (14 de abril de 2008)
	
"""

import re
import os
import sys
import stat
import commands
import socket, fcntl, struct
from xml.dom import minidom, Node


DEFAULT_STRING_VALUE = ''


class ComputerException(Exception):
	"""Classe ComputerException, para exibir mensagens de exceptions"""
	
	def __init__(self, msg):
		Exception.__init__(self)
		self.message = msg
		
	def getMessage(self):
		"""Retorna a mensagem de Erro"""
		return self.message
	
class MotherBoard:
	"""Classe MotherBoard, contém informações sobre a Placa Mae"""
	
	def __init__(self):
		self.fabricante = ''
		self.descricao = ''
		
	def getDescricao(self):
		"""Retorna o a descricao da placa mae"""
		return self.descricao
	
	def getFabricante(self):
		"""Retorna o fabricante da placa mae"""
		return self.fabricante

class CPU:
	"""Classe CPU, contém informações sobre a CPU"""
	
	def __init__(self) :
		self.id = 0
		self.serial = DEFAULT_STRING_VALUE # string
		self.frequencia = 0.0 # double
		self.descricao = DEFAULT_STRING_VALUE # string
		self.fabricante = DEFAULT_STRING_VALUE # string

	def getId(self):
		"""Retorna o Id da CPU"""
		return self.id
	
	def setId(self, id):
		"""Define o Id da CPU"""
		self.id = id
	
	def getFrequencia (self) :
		""" retorna frequencia da CPU """
		# returns double
		return self.frequencia
	
	def setFrequencia(self, frequencia) :
		""" seta Frequencia(string) """
		# returns 
		self.frequencia = frequencia	
	
	def getFabricante (self) :
		""" retorna fabricante da CPU """
		# returns string
		return self.fabricante	
	
	def setFabricante (self, fabricante) :
		""" seta fabricante da CPU	 """
		# returns 
		self.fabricante = fabricante	
	
	def getDescricao (self) :
		""" retornadescricao da CPU """
		# returns string
		return self.descricao	
	
	def setDescricao (self, descricao) :
		""" seta descricao da CPU """
		# returns 
		self.descricao = descricao	
	
	def getSerial (self) :
		""" retorna serial da CPU """
		# returns string
		return self.serial	
	
	def setSerial (self, serial) :
		""" seta Serial da CPU """
		# returns 
		self.serial = serial
	
	
class Video :
	"""Classe contendo as informacoes de vídeo"""
	
	def __init__(self) :
		self.cores = 0 # int
		self.ram = 0.0 # double
		self.descricao = DEFAULT_STRING_VALUE # string
		
	def getRam (self) :
		""" retorna a quantidade de memoria ram do video """
		# returns double
		return self.ram
		
	def setRam (self, ram) :
		""" define a quantidade de ram do video """
		# returns 
		self.ram = ram
		
	def getCores (self) :
		""" retorna a quantidade de cores do video """
		# returns int
		return self.cores
		
	def setCores (self, cores) :
		""" define a quantidade de cores """
		# returns 
		self.cores = cores
		
	def getDescricao (self) :
		""" retorna a descricao da placa de video. """
		# returns string
		return self.descricao
		
	def setDescricao (self, descricao) :
		""" define a descricao da placa de video """
		# returns 
		self.descricao = descricao


class RAM :
	"""Classe contendo as informacoes de memoria ram"""
	
	def __init__(self) :
		self.tamanho = 0.0 # double
		self.slot = {}
		
	def setSlot(self, slot, size, desc):
		"""Seta o slot com tamanho e descricao"""
		self.slot[slot] = (size, desc)
		
	def getSlot(self, slot):
		"""Devolve uma tupla com tamanho [0] e descricao [1] do slot"""
		return self.slot[slot]
		
	def getTamanho (self) :
		""" retorna a quantidade de memoria ram"""
		# returns double
		return self.tamanho	
	
	def setTamanho (self, ram) :
		""" define a quantidade de ram do video """
		# returns 
		self.tamanho = ram	
		
	def getDescricao (self):
		""" retorna a descricao da ram """
		# returns string				
		chaves = self.slot.keys()
		chaves.sort()
		return ' - '.join(['Slot %s: %s(%s)' % (x, self.slot[x][0], self.slot[x][1]) for x in chaves])
		
	def toString(self):
		s = 'Tamanho Total (Mb): %s \n' % self.getTamanho()
		s += ''.join(['Slot %s: %s \n' % (self.slot[slot][0], self.slot[slot][1]) for slot in self.slot.keys()])
		return s


class Rede:
	"""Classe responsável por conter as informações de rede"""
	
	def __init__(self):
		self.ip = ''
		self.mac = ''
		self.mascara = ''
		self.iprede = ''
		self.dhcp = ''
		self.gateway = ''
		self.descricao = ''
		self.fabricante = ''
		self.logicalname = ''
		self.dns = self.__getDNS__()
		self.dnsdomain = self.__getDNSDomain__()
		
	def getIPAtivo(self, server):
		"""Retorna o endereco de IP que conecta no server especificado"""
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		return self.__getIp__(server)
		
	def __connect__(self, server_ip, port = 80):
		"""
			Conecta ao servidor atraves de socket
			Connect into server by socket
		"""
		self.s.connect((server_ip, port))
	
	def __disconnect__(self):
		"""
			Desconecta o socket
			Socket disconnect
		"""
		self.s.close()
		
	def __testIp__(self, ip_list, server, port = 80):
		"""
			Testa a lista de IP passada procurando qual endereco
			consegue conectar ao servidor
		"""
		try:
			self.__connect__(server, port)
			output = commands.getoutput('netstat -n | grep ' + server)
			netstat = self.__getIpList__(output)
			for ip in ip_list:			
				if ip in netstat:					
					return ip
			return ''
		finally:
			self.__disconnect__()		
		
	def __getIpList__(self, output):
		"""
			Expressao regular para montar uma lista de enderecos IP
			Regular Expression for to make a IP address list 
		"""
		p = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
		return p.findall(output)

	def __getIp__(self, server):
		"""
			Pega todos os enderecos IP atraves do comando 'ifconfig'
			e valida-o tentando conectar ao servidor, retornando o IP validado
			
			Get all IP address by the 'ifconfig' command output and
			try connect to server, return the valid address  
		"""
		ips = self.__getIpList__(commands.getoutput("ifconfig -a | grep 'inet'"))
		return self.__testIp__(ips, server)		
	
	def __getMask__(self, ip):
		"""
			Pega a Mascara de rede atraves do IP validado
			Get the net mask by the valid IP address
		"""
		mask = self.__getIpList__(commands.getoutput("ifconfig -a | grep " + ip))
		if len(mask) > 1:
			return mask[2]
		return ''
	
	def __getIPRede__(self, ip, netmask):
		"""
			Pega a o IP da Rede referente ao IP da maquina e mascara
			Gets the Network IP based on this machine IP and the mask.
		"""
		longnetmask = struct.unpack('!I', socket.inet_aton(netmask))[0]
		longip = struct.unpack('!I', socket.inet_aton(ip))[0]
		longnetwork = longnetmask & longip
		network = socket.inet_ntoa(struct.pack("!I", longnetwork))
		return network
	
	def __getMac__(self, ip):
		"""
			Pega o endereco Mac de rede atraves do IP
			Get the net mac address by the IP address
		"""
		p = re.compile('[0-9A-F]{2}(?:\:[0-9A-F]{2}){5}')
		return p.findall(commands.getoutput("ifconfig -a | grep -B 1 -A 1 " + ip))[0]
	
	def __getGateway__(self, logicalname):
		"""Pega o endereco do Default Gateway"""
		ls = commands.getoutput("netstat -rn | grep " + logicalname).split('\n')
		for l in ls: 
			if self.__getIpList__(l)[0] == '0.0.0.0':
				return self.__getIpList__(l)[1]
		return ''
	
	def __getDNS__(self):
		"""Pega os enderecos do DNS (primario, secundario)"""
		dns = self.__getIpList__(commands.getoutput("cat /etc/resolv.conf"))
		if len(dns) == 2:
			return dns
		return ['', ''] 
	
	def __getDNSDomain__(self):
		""" Pega o domínio """
		dns = commands.getoutput("cat /etc/resolv.conf")
		pos = dns.find("search ")
		if pos != -1:
			pos2 = dns.find("\n", pos)
			if pos2 != -1:
				return dns[pos+len("search "):pos2]
			else:	
				return dns[pos+len("search "):]
		return ""
		
		
		
	
	def __getDHCP__(self, ip):
		"""Pega o endereco do servidor DHCP"""
		dhpc_cmd = ["cat /var/lib/dhclient/*", "cat /var/lib/dhcp/*", "cat /var/lib/dhcp3/*"]
		p = re.compile('lease \{(?:\n|.)*?\}')
		for cmd in dhpc_cmd:
			leases = p.findall(commands.getoutput(cmd))
			for lease in leases:
				if ip in lease:
					return self.__getIpList__(lease[lease.find('dhcp-server'):])[0]
		return ''			
	
	def getIPRede(self, ip):
		""" retorna a descricao da placa de rede """
		# returns string
		return self.iprede
	
	def getDescricao(self):
		""" retorna a descricao da placa de rede """
		# returns string
		return self.descricao
	
	def getFabricante(self):
		""" retorna o fabricante da placa de rede """
		# returns string
		return self.fabricante
	
	def getLogicalName(self):
		""" retorna o o nome logico da placa de rede """
		# returns string
		return self.logicalname
	
	def getIP(self):
		""" retorna o endereco ip da maquina """
		# returns string
		return self.ip
	
	def getDHCP(self):
		""" retorna o endereço IP do servidor DHCP """
		return self.dhcp
	
	def getMascara(self):
		""" retorna a máscara de rede da máquina """
		# returns string
		return self.mascara
	
	def getGateway(self):
		""" retorna o enderedo do gateway"""
		# returns string
		return self.gateway
	
	def getMAC(self):
		""" retorna o endereco mac da máquina """
		# returns string
		return self.mac
	
	def getDHCP(self):
		""" retorna o endereco do servidor DHCP """
		# returns string
		return self.dhcp
	
	def getDNS(self):
		""" retorna os enderecos do DNS (primario, secundario) """
		# returns string
		return self.dns
	
	def getDNSDomain(self):
		""" retorna o domínio do DNS """
		#return string
		return self.dnsdomain
	
	
class Bios:
	"""Classe responsável por conter as informações da Bios"""
	
	def __init__(self) :
		self.data = DEFAULT_STRING_VALUE # string
		self.fabricante = DEFAULT_STRING_VALUE # string
		self.descricao = DEFAULT_STRING_VALUE # string
		
	def getData (self) :
		""" retorna a data da Bios """
		# returns string
		return self.data
		
	def setData (self, data) :
		""" define a data da Bios """
		# returns 
		self.data = data
		
	def getFabricante (self) :
		""" retorna o fabricante da Bios """
		# returns string
		return self.fabricante
		
	def setFabricante (self, fabricante) :
		""" define o fabricante da Bios """
		# returns 
		self.fabricante = fabricante
		
	def getDescricao (self) :
		""" retorna o fabricante da Bios """
		# returns string
		return self.descricao
		
	def setDescricao (self, descricao) :
		""" define a descricao da Bios """
		# returns 
		self.descricao = descricao


class HardDisk:
	"""Classe responsável por conter as informações sobre o HD"""
	
	def __init__(self) :
		self.tamanho = 0.0 # double
		self.fabricante = DEFAULT_STRING_VALUE # string
		self.descricao = DEFAULT_STRING_VALUE # string
		
	def getFabricante (self) :
		""" retorna o Fabricante do HD """
		# returns string
		return self.fabricante
		
	def setFabricante (self, fabricante) :
		""" seta Fabricante	 """
		# returns 
		self.fabricante = fabricante
		
	def getDescricao (self) :
		""" retorna descricao do HD """
		# returns string
		return self.descricao
		
	def setDescricao (self, descricao) :
		""" seta descricao do HD """
		# returns 
		self.descricao = descricao
		
	def getTamanho (self) :
		""" retorna o tamanho do HD (MB) """
		# returns double
		return self.tamanho
		
	def setTamanho (self, tamanho) :
		""" seta tamanho do HD """
		# returns 
		self.tamanho = tamanho
		
		
		
class PC_XML:
	"""
		Classe intermediária responsavel por executar o binario lshw,
		que ira gerar um xml, e entao tratar o xml setando os atributos
		do Computador atraves do mesmo e por comandos bash.
	"""	
	   
	def __init__(self):
		try:
			self.placaMae = MotherBoard()
			self.ram = RAM() # RAM
			self.rom = [] # list (rom drivers - CD, DVD)			
			self.placaRede = [] # list
			self.hardDisk = [] # list
			self.bios = Bios() # Bios
			self.video = [] # list
			self.audio = [] # list
			self.cpu = [] # list
			self.modem = [] # list
			# inicia leitura do XML			
			self.readXML() 
		except ComputerException, e:
			raise ComputerException(e.message)
	
	def getXML(self):
		"""Executa o binario para gerar arquivo xml com as informacoes do hardware"""
		lshw = "%s/coletores/lib/lshw" % sys.path[0]
		if os.path.exists(lshw):
			# modificando a permissao do arquivo
			if stat.S_IMODE(os.lstat(lshw)[stat.ST_MODE]) < 448:
				os.chmod(lshw, 777)
			return commands.getoutput(lshw + " -xml")
		else:
			raise ComputerException('Erro ao executar o lshw, arquivo nao encontrado')
		
	def readXML(self):
		"""Le o arquivo xml (String) gerado"""
		try:
			# percorrendo o xml
			xml = minidom.parseString(self.getXML())
			root = xml.getElementsByTagName('node')[0]
			for no in root.childNodes:
				if no.nodeType == Node.ELEMENT_NODE:
					atributos = no.attributes
					for a in atributos.keys():
						valor = atributos.get(a).nodeValue
						if a == 'id' and valor == 'core':
							self.getPlacaMaeInfo(no)
							return
		except ComputerException, e:
			raise ComputerException(e.message)
		except Exception, e:
			raise ComputerException('Erro ao abrir arquivo XML, formato inesperado')
		
	def getPlacaMaeInfo(self, no):
	    """Pega as informacoes da Placa Mae atraves do no do XML """
	    for filho in no.childNodes:
	        if filho.nodeName == 'product':
	        	self.placaMae.descricao = filho.firstChild.nodeValue
	        if filho.nodeName == 'vendor':
	        	self.placaMae.fabricante = filho.firstChild.nodeValue
	        if filho.nodeName == 'node':
	            atributos = filho.attributes
	            for a in atributos.keys():
	                valor = atributos.get(a).nodeValue
	                if a == 'id' and valor == 'firmware':
	                    self.getBiosInfo(filho)
	                if a == 'id' and valor == 'memory':
	                    self.getMemoriaInfo(filho)
	                if a == 'id' and valor[0:3] == 'cpu':
	                    self.getCPUInfo(filho)
	                if a == 'id' and valor[0:3] == 'pci':
	                    self.getPCIInfo(filho)
	                if a == 'id' and valor == 'bridge':
 						self.getRedeInfo(filho)

	def getBiosInfo(self, no):
	    """Pega as informacoes da Bios atraves do no do XML """
	    for filho in no.childNodes:
	        if filho.nodeName == 'vendor':
	        	self.bios.setFabricante(filho.firstChild.nodeValue)
	        if filho.nodeName == 'version':
	            # expressao regular para pegar data da bios
	            p = re.compile('[0-9][1-9]/[0-9][1-9]/[1-9][0-9][0-9][0-9]')
	            self.bios.setData(p.findall(filho.firstChild.nodeValue)[0])
	            self.bios.setDescricao(filho.firstChild.nodeValue)

	def getMemoriaInfo(self, no):
	    """Pega as informacoes da Memoria RAM atraves do no do XML """
	    descricao = ""
	    for filho in no.childNodes:
	        if filho.nodeName == 'size':
	            # como resultado pego esta em bytes converte para megas
	            self.ram.setTamanho((int(filho.firstChild.nodeValue)/1048576))
	        # monta uma unica string contendo informacoes sobre os slots
	        if filho.nodeName == 'node':
	            slot = ""
	            size = ""
	            desc = ""
	            hasSize = False
	            for folha in filho.childNodes:
	                if folha.nodeName == 'description':
	                    desc = folha.firstChild.nodeValue
	                if folha.nodeName == 'physid':
	                    slot = folha.firstChild.nodeValue
	                if folha.nodeName == 'size':
	                    size = (int(folha.firstChild.nodeValue)/1048576)
	                    hasSize = True
	                if hasSize == True:
	                	self.ram.setSlot(slot, size, desc)
	                	hasSize = False

	def getCPUInfo(self, no):
		"""Pega as informacoes do Processador atraves do no do XML """
		c = CPU()
		c.setId(no.attributes.get('id').nodeValue[4:])
		for filho in no.childNodes:
		    if filho.nodeName == 'product':
		    	c.setDescricao(filho.firstChild.nodeValue)
		    if filho.nodeName == 'vendor':
		    	c.setFabricante(filho.firstChild.nodeValue)
		    if filho.nodeName == 'serial':
		    	c.setSerial(filho.firstChild.nodeValue)
		    if filho.nodeName == 'size':
		        # "converte" a frequencia de Hz para GHz
		        c.setFrequencia((int(filho.firstChild.nodeValue)/1000000))
		if c.getDescricao() != "":
			self.cpu.append(c)
		# Caso exista um novo processador mas a descrição está vazia
		# assuma que sao mais de um nucleo e replica as informacoes do
		# ultimo adicionado
		elif len(self.cpu) > 0:
			c.setDescricao(self.cpu[len(self.cpu)-1].getDescricao())
			c.setFabricante(self.cpu[len(self.cpu)-1].getFabricante())
			c.setSerial(self.cpu[len(self.cpu)-1].getSerial())
			c.setFrequencia(self.cpu[len(self.cpu)-1].getFrequencia())
			self.cpu.append(c)

	def getPCIInfo(self, no):
		"""Pega as informacoes do PCI atraves do no do XML"""
 		for filho in no.childNodes:
 			if filho.nodeName == 'node':
 				atributos = filho.attributes
 				for a in atributos.keys():
 					valor = atributos.get(a).nodeValue
 					# recursividade
 					if a == 'id' and valor[0:3] == 'pci':
 						self.getPCIInfo(filho)
 					if a == 'id' and valor == 'multimedia':
 						self.getAudioInfo(filho)
 					if a == 'id' and valor == 'display':
 						self.getVideoInfo(filho)
 					if a == 'id' and valor[0:3] == 'ide':
 						self.getIDEInfo(filho)
 					if a == 'id' and valor in ('network', 'bridge'):
 						self.getRedeInfo(filho)
 					if a == 'id' and valor == 'communication':
 						self.getModemInfo(filho)
 					if a == 'id' and valor == 'storage':
 						self.getStorageInfo(filho)
                   
	def getAudioInfo(self, no):
	    """Pega as informacoes Multimedia atraves do no do XML """
	    desc1 = ""
	    desc2 = ""
	    for filho in no.childNodes:
	        if filho.nodeName == 'vendor':
	            desc1 = filho.firstChild.nodeValue
	        if filho.nodeName == 'product':
	            desc2 = filho.firstChild.nodeValue	                    
	    self.audio.append(desc1 + ' - ' + desc2)
    
	def getVideoInfo(self, no):
	    """Pega as informacoes de Video atraves do no do XML"""
	    video = Video()
	    desc1 = ""
	    desc2 = ""
	    for filho in no.childNodes:
	        if filho.nodeName == 'vendor':
	            desc1 = filho.firstChild.nodeValue
	        if filho.nodeName == 'product':
	            desc2 = filho.firstChild.nodeValue
	        if filho.nodeName == 'width':
	        	video.setCores(filho.firstChild.nodeValue)
	    video.setDescricao(desc1 + ' - ' + desc2)
	    video.setRam(self.getVideoSystemInfo())  
	    self.video.append(video)  
                        
	def getVideoSystemInfo(self):
	    """Pega as informacoes de Video atraves da linhad e comando"""
	    s = commands.getoutput("grep -i video /var/log/Xorg.0.log")
	    s = s.lower()
	    pesqBus = s.find("videoram:")
	    if(pesqBus > 0):
	        primeiro = pesqBus+10
	        fim = (s.find("k",primeiro))
	        if(primeiro > 0 and fim > 0):
	            return int(s[primeiro:fim])/1024  
	    return DEFAULT_STRING_VALUE
  
	def getIDEInfo(self, no):
	    """Pega as informacoes de IDE atraves do no do XML"""
	    for filho in no.childNodes:
	        if filho.nodeName == 'node':
	            atributos = filho.attributes
	            for a in atributos.keys():
	                valor = atributos.get(a).nodeValue
	                # recursividade
	                if a == 'id' and valor[0:3] == 'ide':
	                    self.getIDEInfo(filho)
	                if a == 'id' and valor[0:4] == 'scsi':
	                    self.getSCSIInfo(filho)
	                if a == 'id' and valor[0:5] == 'cdrom':
	                	self.getCDROMInfo(filho)

	def getSCSIInfo(self, no):
		"""Pega as informacoes de SCSI atraves do no do XML"""
		self.getIDEInfo(no)

	def getRedeInfo(self, no):
	    """Pega as informacoes da Placa de REde atraves do no do XML"""
	    rede = Rede()
	    for filho in no.childNodes:
	    	if filho.nodeName == 'vendor':
	    		rede.fabricante = filho.firstChild.nodeValue
	    	if filho.nodeName == 'product':
	    		rede.descricao = filho.firstChild.nodeValue
	    	if filho.nodeName == 'product':
	    		rede.descricao = filho.firstChild.nodeValue
	    	if filho.nodeName == 'serial':
	    		rede.mac = filho.firstChild.nodeValue.upper()
	    	if filho.nodeName == 'logicalname':
	    		rede.logicalname = filho.firstChild.nodeValue
	    		rede.gateway = rede.__getGateway__(rede.logicalname)
	    	# pegando o ip
	    	if filho.nodeName == 'configuration':
	    		for i in filho.childNodes:
	    			if i.nodeType == Node.ELEMENT_NODE and i.nodeName == 'setting' and i.attributes['id'].nodeValue == 'ip':
    					rede.ip = i.attributes['value'].nodeValue
    					rede.dhcp = rede.__getDHCP__(rede.ip)
    					rede.mascara = rede.__getMask__(rede.ip)    	
    					rede.iprede = rede.__getIPRede__(rede.ip, rede.mascara)	
    					self.placaRede.append(rede)
    					return

	def getModemInfo(self, no):
		"""Pega as informacoes da Placa de Fax Modem atraves do no do XML"""
		desc = []
		for filho in no.childNodes:
			if filho.nodeName == 'vendor':
				desc.append(filho.firstChild.nodeValue)
			if filho.nodeName == 'product':
				desc.append(filho.firstChild.nodeValue)
		self.modem.append(' - '.join(desc))

	def getCDROMInfo(self, no):
		"""Pega as informacoes do CD-ROM atraves do no do XML """
		desc = []
		for filho in no.childNodes:
			if filho.nodeName == 'vendor':
				desc.append(filho.firstChild.nodeValue)
			if filho.nodeName == 'description':
				desc.append(filho.firstChild.nodeValue)
			if filho.nodeName == 'product':
				desc.append(filho.firstChild.nodeValue)
		self.rom.append(' - '.join(desc))
		
	def getStorageInfo(self, no):
		"""Pega as informacoes de armazanagem atraves do no do XML"""
		for filho in no.childNodes:
			if filho.nodeName == 'node':
				atributos = filho.attributes
				for a in atributos.keys():
					valor = atributos.get(a).nodeValue
					if a == 'id' and valor[0:4] == 'disk':
						self.getHardDiskInfo(filho)
		
	def getHardDiskInfo(self, no):
		"""Pega as informacoes do HD atraves do no do XML """
		hd = HardDisk()
		for filho in no.childNodes:
			if filho.nodeName == 'vendor':
				hd.setFabricante(filho.firstChild.nodeValue)
			if filho.nodeName == 'product':
				hd.setDescricao(filho.firstChild.nodeValue)
			if filho.nodeName == 'size':
				# convertendo de bytes para megas
				hd.setTamanho(int(filho.firstChild.nodeValue) / 1024)
		self.hardDisk.append(hd)
    

class SO_Info:
	"""
		Responsavel por pegar atraves de arquivos de configuracao
		a distribuicao Linux do usuario
		
		Distribuicoes reconhecidas: 	
			Debian - Ubuntu - Kurumin - Red Hat - Mandrake - Puppy Linux
			Kinoppix - PLD Linux - Pardus - Xandros - Gentoo - Arch - Zenwalk
			Yellow dog - SuSE - Solaris - Sparc - Sun JDS - Slackware
	"""
	
	def getSO():
		"""
			Retorna a distribuicao Linux que o usuario
			esta usando 
		"""
		# Debian - Ubuntu - Kurumin
		if(os.path.exists("/etc/debian_version")):
			descr = "Debian"
			version = commands.getoutput("cat /etc/debian_version")
			if(os.path.exists("/etc/lsb-release")):
				descr = "Ubuntu"
				version = commands.getoutput("cat /etc/lsb-release")
				pos = version.find("_RELEASE=")+9
				version = version[pos:version.find("\n",pos)]
			elif(os.path.exists("/etc/kurumin_version")):
				descr = "Kurumin"
				version = commands.getoutput("cat /etc/kurumin_version")
		# Red Hat
		elif(os.path.exists("/etc/redhat-release")):
			descr = commands.getoutput("cat /etc/redhat-release")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Mandrake
		elif(os.path.exists("/etc/mandrake-release")):
			descr = commands.getoutput("cat /etc/mandrake-release")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Puppy Linux
		elif(os.path.exists("/etc/puppyversion")):
			version = commands.getoutput("cat /etc/puppyversion")
			descr = "Puppy Linux"
		# Kinoppix
		elif(os.path.exists("/etc/kinoppix-version")):
			descr = "Kinoppix"
			version = commands.getoutput("cat /etc/kinoppix-version")
		# PLD Linux
		elif(os.path.exists("/etc/pld-release")):
			descr = commands.getoutput("cat /etc/pld-release")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Pardus
		elif(os.path.exists("/etc/pardus-release")):
			descr = commands.getoutput("cat /etc/pardus-release")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Xandros
		elif(os.path.exists("/etc/xandros-desktop-version")):
			descr = commands.getoutput("cat /etc/xandros-desktop-version")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Gentoo
		elif(os.path.exists("/etc/gentoo-release")):
			descr = "Gentoo"
			version = commands.getoutput("cat /etc/gentoo-release")
		# Arch
		elif (os.path.exists("/etc/arch-release")):
			descr = "Arch Linux"
			version = commands.getoutput("cat /etc/arch-release")
		# Zenwalk
		elif (os.path.exists("/etc/zenwalk-version")):
			descr = "Zenwalk"
			version = commands.getoutput("cat /etc/zenwalk-version")
		# Yellow dog
		elif (os.path.exists("/etc/yellowdog-release")):
			descr = "Yellow dog"
			version = commands.getoutput("cat /etc/yellowdog-release")
		# SuSE
		elif (os.path.exists("/etc/SuSE-release")):
			descr = commands.getoutput("cat /etc/SuSE-release")
			pos = descr.find(" ")
			version = descr[pos+1:descr.find("\n")]
			descr = descr[:pos]
		# Solaris - Sparc 
		elif (os.path.exists("/etc/release")):
			descr = commands.getoutput("cat /etc/release")
			pos = descr.find("release")+7
			version = descr[pos+1:descr.find(" ",pos+1)]
			descr = descr[:pos]
		# Sun JDS
		elif (os.path.exists("/etc/sun-release")):
			descr = "Sun JDS"
			version = commands.getoutput("cat /etc/sun-release")
		# Slackware
		elif (os.path.exists("/etc/slackware-version")):
			descr = commands.getoutput("cat /etc/slackware-version")
			pos = descr.find(" ")
			version = descr[pos+1:]
			descr = descr[:pos]
		# Desconhecido
		else:
			descr = "Unspecifield"
		s = descr
		if version != "":
			s += " - " + version
		return s
	
	# transforma o metodo em static
	getSO = staticmethod(getSO)


class Pacotes:
	"""
		Classe para verificar quais pacotes estao instalados
		e/ou se um especifico esta
	"""
	
	def __init__(self):
		# SOs divido por gerenciadores de pacotes
		self.pkg_so = {
			  	# Debian - dpkg
			  	'dpkg' : ['debian', 'ubuntu', 'kurumin'],
			  	# BSD
		    	'pkg_info' : ['freebsd', 'openbsd'],
			  	# RPM
			  	'rpm' : ['rhel', 'red hat', 'redhat', 'fedora', 'centos', 'suse'],
			  	# Slackware - find no diretorio packages
			  	'slack' : ['slackware'],
	 	}	
		self.pkg_cmd = {
			    'dpkg' : 'dpkg --get-selections ',
			    'pkg_info' : 'pkg_info ',
			    'rpm' : 'rpm -qa ',
			    'slack' : 'find /var/log/packages -name ',
		}
		
	def __getMng__(self, so_name):
		"""
			Retorna o gerenciador de pacote atraves do nome do SO
			Ex: so_name = 'Ubuntu 8.04' - return 'dpkg'
		"""
		for pkg in self.pkg_so:
			for so in self.pkg_so[pkg]:
				if so in so_name.lower():
					return pkg
		return ''
		
	def __getMethod__(self, so_name, mng = None):
		"""
			Retorna o comando do gerenciador de pacote atraves do nome do SO
			Ex: so_name = 'Ubuntu 8.04' - return 'dpkg --get-selections'
		"""
		if not mng:
			for pkg in self.pkg_so:
				for so in self.pkg_so[pkg]:
					if so in so_name.lower():
						return self.pkg_cmd[pkg]
		else:
			return self.pkg_cmd[mng]
		return ''
	
	def isInstalled(self, pkg_installed, os):
		"""
			Retorna true ou false verificando se o pacote passado por parametro
			esta ou nao instalado
		"""
		mng = self.__getMng__(os)
		output = commands.getoutput(self.__getMethod__(os) + pkg_installed)
		if mng == 'dpkg':
			if 'install' in output:
				return True
		else:
			if output != '':
				return True
		return False
			
	def getAllInstalled(self, os):
		"""Retorna uma string com todos os pacotes instalados"""
		mng = self.__getMng__(os)
		if mng == 'slack':
			return  commands.getoutput(self.__getMethod__(os)[0:-6])
		return commands.getoutput(self.__getMethod__(os))
		

class Computador :
	"""
		Classe Computador contem as informacoes de 
		hardware e configuracoes da maquina
	"""
	def __init__(self):
		devices = self.__get_input_devices__()
		self.ip_ativo = ''
		self.hostName = self.__get_host_name__()
		self.so = SO_Info.getSO()
		self.mouse = devices['mouse']
		self.teclado = devices['teclado']
		self.pacote = Pacotes()
		self.ram = ''
		self.rom = ''
		self.placaMae = ''
		self.placaRede = ''
		self.hardDisk = ''
		self.bios = ''
		self.video = ''
		self.audio = ''
		self.cpu = ''
		self.modem = ''
		
	def isRoot(self):
		"""Retorna se o usuario e root ou nao"""
		if os.getuid() != 0:
			return False
		return True

	def coletar(self):
		print "COLETAR"
		"""Inicia a coleta de informacoes do computador"""
		try:
			if not self.isRoot():
				raise ComputerException('Para executar o programa é necessário estar como super usuário (root).')
			pc_xml = PC_XML()
			self.ram = pc_xml.ram		
			self.rom = pc_xml.rom
			self.placaMae = pc_xml.placaMae
			self.placaRede = pc_xml.placaRede
			self.hardDisk = pc_xml.hardDisk
			self.bios = pc_xml.bios
			self.video = pc_xml.video
			self.audio = pc_xml.audio
			self.cpu = pc_xml.cpu
			self.modem = pc_xml.modem
		except ComputerException, e:
			raise Exception('%s\n\nO programa foi abortado de forma prematura.\n' % e.message)
			sys.exit()
	
	def __get_host_name__(self):
		"""Retorna o hostname da maquina atraves de socket"""
		return socket.gethostname()
	
	
	def __get_last_login__(self):
		"""Retorna o ultimo login atras de bash"""
		last = commands.getoutput('last -n 1')
		return last[:last.find(' ')]

	def __get_input_devices__(self):
		"""Retorna a descricao de mouse e teclado"""
		inputs = {'teclado': '', 'mouse': ''}
		s = commands.getoutput("cat /proc/bus/input/devices")
		fim = 0
		pesqBus = s.find("Bus=0011")
		if(pesqBus > 0):
			primeiro = (s.find("Name=",pesqBus))+6
			fim = (s.find("P:",primeiro))-2
			if(primeiro > 0 and fim > 0):
				inputs['teclado'] = s[primeiro:fim]
		pesqBus = s.find("Bus=0011",fim)
		if(pesqBus > 0):
			primeiro = (s.find("Name=",pesqBus))+6
			fim = (s.find("P:",primeiro))-2
			if(primeiro > 0 and fim > 0):
				inputs['mouse'] = s[primeiro:fim]
		return inputs	        
	
	def getSO (self) :
		""" retorna string contendo sistema operacional """
		# returns string
		return self.so	
	
	def getPacotes(self):
		"""Retorna todos os pacotes instalados na maquina"""
		return self.pacote.getAllInstalled(self.getSO())

	def isInstalado(self, pacote):
		"""Retorna True ou False se o pacote esta ou nao instalado"""
		return self.pacote.isInstalled(pacote, self.getSO())
	
	def getHostName(self) :
		""" retorna host name """
		# returns string
		return self.hostName	
		
	def getPlacaMae(self) :
		""" retorna objeto MotherBoard com as informacoes da placa mae """
		# returns string 
		return self.placaMae
	
	def getCPU(self) :
		""" retorna lista de cpus do micro """
		# returns list
		return self.cpu	
	
	def getRam(self) :
		""" retorna objeto RAM com descricao das memorias ram do micro """
		# returns RAM
		return self.ram	
	
	def getHardDisk(self) :
		""" retorna lista de objetos HD """
		# returns list
		return self.hardDisk	
	
	def getAudio(self) :
		""" retorna lista de audio """
		# returns list
		return self.audio
	
	def getVideo(self) :
		""" retorna lista de placa de video """
		# returns list
		return self.video
	
	def getRom(self) :
		""" retorna lista de midias ROM """
		# returns list
		return self.rom
	
	def getPlacaRede(self) :
		""" retorna lista de placas de redes """
		# returns list
		return self.placaRede
	
	def getIPAtivo(self, server):
		""" retorna o endereco de IP que conecta no server especificado """		
		p = re.compile('[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}')
		ips = p.findall(server)
		if len(ips) == 0:
			raise ComputerException("Endereço do Servidor inválido. Não foi possível detectar o ip ativo.")			
		return Rede().getIPAtivo(ips[0])
	
	def getMACAtivo(self, ip):
		""" retorna o endereco de IP que conecta no server especificado """			
		return Rede().__getMac__(ip).replace(':','-')
	
	def getModem(self) :
		""" retorna lista de modens """
		# returns list
		return self.modem
	
	def getBios(self) :
		""" retorna um objeto do tipo Bios """
		# returns Bios
		return self.bios
	
	def getTeclado(self):
		"""Retorna a descricao do Teclado"""
		return self.teclado
	
	def getMouse(self):
		"""Retorna a descricao do mouse"""
		return self.mouse
		
	def __toString(self):
		"""Metodo toString da Classe"""
		desc = "Computador \n"
		desc += "\tSistema Operacional: %s \n" % self.getSO()
		desc += "\tHostname: %s \n" % self.getHostName()
		desc += "Placa Mae \n"
		desc += "\tDescricao: %s \n" % self.getPlacaMae()
		desc += "Bios \n"
		desc += "\tDescricao: %s \n" % self.bios.getDescricao()
		desc += "\tData: %s \n" % self.bios.getData()
		for c in self.cpu:
			desc += "CPU \n"
			desc += "\tId: %s \n" % c.getId()
			desc += "\tFrequencia: %s \n" % c.getFrequencia()
			desc += "\tDescricao: %s \n" % c.getDescricao()
			desc += "\tSerial: %s \n" % c.getSerial()
		for hd in self.hardDisk:
			desc += "HD \n"
			desc += "\tTamanho: %s Mb \n" % hd.getTamanho()
			desc += "\tDescricao: %s \n" % hd.getDescricao()
			desc += "\tFabricante: %s \n" % hd.getFabricante()
		desc += "Teclado \n"
		desc += "\tDescricao: %s \n" % self.getTeclado()
		desc += "Mouse \n"
		desc += "\tDescricao: %s \n" % self.getMouse()
		for v in self.video:
			desc += "Video \n"
			desc += "\tRam: %s Mb \n" % v.getRam()
			desc += "\tCores: %s \n" % v.getCores()
			desc += "\tDescricao: %s \n" % v.getDescricao()
		for a in self.audio:
			desc += "Audio \n"
			desc += "\tDescricao: %s \n" % a
		for m in self.modem:
			desc += "Modem \n"
			desc += "\tDescricao: %s \n" % m
		desc += "Ram \n"
		desc += "\tTamanho: %s Mb \n" % self.ram.getTamanho()
		desc += "\tDescricao: %s \n" % self.ram.getDescricao()
		for r in self.rom:
			desc += "Rom \n"
			desc += "\tDescricao: %s \n" % r
		for pr in self.placaRede:
			desc += "Placa de Rede \n"
			desc += "\tFabricante: %s \n" % pr.getFabricante()
			desc += "\tDescricao: %s \n" % pr.getDescricao()
			desc += "\tEndereco IP: %s \n" % pr.getIP()
			desc += "\tMascara de Rede: %s \n" % pr.getMascara()
			desc += "\tEndereco Mac: %s \n" % pr.getMAC()
			desc += "\tLogicalname Mac: %s \n" % pr.getLogicalName()
		return desc 
	
	def toString(self):
		"""Metodo toString da Classe"""
		return self.__toString()
