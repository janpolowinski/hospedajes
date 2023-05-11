# bloques de datos
# v3.0.0. 23-02-2023 (DD-MM-YYYY)
import app.tipos as tipos
from pydantic import validator, root_validator, Field, EmailStr, PastDate
from datetime import date
import re
from loguru import logger

MAYORIA_EDAD = 18

def mayor_edad(fechaNacimiento: date)->bool:
    # devuelve True si la persona es mayor de edad
    if fechaNacimiento is None:
        return False
    else:
        # Calcular la edad de la persona
        edad = date.today().year - fechaNacimiento.year - ((date.today().month, date.today().day) < (fechaNacimiento.month, fechaNacimiento.day))
        return edad >= MAYORIA_EDAD

def validar_nif(nif:str)->bool:
    """
    Valida un NIF o un NIE.

    Args:
        nif (str): el NIF o NIE a validar.

    Returns:
        bool: True si el NIF o NIE es válido, False si no lo es.
    """
    # Expresión regular para validar NIF o NIE
    regex = r'^[XYZ]?\d{7,8}[A-Z]$|^[0-9]{8}[A-Z]$'

    # Comprobar si el NIF o NIE es válido
    if re.match(regex, nif):
        # Obtener la letra del NIF o NIE
        letra = nif[-1]

        # Calcular el número del NIF o NIE
        numero = int(nif[:-1]) if nif.startswith(('X', 'Y', 'Z')) else int(nif[:-1])

        # Calcular el resto de la división del número del NIF o NIE entre 23
        resto = numero % 23

        # Obtener la letra correspondiente al resto
        letras = 'TRWAGMYFPDXBNJZSQVHLCKE'
        letra_correcta = letras[resto]

        # Comprobar si la letra es correcta
        if letra == letra_correcta:
            return True
        else:
            return False
    else:
        return False



class direccionType(tipos.hospedajesBaseType):
    # Bloque común (reservas, hospedajes) con datos de dirección de correo    
    # hay que indicar obligatoriamente uno de los dos campos
    # si es ESP, hay que indicar obligatoriamente el código de municipio o nombre de municipio
    # si no, obligatorio indicar el nombre de municipio
    # en definitiva, lo más sencillo es poner siempre el nombre de municipio
    # si conocemos el código de municipio, indicamos también el nombre de municipio,
    # por ello, hemos optado por definir nombreMunicipio como obligatorio
    pais: tipos.paisType
    nombreMunicipio: str = Field(default='', max_length=100, description="Nombre del municipio, ciudad, estado, etc. **Obligatorio** si el país no es España")    
    codigoMunicipio: tipos.codigoMunicipioType | None = None # si es España    
    direccion: str = Field(max_length=100, description="Dirección física. Calle, número, escalera, piso, puerta y demás.")
    direccionComplementaria: str = Field(default='', max_length=100, description="Dirección complementaria")    
    codigoPostal: tipos.codigoPostalType    
    
    @root_validator(skip_on_failure=True) # valida todos los campos, una vez seteados
    def validar_municipio(cls, values):
        _pais=values.get('pais', None)
        _codigoMunicipio=values.get('codigoMunicipio', None)
        _nombreMunicipio=values.get('nombreMunicipio', None)

        # si no es ESP, obligatorio el nombre de municipio
        if _pais!='ESP' and \
            (_nombreMunicipio is None or _nombreMunicipio==''):
            raise ValueError(f'Nombre de municipio obligatorio si el país no es España. Valores {values}')

        # si no es ESP, no puede haber código de municipio        
        if _pais!='ESP' and \
            (_codigoMunicipio is not None):
            raise ValueError(f'Código de municipio no válido si el país no es España')


        if _pais=='ESP':
            # si es ESP, obligatorio o codigoMunicipio o nombreMunicipio
            if (_nombreMunicipio is None or _nombreMunicipio=='') and \
                    (_codigoMunicipio is None or _codigoMunicipio==''):
                raise ValueError(f'Código de municipio o nombre obligatorio si el país es España. Valores {values}')

            # si hay código de municipio, forzar el nombre de municipio aunque se haya indicado
            if _codigoMunicipio is not None and _codigoMunicipio!='':
                # forzar el nombre de municipio
                if _codigoMunicipio not in tipos.municipios:
                    raise ValueError(f'Código de municipio no válido. Valores {_codigoMunicipio}')            
                values['nombreMunicipio']=tipos.municipios[_codigoMunicipio]
        return values


class datosEstablecimientoType(tipos.hospedajesBaseType):
    tipo: tipos.tipoEstablecimientoType
    nombre: str = Field(max_length=50, description="Nombre del establecimiento")
    direccion: direccionType

class contratoType(tipos.hospedajesBaseType):
    # un contrato, tanto en la reserva como en el hospedaje
    class pagoType(tipos.hospedajesBaseType):
        # Bloque común (reservas, hospedajes) con datos de pago        
        tipoPago: tipos.tipoPagoType # obligatorio        
        fechaPago: tipos.fechaType | None = None
        medioPago: str = Field(default='', max_length=50, description="Identificación del medio de pago: tipo de tarjeta y número, IBAN, número de móvil, etc.")
        titular: str = Field(default='', max_length=100, description="Nombre y apellidos del titular del pago")
        fechaCaducidadTarjeta: tipos.fechaType | None = None # no obligatorio, solo apuntar si tipoPago es TARJT
    
    referencia: str = Field(max_length=50, description="Número de referencia del contrato") # usualmente, el número de reserva
    fechaContrato: tipos.fechaType
    fechaEntrada: tipos.fechaHoraType
    fechaSalida: tipos.fechaHoraType
    numPersonas: int = Field(ge=1, le=99, description="Número de personas que ocupan el alojamiento")
    numHabitaciones: int | None
    internet: bool | None # indica si el alojamiento incluye conexión a internet
    pago : pagoType  # Contiene los datos del pago contrato

    @validator('numPersonas')
    def numPersonas_mayor_uno(cls, v):
        if v < 1 or v > 99:
            raise ValueError('Número de personas no válido. Debe estar entre 1 y 99')
        return v