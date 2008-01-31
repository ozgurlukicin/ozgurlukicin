#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2007 Artistanbulpr
# Licensed under the GNU General Public License, version 3.
# See the file http://www.gnu.org/copyleft/gpl.txt.

class Loggme(object):
    
    def __init__(self):
        """ Bu apacheden bıktım abi logger yapçem bitane :)"""
        self.son_mesaj=[] #bu loglancek işte
        
    
    def loglabeni(self):
        """ Buda dosyaya yazcek işte"""
        
        logcu=open("logumben.txt",'w')
        logcu.writelines(self.son_mesaj)
        logcu.close()
            
