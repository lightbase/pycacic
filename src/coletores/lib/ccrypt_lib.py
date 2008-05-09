"""
    Adiciona o caminho do AES a partir da arquitetura
    da maquina local (32 ou 64 bits) e da versao do Glibc
"""
import commands, sys
from globals import Globals 

import sys

if __name__ == 'coletores.lib.ccrypt_lib':
    # token
    x_64 = 'X86_64'
    # AES.so paths
    dic = {
           '32'   : '%s/coletores/lib/x32' % Globals.PATH,
           '64'   : '%s/coletores/lib/x64' % Globals.PATH, 
           '32_4' : '%s/coletores/lib/x32/libc4' % Globals.PATH,
           }
    # output uname shell
    arch = commands.getoutput("uname -m")
    # is 64
    if x_64 in arch.upper():
        sys.path.append(dic['64'])
    else:
        """
            TODO: pegar a versao do glib instalada
        """
        sys.path.append(dic['32_4'])        

else:
    # dont called 
    sys.exit()
    
    