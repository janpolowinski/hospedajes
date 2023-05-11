import pytest
from datetime import date, datetime
import app.tipos as t
from app.bloques import direccionType, contratoType
from app import partes
from loguru import logger
import arrow
from pydantic import EmailStr

def test_direccion():
    # Creamos una instancia válida de la clase
    direccion = direccionType(
        direccion="Calle Falsa 123",
        codigoPostal="28001",     
        nombreMunicipio="Madrid1",
        pais="ESP"
    )

    # Comprobamos que la instancia es válida
    assert direccion is not None
    assert direccion.direccion == "Calle Falsa 123"
    assert direccion.codigoPostal == "28001"
    assert direccion.nombreMunicipio == "Madrid1"
    assert direccion.pais == "ESP"

    # pais no ESP sin nombre ni codigo de municipio
    with pytest.raises(ValueError):
        direccion = direccionType(
            direccion="Calle Falsa 123",
            codigoPostal="28001",
            pais="ARE"
        )    

    # sobreescribir automáticamente nombre de municipio
    direccion = direccionType(
        direccion="Calle Falsa 123",
        codigoPostal="28001",
        codigoMunicipio="01006",
        nombreMunicipio="Madrid2",
        pais="ESP"
    )
    assert direccion.nombreMunicipio == "Armiñón"

    # codigo municipio pais no ESP
    with pytest.raises(ValueError):
        direccion = direccionType(
            direccion="Calle Falsa 123",
            codigoPostal="28001",
            codigoMunicipio="01006",
            nombreMunicipio="Madrid2",
            pais="ARG"
        )

    # pais no ESP con nombre, sin código de municipio
    direccion = direccionType(
            direccion="Calle Falsa 123",
            nombreMunicipio="Madrid3",
            codigoPostal="28001",
            pais="ARE"
        )    


    # pais no ESP con código, sin nombre de municipio
    with pytest.raises(ValueError):
        direccion = direccionType(
                direccion="Calle Falsa 123",
                codigoMunicipio="26005",
                codigoPostal="28001",
                pais="DEU"
            )        
    # pais ESP con código, sin nombre de municipio
    direccion = direccionType(
            pais="ESP",
            direccion="Calle Falsa con dódigo, sin nombre de municipio",
            codigoMunicipio="01060",
            codigoPostal="28001",            
        )    
    

    # ESP, ni codigo de municipio ni nombre de municipio
    with pytest.raises(ValueError):
        direccion = direccionType(
            direccion="Calle Falsa 123",
            codigoPostal="28001",
            pais="ESP"
        )    


def test_contrato_valido():
    # Crear un contrato válido
    contrato = contratoType(
        referencia='R001',
        fechaContrato=datetime.now(),
        fechaEntrada=datetime.now(),
        fechaSalida=datetime.now(),
        numPersonas=2,
        numHabitaciones=1,
        internet=True,
        pago=contratoType.pagoType(
            tipoPago='TARJT',
            medioPago='1234567890123456',
            titular='Juan Pérez',
            fechaCaducidadTarjeta=datetime.now(),
        ),
    )
    assert contrato.referencia == 'R001'
    assert isinstance(contrato.fechaContrato, datetime)
    assert isinstance(contrato.fechaEntrada, datetime)
    assert isinstance(contrato.fechaSalida, datetime)
    assert contrato.numPersonas == 2
    assert contrato.numHabitaciones == 1
    assert contrato.internet == True
    assert contrato.pago.tipoPago == 'TARJT'
    assert contrato.pago.medioPago == '1234567890123456'
    assert contrato.pago.titular == 'Juan Pérez'
    assert isinstance(contrato.pago.fechaCaducidadTarjeta, datetime)

def test_contrato_sin_referencia():
    # Crear un contrato sin referencia (obligatoria)
    with pytest.raises(ValueError):
        contratoType(
            fechaContrato=datetime.now(),
            fechaEntrada=datetime.now(),
            fechaSalida=datetime.now(),
            numPersonas=2,
            numHabitaciones=1,
            internet=True,
            pago=contratoType.pagoType(
                tipoPago='TARJT',
                medioPago='1234567890123456',
                titular='Juan Pérez',
                fechaCaducidadTarjeta=datetime.now(),
            ),
        )

def test_contrato_sin_fecha_contrato():
    # Crear un contrato sin fecha de contrato (obligatoria)
    with pytest.raises(ValueError):
        contratoType(
            referencia='R001',
            fechaEntrada=datetime.now(),
            fechaSalida=datetime.now(),
            numPersonas=2,
            numHabitaciones=1,
            internet=True,
            pago=contratoType.pagoType(
                tipoPago='TARJT',
                medioPago='1234567890123456',
                titular='Juan Pérez',
                fechaCaducidadTarjeta=datetime.now(),
            ),
        )

def test_contrato_invalido_tipo_pago():
    # Crear un contrato con un tipo de pago no válido
    with pytest.raises(ValueError):
        contratoType(
            referencia='R001',
            fechaContrato=datetime.now(),
            fechaEntrada=datetime.now(),
            fechaSalida=datetime.now(),
            numPersonas=2,
            numHabitaciones=1,
            internet=True,
            pago=contratoType.pagoType(
                tipoPago='CASH',
                medioPago='1234567890123456',
                titular='Juan Pérez',
            ),
        )


direcc=direccionType(
            direccion="Calle Falsa 123",
            codigoPostal="28001",
            nombreMunicipio="Matalascañas",
            pais="ESP")

def test_fecha_nacimiento_no_nula():
    with pytest.raises(ValueError):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=None)

def test_fecha_nacimiento_valida():
    with pytest.raises(ValueError):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(2100, 1, 1))

def test_documento_obligatorio_si_mayor_edad():
    with pytest.raises(ValueError):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1), tipoDocumento=None)

def test_documento_valido():
    with pytest.raises(ValueError, match='Número de NIF 123456789 no válido'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   nombre='Juan', telefono='asdfas', nacionalidad='ESP', 
        apellido1='  Apellido1', apellido2='algo ruiz', tipoDocumento='NIF', direccion=direcc, 
        soporte='1233', 
        documento='123456789')

def test_soporte_documento_obligatorio_si_nif():
    with pytest.raises(ValueError, match='Soporte de documento obligario si el tipo de documento es NIF o NIE'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   
                    nombre='Juan', telefono='789686', nacionalidad='ESP',
        apellido1='  Apellido1', apellido2='algo ruiz', tipoDocumento='NIF', 
        direccion=direcc, documento='12345678Z')

def test_parentesco_obligatorio_si_menor_edad():
    with pytest.raises(ValueError, match='Parentesco no presente y es menor de edad'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(2020, 1, 1),   
                    nombre='Juan', telefono='789686', nacionalidad='ESP',
        apellido1='  Apellido1', apellido2='algo ruiz', tipoDocumento='NIF', 
        direccion=direcc, documento='12345678Z')

def test_mayor_edad_sin_nacionalidad():
    with pytest.raises(ValueError, match='Mayor de edad sin nacionalidad'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   
                    nombre='Juan', telefono='789686', 
        apellido1='  Apellido1', apellido2='algo ruiz', tipoDocumento='NIF', 
        direccion=direcc, documento='12345678Z')

def test_nif_no_espanol():
    with pytest.raises(ValueError, match='Sólo los españoles pueden tener NIF'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   
                    nombre='Juan', telefono='789686', soporte='343', nacionalidad='FRA',
        apellido1='  Apellido1', apellido2='algo ruiz', tipoDocumento='NIF', 
        direccion=direcc, documento='12345678Z')

def test_apellido2_obligatorio_si_nif():
    with pytest.raises(ValueError, match='Segundo apellido obligatorio si el documento es NIF'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   
                    nombre='Juan', telefono='789686', soporte='343', nacionalidad='ESP',
        apellido1='  Apellido1', tipoDocumento='NIF', 
        direccion=direcc, documento='12345678Z')

def test_telefono_o_correo_obligatorio():
    with pytest.raises(ValueError, match='Teléfono, teléfono2 o correo obligatorio'):
        partes.solicitudType.comunicacionType.personaType(fechaNacimiento=date(1990, 1, 1),   
                    nombre='Juan', soporte='343', nacionalidad='ESP',
                    apellido1='  Apellido1', tipoDocumento='NIF', apellido2='giménez',
                    direccion=direcc, documento='12345678Z')
