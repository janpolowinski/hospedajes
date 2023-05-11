# Alta de reservas de hospedaje
# Tipo de operación: A, tipo de comunicación: RH
from pydantic import validator, root_validator
import app.tipos as t
import app.bloques as b

class solicitudType(t.hospedajesBaseType):   
    # solicitud con las reservas de uno o varios establecimientos, por ejemplo, durante un día

    class comunicacionType(t.hospedajesBaseType):
        # Comunicación de una reserva
        # Una comunicación está formada por un establecimiento, un contrato de reserva y 
        # una lista de viajeros incluidos en la reserva

        class establecimientoType(t.hospedajesBaseType):
            # Establecimiento de un contrato de reserva
            # es obligatorio o el código o los datos del establecimiento
            codigo: t.codigoEstablecimientoType | None
            datosEstablecimiento: b.datosEstablecimientoType | None

            @root_validator() #  valida todos los campos, una vez seteados
            def validar_no_nulos(cls, values):        
                # o codigo o datosEstablecimiento
                if not values.get('codigo', None) and not values.get('datosEstablecimiento', None):
                    raise ValueError('Debe indicar o código datos del establecimiento')        
                return values

        class personaType(t.hospedajesBaseType):
            # es como un viajero pero sin soporte ni parentesco
            # la mayoría de validaciones no se aplican, además, la fecha de nacimiento y la dirección no son obligatorias
            # en la v3.0.0.0 se tiene que poner telefono, telefono2 o correo aunque sea menor de edad
            rol: t.rolType = 'TI' # titular por defecto
            nombre: t.nombreType
            apellido1: t.nombreType
            apellido2: t.nombreType | None
            fechaNacimiento: t.fechaNacimientoType | None
            tipoDocumento: t.tipoDocumentoType | None 
            documento : t.documentoType | None    
            nacionalidad: t.nacionalidadType | None
            sexo: t.sexoType | None
            direccion: b.direccionType | None

            # obligatorio uno de los tres siguientes
            telefono: t.telefonoType | None
            telefono2: t.telefonoType | None
            correo: t.emailType | None

            @root_validator() # skip_on_failure=True) # valida todos los campos, una vez seteados
            def validar_documentacion(cls, values):        
                # valida la documentación según edad, tipo de documento y parentesco        
                _tipoDocumento = values.get('tipoDocumento', None)
                _documento = values.get('documento', None)        
                _nacionalidad = values.get('nacionalidad', None)
                
                # sólo los españoles pueden tener NIF
                if _tipoDocumento and _tipoDocumento == 'NIF' and ((_nacionalidad and _nacionalidad != 'ESP') or not _nacionalidad):
                    raise ValueError('Sólo los españoles pueden tener NIF')

                # validar el NIF o NIE
                if _tipoDocumento and (_tipoDocumento == 'NIF' or _tipoDocumento == 'NIE') and not b.validar_nif(_documento):
                    raise ValueError(f'Número de NIF {_documento} no válido')

                # uno de los tres obligatorio
                if not values.get('telefono', None) and \
                not values.get('telefono2', None) and \
                not values.get('correo', None):
                    raise ValueError('Teléfono, teléfono2 o correo obligatorio')        

                return values

        establecimiento: establecimientoType
        contrato: b.contratoType
        viajeros: list[personaType]

    comunicacion: list[comunicacionType]