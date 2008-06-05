# -*- coding: UTF-8 -*-

import os
import codecs
import commands
from time import strftime

class CLog:
    
    STRP = '%CLOG%'    
       
    def getCurrentFileName():
        """Retorna o nome do arquivo de log atual, formato YYYY-MM-DD"""
        return '%s.log' % strftime("%Y-%m-%d")
    
    def getCurrentFile():
        """Retorna o conteudo do arquivo de log atual"""
        return file('/usr/share/pycacic/logs/%s' % CLog.getCurrentFileName(), 'r').read()
    
    def removeOlds():
        """Remove os arquivos de log que nao sao do mes atual"""
        name = CLog.getCurrentFileName().split('-')
        if not len(name) == 3:
            return
        month = name[1]
        # commands.getoutput('rm -- *-!(%s)-*.log' % month)
        #commands.getoutput('rm -- /usr/share/pycacic/logs/*.log')
    
    def createNew(fileName):
        """Cria novo arquivo de log"""
        file(fileName, 'w').write('')
        codecs.open(fileName, "w", "utf-8").write('')
    
    def appendLine(module, desc):
        """Adiciona uma linha contendo o data, nome do modulo e a descricao da acao no final """
        fileName = '/usr/share/pycacic/logs/%s' % CLog.getCurrentFileName()
        if not os.path.exists(fileName):
            CLog.removeOlds()
            CLog.createNew(fileName)
        f = file(fileName, 'a')
        l =  '%s%s%s%s%s\n' % (strftime("%H:%M:%S %d/%m/%Y"), CLog.STRP, module, CLog.STRP, desc)
        f.write(l.encode("utf-8"))
        f.close()
        
    getCurrentFileName = staticmethod(getCurrentFileName)
    getCurrentFile = staticmethod(getCurrentFile)
    removeOlds = staticmethod(removeOlds)
    createNew = staticmethod(createNew)
    appendLine = staticmethod(appendLine)
    
