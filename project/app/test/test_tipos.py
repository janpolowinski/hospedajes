import pytest
from datetime import date, datetime
import app.tipos as h
from loguru import logger
from pydantic import BaseModel, ValidationError, PastDate, Field
import arrow

def test_tipos():
    #
    # testear los tipos básicos

    
    class Prueba(BaseModel):
        nombre: h.nombreType
        fecha: h.fechaType
        fechaHora: h.fechaHoraType
        documento: h.documentoType
        pasado: PastDate
        nacionalidad: h.nacionalidadType
        pais: h.paisType
        municipio: h.codigoMunicipioType        
        codigoPostal: h.codigoPostalType
        rol: h.rolType
        parentesco: h.parentescoType
        sexo: h.sexoType
        tipo_documento: h.tipoDocumentoType
        establecimiento: h.tipoEstablecimientoType
        pago: h.tipoPagoType

    p = Prueba(
        nombre='   pepe   LUÍS     miguel  ', 
        fecha=h.fechaType.fromisoformat('1980-06-25'), 
        fechaHora=h.fechaHoraType.fromisoformat('1980-06-25T12:00:00'),
        documento=' 14 5 ñ 678-A ',
        pasado=date.fromisoformat('1980-06-25'),
        nacionalidad='ESP',
        pais='ARE',
        municipio='28079',        
        codigoPostal='07800',
        rol='TI',
        parentesco='HJ',
        sexo='H',
        tipo_documento='NIF',
        establecimiento='HOTEL',
        pago='TARJT'
        )

    # logger.info(p)
    # fecha    
    # comprobar que salga en formato AAAA-MM-DD
    assert str(p.fecha) == '1980-06-25'

    # fecha y hora
    assert p.fechaHora.year == 1980
    assert p.fechaHora.hour == 12
    # comprobar que salga en formato AAAA-MM-DDTHH:MM:SS
    assert str(p.fechaHora) == '1980-06-25T12:00:00'

    # documento, sin guiones o espacios, en mayúsculas
    assert p.documento == '145678A'

    # nombre
    assert p.nombre == 'Pepe Luís Miguel'




    # enumeracions
    """
    class PruebaEnum(BaseModel):
        sexo: h.sexoType

    p = PruebaEnum(sexo=h.sexoType.Hombre)
    logger.debug(p)

    p = PruebaEnum(sexo=2)
    logger.debug(p)

    logger.debug(f"El valor de hombre es {h.sexoType.Hombre.value}")

    for l in h.sexoType:
        logger.debug(f"El valor de {l} es {l.value}")
    """