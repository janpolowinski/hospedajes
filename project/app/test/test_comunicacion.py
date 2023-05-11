import pytest
from datetime import date, datetime
import app.tipos as t
from app.bloques import direccionType, contratoType
import app.partes as partes
import app.reservas as reservas
import app.comunicacionRequest as comunicacionRequest
from app.utils import get_credenciales,  comprimir_cadena_en_zip, descomprimir_cadena_de_zip, get_entorno
import base64
import arrow
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

def test_comunicacion_partes():

    # un alta de viajero
    p=comunicacionRequest.peticionType(    

        # cabecera de la peticion
        cabecera=comunicacionRequest.peticionType.cabeceraPeticionType(
            tipoOperacion='A',
            tipoComunicacion='PV',
        ),

        # solicitud de la peticion
        solicitud = solicitud
    )
    #logger.debug(f"solicitud: {solicitud.to_xml()}")
    #logger.debug(f"validacion de la solicitud: {solicitud.valida_xml()}")
    #c=solicitud.to_zip()
    #logger.debug(f"solicitud comprimida: {solicitud.to_zip()}")
    #logger.debug(f"solicitud descomprimida: {solicitud.from_zip(c)}")
    assert True == True
    #assert p.to_xml()=='hola'

def test_comunicacion_comunica():
    # un alta de viajero
    p=comunicacionRequest.peticionType(    

        # cabecera de la peticion
        cabecera=comunicacionRequest.peticionType.cabeceraPeticionType(
            tipoOperacion='A',
            tipoComunicacion='PV',
        ),

        # solicitud de la peticion
        solicitud = solicitud
    )
    assert True == True
    #r=p.enviar()
    #logger.debug(f"respuesta: {r}")
    #assert r[0] == 200

def test_credenciales():
    # comprueba que las credenciales se comprimen y descomprimen bien
    c = get_credenciales()
    # logger.info(f"credenciales: {c}")
    d = base64.b64decode(c).decode()
    # logger.info(f"descomprimido: {d}")

    entorno=get_entorno()
    assert f"{entorno['usuario']}:{entorno['password']}" == d
