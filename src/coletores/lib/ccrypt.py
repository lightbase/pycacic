# -*- coding: UTF-8 -*-

"""

    Modulo ccrypt (Cacic Crypt)
    
    Modulo com finalidade de encriptar ou decriptar
    as mensagens enviadas ou recebidas pelo Gerente Web.
    E tambem as guardadas nos arquivos locais (temporarios ou nao)
    
    Tornando mais segura a comunicacao entre o agente e o servidor
    
    @author: Dataprev - ES
    @version: 1.0.0 (14 de abril de 2008)
    
"""

import re
import binascii
import base64
import ccrypt_lib
from Crypto.Cipher import AES

class CCrypt:
    """
        Classe CCrypt
        
        Encripta e Decripta mensagens
        utilizando AES (modo CBC) e Base64
    """
    
    AES.block_size = 16 # 16 bytes = 128 bits 
    AES.key_size = 32 # 32 bytes = 256 bits
    mode = AES.MODE_CBC
    KEY = 'CacicES2005'
    IV = 'abcdefghijklmnop'
    cipher = AES.new
    
    def __init__(self):
        self.char = '@'
        self.key = self.padding(self.KEY, AES.key_size, self.char)
        self.iv = self.padding(self.IV, AES.block_size, self.char)

    def encrypt(self, text):
        """Encrypta uma string com AES (CBC) e depois em BASE64"""
        cifrado = self.cipher(self.key, self.mode, self.iv).encrypt(self.padding(text, AES.block_size, self.char))
        return base64.b64encode(cifrado)
    
    def decrypt(self, text):
        """Decripta uma string convertida pelo metodo encrypt()"""
        # ER para remover o padding da string
        rm = re.compile("(?:"+ self.char +")*$")
        decifrado = self.cipher(self.key, self.mode, self.iv).decrypt(base64.b64decode(text))
        return decifrado.replace(rm.findall(decifrado)[0],'')

    def padding(self, s, tam, char):
        """Adiciona preenchimento a string"""
        s = str(s)
        origsize = len(s)
        if (origsize % tam) != 0 or origsize == 0:
            p = tam - (origsize % tam)
            s = s + (char*p);
        return s

