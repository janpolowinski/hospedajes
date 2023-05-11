import pytest
from datetime import date, datetime
import app.tipos as t
from app.bloques import direccionType, contratoType
import app.partes as partes
import app.reservas as reservas
import arrow
from app.utils import descomprimir_cadena_de_zip
from loguru import logger


solicitud=partes.solicitudType(
            codigoEstablecimiento='0000000107',
            comunicacion=[
            
                # parte número 1
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='123456789',
                        fechaContrato=arrow.get('2020-01-01').date(),
                        fechaEntrada=arrow.get('2020-01-01').datetime,
                        fechaSalida=arrow.get('2020-01-01').datetime,
                        numPersonas=2,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', apellido2=' rodrígez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', apellido2=' NMartínez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 58219929Y  ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),

                # parte número 2     
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='xxx789',
                        fechaContrato=arrow.get('2020-01-01').date(),
                        fechaEntrada=arrow.get('2020-01-01').datetime,
                        fechaSalida=arrow.get('2020-01-01').datetime,
                        numPersonas=2,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 86538575V ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 58219929Y ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),


            ]
        )



def test_persona_type_valido():    
    v = partes.solicitudType.comunicacionType.personaType(        
        nombre='Juan',
        apellido1='  Apellido1',
        tipoDocumento='NIF',
        documento=' 12345678 - Z ',
        soporte='123',
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
    assert isinstance(v, partes.solicitudType.comunicacionType.personaType)    
    assert v.tipoDocumento == 'NIF'
    assert v.documento == '12345678Z'
    assert v.soporte == '123'
    assert v.parentesco == 'PM'
    assert v.apellido1 == 'Apellido1'
    assert v.apellido2 == 'Apellido2'
    assert v.telefono == '123456789'
    assert v.correo == 'test@example.com'
    assert v.fechaNacimiento == date(1980, 1, 1)


def test_solicitud():
    partes.solicitudType(
        codigoEstablecimiento='123456789',
        comunicacion=[
        
            # parte número 1
            partes.solicitudType.comunicacionType(
                # contrato
                contrato=contratoType(
                    referencia='123456789',
                    fechaContrato='2020-01-01',
                    fechaEntrada='2020-01-01',
                    fechaSalida='2020-01-01',
                    numPersonas=2,
                    pago=contratoType.pagoType(
                            tipoPago='TARJT',                            
                        )
                    ),
                # personas
                persona=[
                    partes.solicitudType.comunicacionType.personaType(
                        rol='TI', nombre='Juan', apellido1=' sin miedo ', apellido2=' rodrígez ', fechaNacimiento='1980-01-01',
                        tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                        direccion=direccionType(
                            direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                        ), telefono='234545'
                    ),
                    partes.solicitudType.comunicacionType.personaType(
                        rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', apellido2=' NMartínez ', fechaNacimiento='1980-01-01',
                        tipoDocumento='NIF', documento=' 33510091B ', soporte='123', nacionalidad='ESP',
                        direccion=direccionType(
                            direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                        ), telefono='949857857', correo='falso@falso.com'
                    ),
                ]
            ),

            # parte número 2     
            partes.solicitudType.comunicacionType(
                # contrato
                contrato=contratoType(
                    referencia='xxx789',
                    fechaContrato='2020-01-01',
                    fechaEntrada='2020-01-01',
                    fechaSalida='2020-01-01',
                    numPersonas=2,
                    pago=contratoType.pagoType(
                            tipoPago='TARJT',                            
                        )
                    ),
                # personas
                persona=[
                    partes.solicitudType.comunicacionType.personaType(
                        rol='TI', nombre='Juan', apellido1=' sin miedo ', fechaNacimiento='1980-01-01',
                        tipoDocumento='PAS', documento=' 86538575V ', soporte='123', nacionalidad='ESP',
                        direccion=direccionType(
                            direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                        ), telefono='234545'
                    ),
                    partes.solicitudType.comunicacionType.personaType(
                        rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', fechaNacimiento='1980-01-01',
                        tipoDocumento='PAS', documento=' 58219929Y ', soporte='123', nacionalidad='ESP',
                        direccion=direccionType(
                            direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                        ), telefono='949857857', correo='falso@falso.com'
                    ),
                ]
            ),


        ]
    )


def test_partes_mas_viajeros_que_contrato():
    with pytest.raises(ValueError, match='Hay más viajeros que personas en el contrato'):    
        partes.solicitudType(
            codigoEstablecimiento='123456789',
            comunicacion=[
            
                # parte número 1
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='123456789',
                        fechaContrato='2020-01-01',
                        fechaEntrada='2020-01-01',
                        fechaSalida='2020-01-01',
                        numPersonas=1,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', apellido2=' rodrígez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', apellido2=' NMartínez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 33510091B ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),

                # parte número 2     
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='xxx789',
                        fechaContrato='2020-01-01',
                        fechaEntrada='2020-01-01',
                        fechaSalida='2020-01-01',
                        numPersonas=1,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 86538575V ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 58219929Y ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),


            ]
        )


def test_partes_mismo_id():
    with pytest.raises(ValueError, match='Documento de identidad 12345678Z repetido en viajeros del contrato 123456789'):
        partes.solicitudType(
            codigoEstablecimiento='123456789',
            comunicacion=[
            
                # parte número 1
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='123456789',
                        fechaContrato='2020-01-01',
                        fechaEntrada='2020-01-01',
                        fechaSalida='2020-01-01',
                        numPersonas=1,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', apellido2=' rodrígez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', apellido2=' NMartínez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),

                # parte número 2     
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='xxx789',
                        fechaContrato='2020-01-01',
                        fechaEntrada='2020-01-01',
                        fechaSalida='2020-01-01',
                        numPersonas=1,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 86538575V ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 58219929Y ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),


            ]
        )    

def test_partes_xml_valida():
    # pasamos la solicitud a xml
    p=partes.solicitudType(
            codigoEstablecimiento='123456789',
            comunicacion=[
            
                # parte número 1
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='123456789',
                        fechaContrato=arrow.get('2020-01-01').date(),
                        fechaEntrada=arrow.get('2020-01-01').datetime,
                        fechaSalida=arrow.get('2020-01-01').datetime,
                        numPersonas=2,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', apellido2=' rodrígez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 12345678 - Z ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', apellido2=' NMartínez ', fechaNacimiento='1980-01-01',
                            tipoDocumento='NIF', documento=' 58219929Y  ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),

                # parte número 2     
                partes.solicitudType.comunicacionType(
                    # contrato
                    contrato=contratoType(
                        referencia='xxx789',
                        fechaContrato=arrow.get('2020-01-01').date(),
                        fechaEntrada=arrow.get('2020-01-01').datetime,
                        fechaSalida=arrow.get('2020-01-01').datetime,
                        numPersonas=2,
                        pago=contratoType.pagoType(
                                tipoPago='TARJT',                            
                            )
                        ),
                    # personas
                    persona=[
                        partes.solicitudType.comunicacionType.personaType(
                            rol='TI', nombre='Juan', apellido1=' sin miedo ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 86538575V ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='234545'
                        ),
                        partes.solicitudType.comunicacionType.personaType(
                            rol='VI', nombre='María de los Remedios', apellido1=' García Herrera ', fechaNacimiento='1980-01-01',
                            tipoDocumento='PAS', documento=' 58219929Y ', soporte='123', nacionalidad='ESP',
                            direccion=direccionType(
                                direccion='Calle Falsa 123', codigoPostal='28001', nombreMunicipio='Matalascañas', pais='ESP'
                            ), telefono='949857857', correo='falso@falso.com'
                        ),
                    ]
                ),


            ]
        )    
    assert p.valida_xml() == True


def test_partes_xml_comprime():
    # pasamos la solicitud a xml y la comprimimos en zip y se codifica en base64

    #assert solicitud.valida_xml() == True
    #raise Exception(solicitud.to_xml())
    assert descomprimir_cadena_de_zip(solicitud.to_zip()) == solicitud.to_xml()

def test_genera_fichero_partes():
    # generamnos el fichero de partes
    try:
        with open('envio_parte.xml', 'w') as envio:
            envio.write(solicitud.to_xml())
    except Exception as e:
        logger.error(f"Error al escribir el fichero de partes: {e}")
        raise Exception(f"Error al escribir el fichero de partes: {e}")
    # logger.info(solicitud.to_xml())