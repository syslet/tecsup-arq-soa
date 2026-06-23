# Arquitectura Orientada a Servicios (SOA)

Implementación de Ecosistema con Python, Flask y Docker Compose

Infraestructura de Microservicios SOAP & ESB

### Integrante: Rene Plaz 


## ECOSISTEMA TECNOLÓGICO

### Backend Python
Uso de Flask y Spyne para la creación de servicios SOAP robustos y ligeros.

### Middleware ESB
Orquestación centralizada con WSO2 / Apache ServiceMix para enrutamiento.


### Contenerización
Docker Compose para gestionar 5 microservicios aislados y replicables.

## EL ROL CRÍTICO DEL ESB
El Bus de Servicios Empresariales actúa como el "sistema nervioso" de nuestra arquitectura SOA.

**Enrutamiento Inteligente:** Redirige peticiones SOAP al servicio correcto.

**Transformación:** Capacidad de adaptar mensajes entre protocolos si fuera necesario.

**Seguridad:** Punto único de aplicación de políticas de acceso.


## ARQUITECTURA DE LA SOLUCIÓN

```
                ┌─────────────────────────────┐
                │        Web App (Flask)      │
                │  Cliente SOAP (Zeep)        │
                │  Contenedor Docker          │
                └─────────────▲───────────────┘
                              │
                              │ SOAP Requests
                              │
                ┌─────────────┴───────────────┐
                │       Service Bus (ESB)     │
                │   WSO2 / Apache ServiceMix  │
                │   Contenedor Docker         │
                └─────────────▲───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        │                     │                     │
┌───────┴───────┐     ┌───────┴───────┐     ┌───────┴───────┐
│ Consulta SOAP │     │ Registro SOAP │     │ Actualización │
│ Flask+Spyne   │     │ Flask+Spyne   │     │ Flask+Spyne   │
│ Contenedor    │     │ Contenedor    │     │ Contenedor    │
└───────▲───────┘     └───────▲───────┘     └───────▲───────┘
        │                     │                     │
        └───────────────┬─────┴───────────────┬─────┘
                        │                     │
                        ▼                     ▼
                ┌───────────────────────────────────┐
                │        MySQL Database             │
                │   Contenedor Docker (init.sql)    │
                │   Tabla: citas                    │
                └───────────────────────────────────┘
```

**Capa Cliente:** Web App Python interactuando vía Cliente Zeep.

**Capa de Mediación:** Bus de Servicios (ESB) validando contratos SOAP.

**Capa de Servicios:** 3 Servicios SOAP especializados (Spyne).

**Capa de Datos:** Persistencia en MySQL con volúmenes Docker.


## DETALLE DE SERVICIOS SOAP

### Registro
Puerto: 5001  
Inserción de nuevas citas validando integridad de datos.  
http://localhost:5001/?wsdl

```xml
<wsdl:definitions xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:wsdlsoap11="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdlsoap12="http://schemas.xmlsoap.org/wsdl/soap12/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:soap11enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap12env="http://www.w3.org/2003/05/soap-envelope" xmlns:soap12enc="http://www.w3.org/2003/05/soap-encoding" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:http="http://schemas.xmlsoap.org/wsdl/http/" xmlns:tns="health.citas" targetNamespace="health.citas" name="Application">
<wsdl:types>
<xs:schema targetNamespace="health.citas" elementFormDefault="qualified">
<xs:complexType name="registrar_cita">
<xs:sequence>
<xs:element name="fecha_hora" type="xs:dateTime" minOccurs="0" nillable="true"/>
<xs:element name="especialidad" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="medico" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="dni_paciente" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="paciente" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="centro_salud" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="consultorio" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="estado" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:complexType name="registrar_citaResponse">
<xs:sequence>
<xs:element name="registrar_citaResult" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:element name="registrar_cita" type="tns:registrar_cita"/>
<xs:element name="registrar_citaResponse" type="tns:registrar_citaResponse"/>
</xs:schema>
</wsdl:types>
<wsdl:message name="registrar_cita">
<wsdl:part name="registrar_cita" element="tns:registrar_cita"/>
</wsdl:message>
<wsdl:message name="registrar_citaResponse">
<wsdl:part name="registrar_citaResponse" element="tns:registrar_citaResponse"/>
</wsdl:message>
<wsdl:service name="RegistroService">
<wsdl:port name="Application" binding="tns:Application">
<wsdlsoap11:address location="http://localhost:5001/"/>
</wsdl:port>
</wsdl:service>
<wsdl:portType name="Application">
<wsdl:operation name="registrar_cita" parameterOrder="registrar_cita">
<wsdl:input name="registrar_cita" message="tns:registrar_cita"/>
<wsdl:output name="registrar_citaResponse" message="tns:registrar_citaResponse"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="Application" type="tns:Application">
<wsdlsoap11:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="registrar_cita">
<wsdlsoap11:operation soapAction="registrar_cita" style="document"/>
<wsdl:input name="registrar_cita">
<wsdlsoap11:body use="literal"/>
</wsdl:input>
<wsdl:output name="registrar_citaResponse">
<wsdlsoap11:body use="literal"/>
</wsdl:output>
</wsdl:operation>
</wsdl:binding>
</wsdl:definitions>
```

### Consulta
Puerto: 5002   
Acceso a datos de citas existentes mediante filtros.  
http://localhost:5002/?wsdl
```xml
<wsdl:definitions xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:wsdlsoap11="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdlsoap12="http://schemas.xmlsoap.org/wsdl/soap12/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:soap11enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap12env="http://www.w3.org/2003/05/soap-envelope" xmlns:soap12enc="http://www.w3.org/2003/05/soap-encoding" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:http="http://schemas.xmlsoap.org/wsdl/http/" xmlns:tns="health.citas" targetNamespace="health.citas" name="Application">
<wsdl:types>
<xs:schema targetNamespace="health.citas" elementFormDefault="qualified">
<xs:complexType name="Cita">
<xs:sequence>
<xs:element name="id" type="xs:integer" minOccurs="0" nillable="true"/>
<xs:element name="fecha_hora" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="dni_paciente" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="paciente" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="especialidad" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="medico" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="centro_salud" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="consultorio" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="estado" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:complexType name="consulta_cita">
<xs:sequence>
<xs:element name="dni_paciente" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:complexType name="CitaArray">
<xs:sequence>
<xs:element name="Cita" type="tns:Cita" minOccurs="0" maxOccurs="unbounded" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:complexType name="consulta_citaResponse">
<xs:sequence>
<xs:element name="consulta_citaResult" type="tns:CitaArray" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:element name="Cita" type="tns:Cita"/>
<xs:element name="consulta_cita" type="tns:consulta_cita"/>
<xs:element name="CitaArray" type="tns:CitaArray"/>
<xs:element name="consulta_citaResponse" type="tns:consulta_citaResponse"/>
</xs:schema>
</wsdl:types>
<wsdl:message name="consulta_cita">
<wsdl:part name="consulta_cita" element="tns:consulta_cita"/>
</wsdl:message>
<wsdl:message name="consulta_citaResponse">
<wsdl:part name="consulta_citaResponse" element="tns:consulta_citaResponse"/>
</wsdl:message>
<wsdl:service name="ConsultaService">
<wsdl:port name="Application" binding="tns:Application">
<wsdlsoap11:address location="http://localhost:5002/"/>
</wsdl:port>
</wsdl:service>
<wsdl:portType name="Application">
<wsdl:operation name="consulta_cita" parameterOrder="consulta_cita">
<wsdl:input name="consulta_cita" message="tns:consulta_cita"/>
<wsdl:output name="consulta_citaResponse" message="tns:consulta_citaResponse"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="Application" type="tns:Application">
<wsdlsoap11:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="consulta_cita">
<wsdlsoap11:operation soapAction="consulta_cita" style="document"/>
<wsdl:input name="consulta_cita">
<wsdlsoap11:body use="literal"/>
</wsdl:input>
<wsdl:output name="consulta_citaResponse">
<wsdlsoap11:body use="literal"/>
</wsdl:output>
</wsdl:operation>
</wsdl:binding>
</wsdl:definitions>
```

### Actualización
Puerto: 5003  
Modificación de registros de citas existentes.  
http://localhost:5003/?wsdl

```xml
<wsdl:definitions xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:plink="http://schemas.xmlsoap.org/ws/2003/05/partner-link/" xmlns:wsdlsoap11="http://schemas.xmlsoap.org/wsdl/soap/" xmlns:wsdlsoap12="http://schemas.xmlsoap.org/wsdl/soap12/" xmlns:wsdl="http://schemas.xmlsoap.org/wsdl/" xmlns:soap11enc="http://schemas.xmlsoap.org/soap/encoding/" xmlns:soap11env="http://schemas.xmlsoap.org/soap/envelope/" xmlns:soap12env="http://www.w3.org/2003/05/soap-envelope" xmlns:soap12enc="http://www.w3.org/2003/05/soap-encoding" xmlns:wsa="http://schemas.xmlsoap.org/ws/2003/03/addressing" xmlns:xop="http://www.w3.org/2004/08/xop/include" xmlns:http="http://schemas.xmlsoap.org/wsdl/http/" xmlns:tns="health.citas" targetNamespace="health.citas" name="Application">
<wsdl:types>
<xs:schema targetNamespace="health.citas" elementFormDefault="qualified">
<xs:complexType name="actualizar_cita">
<xs:sequence>
<xs:element name="id" type="xs:string" minOccurs="0" nillable="true"/>
<xs:element name="nueva_fecha_hora" type="xs:dateTime" minOccurs="0" nillable="true"/>
<xs:element name="nuevo_estado" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:complexType name="actualizar_citaResponse">
<xs:sequence>
<xs:element name="actualizar_citaResult" type="xs:string" minOccurs="0" nillable="true"/>
</xs:sequence>
</xs:complexType>
<xs:element name="actualizar_cita" type="tns:actualizar_cita"/>
<xs:element name="actualizar_citaResponse" type="tns:actualizar_citaResponse"/>
</xs:schema>
</wsdl:types>
<wsdl:message name="actualizar_cita">
<wsdl:part name="actualizar_cita" element="tns:actualizar_cita"/>
</wsdl:message>
<wsdl:message name="actualizar_citaResponse">
<wsdl:part name="actualizar_citaResponse" element="tns:actualizar_citaResponse"/>
</wsdl:message>
<wsdl:service name="ActualizacionService">
<wsdl:port name="Application" binding="tns:Application">
<wsdlsoap11:address location="http://localhost:5003/"/>
</wsdl:port>
</wsdl:service>
<wsdl:portType name="Application">
<wsdl:operation name="actualizar_cita" parameterOrder="actualizar_cita">
<wsdl:input name="actualizar_cita" message="tns:actualizar_cita"/>
<wsdl:output name="actualizar_citaResponse" message="tns:actualizar_citaResponse"/>
</wsdl:operation>
</wsdl:portType>
<wsdl:binding name="Application" type="tns:Application">
<wsdlsoap11:binding style="document" transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="actualizar_cita">
<wsdlsoap11:operation soapAction="actualizar_cita" style="document"/>
<wsdl:input name="actualizar_cita">
<wsdlsoap11:body use="literal"/>
</wsdl:input>
<wsdl:output name="actualizar_citaResponse">
<wsdlsoap11:body use="literal"/>
</wsdl:output>
</wsdl:operation>
</wsdl:binding>
</wsdl:definitions>
```

## ORQUESTACIÓN CON DOCKER

**Docker Compose**
```yaml
version: '3.8'
services:
  mysql-db:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "3306:3306"
    command: --bind-address=0.0.0.0

  registro-service:
    build: ./registro
    ports:
      - "5001:5000"
    depends_on:
      - mysql-db

  consulta-service:
    build: ./consulta
    ports:
      - "5002:5000"
    depends_on:
      - mysql-db

  actualizacion-service:
    build: ./actualizacion
    ports:
      - "5003:5000"
    depends_on:
      - mysql-db

  service-bus:
    image: wso2/wso2mi:latest
    ports:
      - "8280:8280"
      - "9443:9443"
```
## DEMO

### Archivos
```
C:\citas\docker-compose.yml
C:\citas\init.sql

C:\citas\actualizacion\actualizacion.py
C:\citas\actualizacion\Dockerfile

C:\citas\consulta\consulta.py
C:\citas\consulta\Dockerfile 

C:\citas\registro\Dockerfile 
C:\citas\registro\registro.py

C:\citas\webapp\app.py 
C:\citas\webapp\Dockerfile 
C:\citas\webapp\requirements.txt 
C:\citas\webapp\templates
C:\citas\webapp\templates\actualizacion.html 
C:\citas\webapp\templates\consulta.html
C:\citas\webapp\templates\registro.html
```

### Iniciar Contenedores

```
C:\citas\docker compose up --build
```
```
C:\webapp\webapp\python app.py
```
**Cliente Web:**  http://127.0.0.1:8888

### Cliente Postman
#### SOA - Registro
```xml
postman request POST 'http://localhost:5001/' \
  --header 'Content-Type: text/xml;charset=UTF-8' \
  --body '<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hea="health.citas">
    <soapenv:Header/>
    <soapenv:Body>
        <hea:registrar_cita>
            <fecha_hora>2026-06-23T10:00:00</fecha_hora>
            <especialidad>Dental</especialidad>
            <medico>Dra. Piono</medico>
            <dni_paciente>10602835</dni_paciente>
            <paciente>Rene</paciente>
            <centro_salud>Hospital Vitarte</centro_salud>
            <consultorio>102</consultorio>
            <estado>Registrado</estado>
        </hea:registrar_cita>
    </soapenv:Body>
</soapenv:Envelope>'
```

#### SOA - Consulta
```xml
postman request POST 'http://localhost:5002/?wsdl=null' \
  --header 'Content-Type: text/xml;charset=UTF-8' \
  --body '<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hea="health.citas">
   <soapenv:Header/>
   <soapenv:Body>
      <hea:consulta_cita>
         <dni_paciente>10602835</dni_paciente>
      </hea:consulta_cita>
   </soapenv:Body>
</soapenv:Envelope>'
```

#### SOA - Actualización
```xml
postman request POST 'http://localhost:5003/' \
  --header 'Content-Type: text/xml;charset=UTF-8' \
  --body '<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:hea="health.citas">
   <soapenv:Header/>
   <soapenv:Body>
      <hea:actualizar_cita>
         <id>1</id>
         <nueva_fecha_hora>2026-06-23T11:00:00</nueva_fecha_hora>
         <nuevo_estado>Reprogramado</nuevo_estado>
      </hea:actualizar_cita>
   </soapenv:Body>
</soapenv:Envelope>'
```
