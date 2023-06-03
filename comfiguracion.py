import os
from pathlib import Path
import toml

class Comfiguracion:
    
    def __init__(self, app, config, base):
        self.directorio_comfiguracion = self.getconfigdir()
        self.app = app
        self.config = config
        self.base = base
        self.comprovar(self.app, self.config)
        
    def comprovar(self, directorio, archivo):
        config_dir = Path(self.directorio_comfiguracion) / directorio
        if not config_dir.exists():
            os.makedirs(config_dir)
        config_file = config_dir / archivo
        if not config_file.exists():
            self.escribir_datos(self.base)
    
    def read_conf(self):
        config_dir = Path(self.directorio_comfiguracion) / self.app
        config_file = config_dir / self.config
        idata = toml.load(config_file)
        return idata
    
    def escribir_datos(self, idato):
        config_file = Path(self.directorio_comfiguracion) / self.app / self.config
        with open(config_file, 'w') as fw:
            toml.dump(idato, fw)
    
    def getconfigdir(self):
        if 'XDG_CONFIG_HOME' in os.environ:
            return os.environ['XDG_CONFIG_HOME']
        else:
            return Path.home() / '.config'
        
    def get_dir(self):
        return Path(self.directorio_comfiguracion) / self.app

#if __name__ == '__main__':
#    
#    APP = "pelisdb"
#    config = f"{APP}.conf"
#    
#    conf = Comfiguracion(APP, config)  
#    
#    #datos2 = conf.read_conf()
#    #datos2["ultimo_lugar"] = "Carpeta 1"
#    #
#    #conf.escribir_datos(datos2)
#    #
#    datos=conf.read_conf()
#    #print(datos)
#    
#    print(conf.get_dir() / datos['dir_caratulas'])
