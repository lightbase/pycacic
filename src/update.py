#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""

    Copyright 2000, 2001, 2002, 2003, 2004, 2005 Dataprev - Empresa de Tecnologia e Informações da Previdência Social, Brasil
    
    Este arquivo é parte do programa CACIC - Configurador Automático e Coletor de Informações Computacionais
    
    O CACIC é um software livre; você pode redistribui-lo e/ou modifica-lo dentro dos termos da Licença Pública Geral GNU como 
    publicada pela Fundação do Software Livre (FSF); na versão 2 da Licença, ou (na sua opnião) qualquer versão.
    
    Este programa é distribuido na esperança que possa ser  util, mas SEM NENHUMA GARANTIA; sem uma garantia implicita de ADEQUAÇÂO a qualquer
    MERCADO ou APLICAÇÃO EM PARTICULAR. Veja a Licença Pública Geral GNU para maiores detalhes.
    
    Você deve ter recebido uma cópia da Licença Pública Geral GNU, sob o título "LICENCA.txt", junto com este programa, se não, escreva para a Fundação do Software
    Livre(FSF) Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
    
    
    
    Módulo update
    
    Tem a finalidade de extrair o novo pacote disponível, sobrescrever o 
    instalado atualmente e reiniciar o programa após um intervalo determinado.
    
    @author Dataprev - ES 
    

"""

import os
import sys
import time

from config.io import Writer
from logs.log import CLog

from lang.language import Language

# Languages
_l = Language()

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
        CLog.appendLine('AutoUpdate', 'Iniciado processo de autoupdate.')
        os.system('mkdir /tmp/%s' % temp_dir)
        os.system('tar -xf /tmp/%s -C /tmp/%s' % (pacote_disponivel, temp_dir))
        os.system('tar -xf /tmp/%s/pycacic/cacic.tar -C /usr/share' % temp_dir)
        # removendo o pacote novo no temporario
        os.system('rm -Rf /tmp/%s' % temp_dir)
        os.system('rm -f /tmp/%s' % pacote_disponivel)
        open("/usr/share/pycacic/config/MD5SUM", "w").write(novo_hash)
        CLog.appendLine('AutoUpdate', _l.get('update_sucess'))
        CLog.appendLine('AutoUpdate', _l.get('program_restart'))
    # reiniciando o PyCacic
    os.system('python /usr/share/pycacic/cacic.py &')
    sys.exit(1)
    