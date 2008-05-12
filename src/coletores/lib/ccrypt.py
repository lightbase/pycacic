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

from Python_AES import Python_AES


class CCrypt:
    """
        Classe CCrypt
        
        Encripta e Decripta mensagens
        utilizando AES (modo CBC) e Base64
    """
    
    KEY = 'CacicES2005'
    AES_KEY_SIZE = 32
    AES_BLOCK_SIZE = 16
    IV = 'abcdefghijklmnop'
    
    
    def __init__(self):
        self.char = '@'
        self.key = self.padding(self.KEY, self.AES_KEY_SIZE, self.char)
        self.iv = self.padding(self.IV, self.AES_BLOCK_SIZE, self.char)
        
    def encrypt(self, text):
        """Encrypta uma string com AES (CBC) e depois em BASE64"""
        self.cipher = Python_AES(self.key, 2, self.iv)
        cifrado = self.cipher.encrypt(self.padding(text, self.AES_BLOCK_SIZE, self.char))
        return base64.encodestring(cifrado)[0:-1]
    
    def decrypt(self, text):
        """Decripta uma string convertida pelo metodo encrypt()"""
        # ER para remover o padding da string
        rm = re.compile("(?:"+ self.char +")*$")
        self.cipher = Python_AES(self.key, 2, self.iv)
        decifrado = self.cipher.decrypt(base64.decodestring(text))
        return decifrado.replace(rm.findall(decifrado)[0],'')

    def padding(self, s, tam, char):
        """Adiciona preenchimento a string"""
        s = str(s)
        origsize = len(s)
        if (origsize % tam) != 0 or origsize == 0:
            p = tam - (origsize % tam)
            s = s + (char*p);
        return s

