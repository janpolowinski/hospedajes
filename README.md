# Hospedajes

Nuevo sistema español de información de hospedajes y alquiler de vehículos.

Un conjunto de herramientas para realizar las comunicaciones. Actualmente, según la versión 3.0.0. del interface.

De momento, sólo están definidos los tipos de datos y las plantillas para generar y/o enviar los partes de hospedaje. No hay soporte para alquiler de vehículos. 

La idea es compartir estas librerias para facilitar la implementación del sistema en los establecimientos.

¡Se aceptan colaboraciones!

## Arranque

Crear la imagen de Docker con `docker compose build` en el directorio raíz del proyecto y lanzar el contendor con `docker compose run hospedajes`. 

En la linea de comandos hacemos `cd app; source t.sh` para ejecutar los tests. 

## Configuración

1. En `project/app/config.yml` guardar los datos del establecimiento. 
2. `source t.sh` para ejecutar los tests

## Uso

En el directorio de tests `project/app/tests` hay un ejemplos de uso de las plantillas para crear, validar y generar los partes de hospedaje.

## Comunicaciones con el servidor

Pueden hacerse la pruebas de tipos en local y dejar las comunicaciones con el servidor para el final. 

Guardar los archivos ACCOMP.crt y PRE_SGSICS.SES.MIR.ES.cer, facilitados por la subsecretaría, en `project/app/soporte`. En el `Dockerfile` quitar las lineas comentadas que copian los archivos de certificados y recrear la imagen con `docker compose build -t hospedajes .`

```Dockerfile
# COPY app/soporte/PRE_SGSICS.SES.MIR.ES.cer /usr/local/share/ca-certificates/
# RUN update-ca-certificates
```

En `comunicacionRequest.py` hay una función de envio de partes al servidor.
