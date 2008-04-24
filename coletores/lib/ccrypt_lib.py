"""
    Adiciona o caminho do AES a partir da arquitetura
    da maquina local (32 ou 64 bits) e da versao do Glibc
"""
import commands, sys

if __name__ == 'coletores.lib.ccrypt_lib': 
    # token
    x_64 = 'X86_64'
    # AES.so paths
    dic = {
           '32' : sys.path[0] + '/coletores/lib/x32',
           '64' : sys.path[0] + '/coletores/lib/x64', 
           '32_4' : sys.path[0] + '/coletores/lib/x32/libc4',           
           }
    # output uname shell
    arch = commands.getoutput("uname -m")
    # is 64
    if x_64 in arch.upper():
        sys.path.append(dic['64'])
    else:
        sys.path.append(dic['32'])
        """
            TODO: pegar a versao do glib instalada
        """

else:
    # dont called 
    sys.exit()
    
    