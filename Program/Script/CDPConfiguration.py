# -*- coding: utf8 -*-
''' Gestion de l'interface de contrôle des expériences de l'eye tracker'''
# Gestion des expériences par création de méthodes virtuelles complétées dans le fichier CDP experience

import configparser


__metaclass__ = type
class CDPConfiguration():
    def __init__(self,configFilename):
        self.config = configparser.ConfigParser()
        self.config.read(configFilename)

    # Méthode généraale de lecture du fichier .ini 
    #  [BLOC] + [KEY]  -> Value
    def getConfiguration(self,  bloc,  key):
        return ( self.config[bloc][key])

    # Dossier de stockage des calibrations 
    def getCalibrationDir(self):
        dirname = self.getConfiguration('PATHS','home_data') + '/' + self.getConfiguration('PATHS','dir_calibration')
        return ( dirname )  

    # Fichier Json de configuration d'une expérience 
    def getConfigFilename(self, experience ):
        filename = self.getConfiguration('PATHS','home_program') + '/' + self.getConfiguration('CONF_EXPERIENCE', experience)
        return (filename)

    # Dossier de stockage des résultats d'une expérience
    def getDataDirname( self , local_dir ) :
        dirname = self.getConfiguration('PATHS','home_data') + '/' +self.getConfiguration('PATHS','dir_experience') + '/' + local_dir
        return( dirname )
        
     # Liste des expériences utilisables dans le Viewer
    def getExperienceList( self   ) :
        list = self.getConfiguration('CONF_VIEWER','LST_EXPERIENCES').split(',')
        return( list )       
        
    # Dossier de stockage des Images utilisées dans une expérience
    def getImageDirname( self , local_dir ) :
        dirname = self.getConfiguration('PATHS','home_program') + '/' +self.getConfiguration('PATHS','dir_image') + '/' + local_dir
        return( dirname )
    ''' Fonctions de calibrations '''



