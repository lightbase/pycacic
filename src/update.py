import os
import sys
import time

if __name__ == '__main__':
    print 'Chamou Update'
    time.sleep(5)
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-pkg':
            pacote_disponivel = sys.argv[i+1]
        elif sys.argv[i] == '-tmp':
            temp_dir = sys.argv[i+1]
    if temp_dir == '' or pacote_disponivel == '':
        print 'Update: Nao foi possivel atualizar.'
        sys.exit(1) 
    print 'Parametros OK'
    # removendo o pacote atual
    os.system('rm -Rf /usr/share/pycacic')
    # descompactando o pacote novo    
    os.system('mkdir /tmp/%s' % temp_dir)
    os.system('tar -xf /tmp/%s -C /tmp/%s' % (pacote_disponivel, temp_dir))
    os.system('tar -xf /tmp/%s/cacic.tar -C /usr/share' % temp_dir)
    # removendo o pacote novo no temporario
    os.system('rm -Rf /tmp/%s' % temp_dir)
    os.system('rm -f /tmp/%s' % pacote_disponivel)
    # reiniciando o PyCacic    
    print 'Reiniciando PyCacic'
    os.system('python /usr/share/pycacic/cacic.py &')
    sys.exit(1)