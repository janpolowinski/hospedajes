import pytest
from datetime import date, datetime
import app.tipos as t
from app.bloques import direccionType, contratoType
import app.partes as partes
import app.reservas as reservas



def test_contratante_type():    
    v = reservas.solicitudType.comunicacionType.personaType(        
        nombre='Juan',
        apellido1='  Apellido1',
        tipoDocumento='NIF',
        documento=' 12345678 - Z ',
        parentesco='PM',
        nacionalidad='ESP',
        apellido2=' Apellido2   ',
        telefono='123456789',
        direccion=direccionType(
            direccion="Calle Falsa 123",
            codigoPostal="28001",
            nombreMunicipio="Matalascañas",
            pais="ESP"),
        correo='test@example.com',
        fechaNacimiento='1980-01-01'
    )
    assert isinstance(v, t.hospedajesBaseType)
    assert isinstance(v, reservas.solicitudType.comunicacionType.personaType)    
    assert v.tipoDocumento == 'NIF'
    assert v.documento == '12345678Z'
    assert v.apellido1 == 'Apellido1'
    assert v.apellido2 == 'Apellido2'
    assert v.telefono == '123456789'
    assert v.correo == 'test@example.com'
    assert v.fechaNacimiento == date(1980, 1, 1)    

def test_nif():
    with pytest.raises(ValueError, match='Número de NIF 12345678X no válido'):
        v = reservas.solicitudType.comunicacionType.personaType(        
            nombre='Juan',
            apellido1='  Apellido1',
            tipoDocumento='NIF',
            documento=' 12345678 - X ',
            parentesco='PM',
            nacionalidad='ESP',
            apellido2=' Apellido2   ',
            telefono='123456789',
            direccion=direccionType(
                direccion="Calle Falsa 123",
                codigoPostal="28001",
                nombreMunicipio="Matalascañas",
                pais="ESP"),
            correo='test@example.com',
            fechaNacimiento='1980-01-01'
        )

def test_esp():
    with pytest.raises(ValueError, match='Sólo los españoles pueden tener NIF'):
        v = reservas.solicitudType.comunicacionType.personaType(        
            nombre='Juan',
            apellido1='  Apellido1',
            tipoDocumento='NIF',
            documento=' 12345678 - X ',
            parentesco='PM',
            # nacionalidad='ESP',
            apellido2=' Apellido2   ',
            telefono='123456789',
            direccion=direccionType(
                direccion="Calle Falsa 123",
                codigoPostal="28001",
                nombreMunicipio="Matalascañas",
                pais="ESP"),
            correo='test@example.com',
            fechaNacimiento='1980-01-01'
        )

def test_uno_de_los_tres():
    with pytest.raises(ValueError, match='Teléfono, teléfono2 o correo obligatorio'):
        v = reservas.solicitudType.comunicacionType.personaType(        
            nombre='Juan',
            apellido1='  Apellido1',
        )
