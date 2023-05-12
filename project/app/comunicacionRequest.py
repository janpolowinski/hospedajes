# comunicaciones con el servidor ses
import app.tipos as t
import app.bloques as b
import app.partes as p
import app.reservas as r
from app.utils import config, load_template, get_entorno, get_credenciales
import requests
from loguru import logger

#TODO: falta apartado 3.1.15 Consulta de lotes
#TODO: falta apartado 3.1.16 Anular comunicaciones

class peticionType(t.hospedajesBaseType):
    # Una petición está formada por una cabecera y una solicitud
    
    class cabeceraPeticionType(t.hospedajesBaseType):
        # La cabecera de una petición está formada por los datos del solicitante
        # y los datos de la aplicación que realiza la petición
        # así como el tipo de operación A Alta, C Consulta B Baja
        # y el tipo de comunicación, por ejemplo, RH Reservas de hospedaje o PV parte viajeros
        arrendador: str = get_entorno().get('arrendador')
        aplicacion: str = get_entorno().get('aplicacion')
        tipoOperacion: t.tipoOperacionType
        tipoComunicacion: t.tipoComunicacionType

    cabecera: cabeceraPeticionType
    # aqui va la solicitud **antes** de pasarla a XML, en ZIP y codificada en base64
    solicitud: p.solicitudType | r.solicitudType

    def to_xml(self):
        # devuelve la petición en XML, lista para enviar
        t=load_template(f'{config.fic_peticion}.jinja2')
        return t.render(p=self,
                        solicitud_codificada=self.solicitud.to_zip())
    
    def enviar(self)->tuple[int, str]:
        # envía la petición al servidor y devuelve la respuesta
        try:
            data = self.to_xml()
            #raise Exception(f'La petición es {data}')
            headers = {#'Content-Type': 'application/xml', 
                    'Authorization': f'Basic {get_credenciales()}'}
            
            
            logger.debug(f'El header es {headers}')
            #raise Exception(f'Las credenciales son {get_credenciales()}')
            logger.debug(f'Enviando petición')
            response = requests.get(
                    get_entorno()['url'], 
                    data=data, 
                    headers=headers,
                    verify=False)
            logger.debug(f'Recibida respuesta {response.status_code}: {response.text}')
            return response.status_code, response.text
        except Exception as e:
            logger.error(f'Error al enviar petición {e}')
            return 500, f'Error al enviar petición {e}'
