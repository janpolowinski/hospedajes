# Alta de partes de viajeros
# Tipo de operación: A, tipo de comunicación: PV
from pydantic import root_validator
import app.tipos as t
import app.bloques as b
from app.utils import config, load_template, validar_xml_con_xsd, comprimir_cadena_en_zip, descomprimir_cadena_de_zip

class solicitudType(t.hospedajesBaseType):   
    # Una solicitud de comunicación de partes está formada por un establecimiento y una lista de comunicaciones
    # por ejemplo, todos los partes de viajeros de un establecimiento en un día o una hora o tiempo real

    class comunicacionType(t.hospedajesBaseType):
        # Comunicación de un parte de viajeros (Reserva+Viajeros)
        # Una comunicación está formada por un contrato de reserva y 
        # una lista de viajeros incluidos en la reserva

        class personaType(t.hospedajesBaseType):
            # una persona en un parte de viajero
            # TODO: si no hay teléfno o correo de un menor, copiar el de su parentesco                    
            rol: t.rolType = 'TI' # titular por defecto
            nombre: t.nombreType
            apellido1: t.nombreType
            apellido2: t.nombreType | None
            fechaNacimiento: t.fechaNacimientoType
            tipoDocumento: t.tipoDocumentoType | None 
            documento : t.documentoType | None    
            nacionalidad: t.nacionalidadType | None
            sexo: t.sexoType | None
            direccion: b.direccionType # dirección del domicilio particular

            # obligatorio uno de los tres siguientes
            telefono: t.telefonoType | None
            telefono2: t.telefonoType | None
            correo: t.emailType | None

            soporte: t.soporteDocumentoType | None
            parentesco : t.parentescoType | None # obligatorio si es menor de edad

            @root_validator() # skip_on_failure=True) # valida todos los campos, una vez seteados
            def validar_persona(cls, values):        
                # valida la documentación según edad, tipo de documento y parentesco
                _fechaNacimiento = values.get('fechaNacimiento', None)
                _tipoDocumento = values.get('tipoDocumento', None)
                _documento = values.get('documento', None)
                _parentesco = values.get('parentesco', None)
                _soporte = values.get('soporte', None)
                _apellido2 = values.get('apellido2', None)
                _nacionalidad = values.get('nacionalidad', None)

                if not _fechaNacimiento:
                    raise ValueError(f'Fecha de nacimiento no presente {values}')
                
                if b.mayor_edad(_fechaNacimiento):
                    # es mayor de edad
                    if not _tipoDocumento:
                        raise ValueError('Tipo de documento obligatorio para mayores de edad')
                    if not _documento:
                        raise ValueError('Mayor de edad sin documento')
                    if not _nacionalidad:
                        raise ValueError('Mayor de edad sin nacionalidad')            
                else: 
                    # es menor de edad
                    if not _parentesco:
                        raise ValueError('Parentesco no presente y es menor de edad')

                # sólo los españoles pueden tener NIF
                if _tipoDocumento and _tipoDocumento == 'NIF' and _nacionalidad and _nacionalidad != 'ESP':
                    raise ValueError('Sólo los españoles pueden tener NIF')

                # apellido2 obligatorio si el documento es NIF 
                if _tipoDocumento and _tipoDocumento == 'NIF' and not _apellido2:
                    raise ValueError('Segundo apellido obligatorio si el documento es NIF')        

                # soporte de docuemnto obligario si tipoDocumento es NIF o NIE
                if (_tipoDocumento=='NIF' or _tipoDocumento=='NIE') and not _soporte:
                    raise ValueError('Soporte de documento obligario si el tipo de documento es NIF o NIE')

                # validar el NIF o NIE
                if _tipoDocumento and (_tipoDocumento == 'NIF' or _tipoDocumento == 'NIE') and not b.validar_nif(_documento):
                    raise ValueError(f'Número de NIF {_documento} no válido')

                # uno de los tres obligatorio
                if not values.get('telefono', None) and \
                not values.get('telefono2', None) and \
                not values.get('correo', None):
                    raise ValueError('Teléfono, teléfono2 o correo obligatorio')        
                return values

            def to_xml(self)->str:
                # convierte la persona a xml
                t=load_template('persona.jinja2')
                return t.render(config=config, persona=self)

        contrato: b.contratoType
        persona: list[personaType]

        @root_validator() # skip_on_failure=True) # valida todos los campos, una vez seteados
        def validar_comunicacion(cls, values):        
            # valida la comunicacion
            # no dos viajeros con el mismo documento
            # no mas viajeros que numPersonas
            # al menos una persona con el rol viajero VI            

            # no dos viajeros con el mismo documento
            _documentos = []
            for _persona in values.get('persona', []):
                _documento = _persona.documento
                if _documento in _documentos:
                    raise ValueError(f'Documento de identidad {_documento} repetido en viajeros del contrato {values.get("contrato", {}).referencia}.')
                _documentos.append(_documento)

            # no mas viajeros que numPersonas en el contrato
            _numPersonas = values.get('contrato', {}).numPersonas
            if _numPersonas and len(values.get('persona', [])) > _numPersonas:
                raise ValueError(f'Hay más viajeros que personas en el contrato')
            
            # al menos una persona con el rol viajero VI
            _viajeros = [p for p in values.get('persona') if p.rol == 'VI']
            if len(_viajeros) == 0:
                raise ValueError(f'No hay ningún viajero. Al menos una persona debe tener el rol VI')

            return values

    codigoEstablecimiento: str # una cadena puede tener más de un establecimiento
    comunicacion: list[comunicacionType] # comunicaciones de un establecimiento durante un día, una hora

    def to_xml(self):
        # convierte la solicitud a xml
        t=load_template(f'{config.fic_partes}.jinja2')
        return t.render(config=config, solicitud=self)
    
    def valida_xml(self)->bool:
        # valida la solicitud
        return validar_xml_con_xsd(            
            self.to_xml(),            
            f'{config.fic_partes}.xsd')
    
    def to_zip(self)->str:
        # valida y convierte la solicitud a zip, codificado en base64
        if self.valida_xml():
            return comprimir_cadena_en_zip(self.to_xml())
        else:
            raise ValueError('La solicitud no es válida')
    
    def from_zip(self, zip64:str)->str:
        # carga la solicitud desde un zip codificado en base64
        return descomprimir_cadena_de_zip(zip64)