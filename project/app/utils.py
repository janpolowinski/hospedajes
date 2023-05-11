import yaml
import os
from loguru import logger
from pydantic import BaseSettings, AnyUrl, Extra
import jinja2
import xmlschema
import io
import gzip
import base64
from pprint import pprint

def pyyaml_config_settings_source(settings: BaseSettings) -> dict[str, any]:
    # carga los settings desde un fichero yaml
    with open(os.path.join(os.path.dirname(__file__), 'config.yml')) as f:        
        try:
            print(f"Directorio actual {os.getcwd()}")
            return yaml.load(f, Loader=yaml.FullLoader) 
        except yaml.YAMLError as exc:
            logger.error(f"{exc}. Directorio actual {os.getcwd()}")
            return {}


class Settings(BaseSettings):
    # settings de la aplicación
      
    # environment: str = os.getenv("ENVIRONMENT", "dev") # estam en dev o en prod
    # testing: bool = os.getenv("TESTING", 0) # estam en mode test o no

    class Config:
        env_file_encoding = "utf-8"
        extra=Extra.allow
        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                pyyaml_config_settings_source,
                env_settings,
                file_secret_settings,
            )        


#@lru_cache()
def get_config() -> BaseSettings:
    return Settings()

# setamos la config a esta variable y ya podemos hacer
# valor = config.clave
config=get_config()


def load_template(template_file:str)->jinja2.Template:
    """ carga y retorna una plantilla """
    searchpath = os.path.join(os.path.dirname(__file__), 'soporte', 'plantillas', config.version)
    try:        
        # logger.debug(f"Directorio de plantillas: {searchpath}")
        templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
        templateEnv = jinja2.Environment(loader=templateLoader)  
        return templateEnv.get_template(template_file)
    except Exception as e:
        logger.error(f"Error al cargar la plantilla {template_file} desde el directorio {searchpath}: {e}")
        raise e

"""
jinja_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape()
)

template = jinja_env.get_template("mytemplate.html")
"""

def get_entorno()->dict:
    # devuelve los datos que dependen del entorno
    # si entorno==pruebas, devuelve los datos de conexión de pruebas
    return config.conexiones[config.entorno]

def get_credenciales()->str:
    # devuelve las credenciales de conexión como basic auth
    try:    
        entorno=get_entorno()
        # logger.debug(f"{entorno['usuario']}:{entorno['password']}")
        return base64.b64encode(f"{entorno['usuario']}:{entorno['password']}".encode()).decode()
    except Exception as e:
        logger.error(f"Error al codificar las credenciales de conexión: {e}")
        raise e
    
def validar_xml_con_xsd(xml_str: str, xsd_file: str)->bool:
    # valida un xml con un xsd
    # Ejemplo de uso
    # validar_xml_con_xsd(cadena_xml, "ejemplo.xsd")

    path_plantilla = os.path.join(os.path.dirname(__file__), 'soporte', 'esquemas', config.version, xsd_file)
    # logger.debug(f"Validando el XML con la plantilla XSD {path_plantilla}")

    # Leer el contenido del archivo XSD
    try:
        with open(path_plantilla, 'r') as xsd:
            schema = xmlschema.XMLSchema(xsd.read())
            # logger.debug(' Plantilla XSD cargada correctamente')
            # pprint(schema.to_dict(xml_str))
    except Exception as e:
        logger.error(f"Error al leer el archivo XSD {path_plantilla}: {e}")
            
    try:
        # validamos el xml con el xsd
        # logger.debug('Validando el XML con la plantilla XSD')
        schema.validate(xml_str)
        # logger.debug('XML validado correctamente')
        return True
    except Exception as e:
        logger.error(f"Error al validar el archivo XML {xml_str} con la plantilla {xsd_file}: {e}")
        
    
def comprimir_cadena_en_zip(contenido: str)->str:
    # comprime una cadena en un archivo zip en memoria y lo devuelve en base64
    try:
        # pasar a bytes y comprimir la cadena
        c=gzip.compress(contenido.encode())

        # retornar la cadena en base64
        return base64.b64encode(c).decode()

    except Exception as e:
        logger.error(f"Error al comprimir la cadena en un archivo zip en memoria: {e}")
        


def descomprimir_cadena_de_zip(contenido: str)->str:
    # descomprime una cadena codificada en base64 y le hace unzip
    # comprime una cadena en un archivo zip en memoria y lo devuelve en base64
    try:
        # decodificar desde base64
        c=base64.b64decode(contenido.encode())

        # pasar a bytes y descomprimir la cadena
        return gzip.decompress(c).decode()

    except Exception as e:
        logger.error(f"Error al descomprimir la cadena: {e}")        