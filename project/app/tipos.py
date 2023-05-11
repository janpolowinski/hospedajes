""" Definimos los tipos base que usaremos en el resto de clases

Según v3.0.0 de la especificación de la Interfaz de Servicios Externos de fecha # v3.0.0. 23-02-2023 (DD-MM-YYYY)

Nombraremos con el postfijo Type a los tipos base
"""
from enum import Enum, IntEnum
from datetime import date, datetime
from pydantic import Field, BaseModel, EmailStr, ConstrainedStr,\
                     ConstrainedDecimal, validator, ConstrainedDate, PastDate, FutureDate,\
                     ConstrainedInt, ConstrainedFloat, ConstrainedList, ConstrainedDate
from loguru import logger
import re
import pycountry
import csv
import os
from email_validator import validate_email
from app.utils import config

class hospedajesBaseType(BaseModel):
    # base de todos los modelos
    ...

class baseStringType(str):
    # base de todos los strings
    @validator("*", pre=True)
    def strip_string(cls, v):
        if isinstance(v, str):
            return v.strip()
        return v


class nombreType(baseStringType):
    """ Nombre propio o apellidos de persona 
    Elimina espacios dobles y convierte a mayúsculas la primera letra de cada palabra
    >>> nombreType(' gerArDo     dieGO ')
    'Gerardo Diego'
    """
    max_length = 50
    min_length = 2

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        #raise ValueError(f'validando nombre {v}')
        if not isinstance(v, str):
            raise TypeError('string required')
        v = v.strip() # elimina espacios al principio y al final
        v = re.sub(r'\s{2,}', ' ', v) # elimina más de dos espacios seguidos

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de nombre o apellido ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        return ' '.join((word.capitalize()) for word in v.split(' ')) # capitaliza la primera letra de cada palabra

class fechaType(date):
    # devuelve formato AAAA-MM-DD
    def __str__(self):
        return self.strftime("%Y-%m-%d")
        
    def __repr__(self):
        return self.strftime("%Y-%m-%d")

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v

class fechaNacimientoType(PastDate):
    # fecha de nacimiento de una persona, siempre pasado de ahora
    def __str__(self):
        return self.strftime("%Y-%m-%d")
        
    def __repr__(self):
        return self.strftime("%Y-%m-%d")

class fechaHoraType(datetime):
    # devuelve en formato AAAA-MM-DDThh:mm:ss
    def __str__(self):
        return self.strftime("%Y-%m-%dT%H:%M:%S")
         
    def __repr__(self):
        return self.strftime("%Y-%m-%dT%H:%M:%S")
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return v

class emailType(baseStringType):
    # un email válido
    max_length = 50
    min_length = 5

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            validate_email(v, check_deliverability=False)
        except Exception as e:
            raise ValueError(f'Email {v} no válido: {e}')

        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de email ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')
        return v
    
class telefonoType(baseStringType):
    # un telefono
    max_length = 20
    min_length = 6

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de nombre o apellido ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')
        return v

class codigoEstablecimientoType(baseStringType):
    # un telefono
    max_length = 10
    min_length = 10

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Codigo de establecimiento, longitud ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')
        return v


class documentoType(baseStringType):
    # Número de documento de identidad
    # Hemos fijado *arbitrariamente* una longitud mínima de 5
    # NIF, NIE, pasaporte, etc.
    # devuelve la cadena sin espacios en blanco y guiones y en mayúsculas
    # >>> documentoType('  12345678 - a  ')
    # '12345678A'
    max_length = 15
    min_length = 5

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # Sólo caracteres alfanuméricos y pasamos a mayúsculas
        v = re.sub(r'[^a-zA-Z0-9]', '', v.strip()).upper()

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de documento ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        return v


class soporteDocumentoType(baseStringType):
    min_length=3
    max_length=9

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de soporte de documento ({len(v)}) no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        return v




paises = [pais.alpha_3 for pais in pycountry.countries] # listado de nacionalidades en ISO 3166-1 alpha-3
class nacionalidadType(baseStringType):
    """ codigo de nacionalidad según ISO 3166-1 alpha-3 
        ver https://es.wikipedia.org/wiki/ISO_3166-1
    """
    max_length = 3
    min_length = 3

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # formateamos
        v = re.sub(r'[^a-zA-Z0-9]', '', v.strip()).upper()

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de nacionalidad {len(v)} no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        # comprobamos que la nacionalidad exista
        if v not in paises:
            raise ValueError(f'Nacionalidad {v} no válida.')

        return v

class paisType(nacionalidadType):
    # Pais de una dirección, en iso-3
    pass

# creamos un diccionario con los municipios del ine
fichero_municipios = os.path.join(os.path.dirname(__file__), 'soporte', config.fic_municipios)
municipios = {}
with open(fichero_municipios, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    # la clave del municipio está formada por el código de provincia `CPRO` + el código de municipio `CMUN`
    for row in reader:                 
        municipios[f"{row['CPRO']}{row['CMUN']}"] =row['NOMBRE']

class codigoMunicipioType(baseStringType):    
    # Código del municipio, códigos del INE cinco dígitos si país España
    # la clave del municipio está formada por el código de provincia `CPRO` + el código de municipio `CMUN`
    max_length = 5
    min_length = 5

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # formateamos
        v = re.sub(r'[^0-9]', '', v)

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de {len(v)} no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        # comprobamos que el municipio exista
        if v not in municipios.keys():
            raise ValueError(f'Municipio {v} no válido en fichero de municipios {fichero_municipios}.')

        return v



# creamos un diccionario con los codigos postales, tomados del callejero del INE
fichero_codigos_postales = os.path.join(os.path.dirname(__file__), 'soporte', config.fic_codigos_postales)
codigos_postales = {}
with open(fichero_codigos_postales, encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=',')
    # clave el código postal, valor la descripción del municipio
    for row in reader:                 
        codigos_postales[f"{row['codigo_postal']}"] =row['municipio_nombre']

class codigoPostalType(baseStringType):
    # Apdo 6.3. Bloque dirección
    # Código postal de la dirección
    # ver https://github.com/codeforspain
    # ver https://github.com/inigoflores/ds-codigos-postales
    max_length = 5
    min_length = 5

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')

        # formateamos
        v = re.sub(r'[^0-9]', '', v)

        # comprobamos longitud
        if len(v) < cls.min_length or len(v) > cls.max_length:
            raise ValueError(f'Longitud de {len(v)} no válida. Debe estar entre {cls.min_length} y {cls.max_length}.')

        # comprobamos que el municipio exista
        if v not in codigos_postales.keys():
            raise ValueError(f'Código postal {v} no válido en fichero de código postales {fichero_codigos_postales}.')

        return v



roles = [('TI', 'Titular del contrato'), ('VI', 'Viajero')]
parentescos = [('AB', "Abuelo/a"), ('BA', "Bisabuelo/a"), ('BN', "Bisnieto/a"), 
               ('CD', "Cuñado/a"), ('CY', "Cónyuge"), ('HJ', "Hijo/a"), 
               ('HR', "Hermano/a"),  ('NI', "Nieto"), ('PM', "Padre o madre"), 
               ('SB', "Sobrino/a"), ('SG', "Suegro/a"), ('TI', "Tío/a"), 
               ('YN', "Yerno o nuera"), ('TU', "Tutor/a"), ('OT', "Otro"),]
sexos = [('H', 'Hombre'), ('M', 'Mujer'), ('O', 'Otro'),]
tipos_documentos=[('NIF', "F - Número identificación fiscal (NIF)"), 
                  ('NIE', "E - Número de identidad de extranjero (NIE)"), 
                  ('PAS', "P - Número de pasaporte"), 
                  ('OTRO', "Otro"),]
tipos_establecimientos = [
    ('ALBERGUE', "Albergue"), ('APART', 'Apartamento'), ('APARTHOTEL', "Apartahotel"),
    ('AP_RURAL', "Apartamento rural"), ('BALNEARIO', "Balneario"), ('CAMPING', "Camping"),
    ('CASA_HUESP', "Casa de huéspedes"), ('CASA_RURAL', "Casa rural"), ('HOSTAL', "Hostal"),
    ('HOTEL', "Hotel"), ('H_RURAL', "Hotel rural"), ('MOTEL', "Motel"),
    ('OFIC_VEHIC', 'Oficina de alquiler de vehículos'), ('OTROS', "Otro"), ('PARADOR', "Parador de turismo"), 
    ('PENSION', "Pensión"), ('RESIDENCIA', "Residencia"),]
tipos_pago=[('EFECT', "Efectivo"), ('TARJT', "Tarjeta de crédito"), ('PLATF', "Plataforma de pago"), 
            ('TRANS', "Transferencia"), ('MOVIL', "Pago por móvil"), ('TREG', 'Tarjeta regalo'),
            ('DESTI', 'Pago en destino'), ('OTRO', "Otros medios de pago"),]
tipos_operacion=[('A', 'Alta'), ('C', 'Consulta'), ('B', 'Anulación')]
tipos_comunicacion=[('PV', 'Partes de viajeros'), ('AV', 'Alquileres de vehículos'), ('RH', 'Reservas de hospedaje'), ('RV', 'Reservas de vehículos de alquiler'),]


class enumStrType(baseStringType):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

class tipoComunicacionType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in tipos_comunicacion]:
            raise ValueError(f'Tipo de comunicación {v} no válido.')
        return v

class tipoOperacionType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in tipos_operacion]:
            raise ValueError(f'Tipo de operación {v} no válido.')
        return v


class rolType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in roles]:
            raise ValueError(f'Rol {v} no válido.')
        return v

class parentescoType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in parentescos]:
            raise ValueError(f'Parentesco {v} no válido.')
        return v

class sexoType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in sexos]:
            raise ValueError(f'Sexo {v} no válido.')
        return v
            
class tipoDocumentoType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in tipos_documentos]:
            raise ValueError(f'Tipo de documento {v} no válido.')
        return v

class tipoEstablecimientoType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in tipos_establecimientos]:
            raise ValueError(f'Tipo de establecimiento {v} no válido.')
        return v

class tipoPagoType(enumStrType):
    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v in [x[0] for x in tipos_pago]:
            raise ValueError(f'Tipo de pago {v} no válido.')
        return v