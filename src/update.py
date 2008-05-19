import os
import sys
import time

from config.io import Writer

if __name__ == '__main__':
    time.sleep(5)
    temp_dir = ''
    pacote_disponivel = ''
    novo_hash = ''
    # pegando argumentos
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-pkg':
            pacote_disponivel = sys.argv[i+1]
        elif sys.argv[i] == '-hash':
            novo_hash = sys.argv[i+1]
        elif sys.argv[i] == '-tmp':
            temp_dir = sys.argv[i+1]
    if temp_dir != '' and pacote_disponivel != '':
        # descompactando o pacote novo    
        os.system('mkdir /tmp/%s' % temp_dir)
        os.system('tar -xf /tmp/%s -C /tmp/%s' % (pacote_disponivel, temp_dir))
        os.system('tar -xf /tmp/%s/pycacic/cacic.tar -C /usr/share' % temp_dir)
        # removendo o pacote novo no temporario
        os.system('rm -Rf /tmp/%s' % temp_dir)
        os.system('rm -f /tmp/%s' % pacote_disponivel)
        open("/usr/share/pycacic/config/MD5SUM", "w").write(novo_hash)
        print 'PyCacic atualizado com sucesso.'
        print 'reiniciando sistema...'
    # reiniciando o PyCacic
    os.system('python /usr/share/pycacic/cacic.py &')
    sys.exit(1)
    