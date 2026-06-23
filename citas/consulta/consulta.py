from flask import Flask
from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel, Array
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector

# 1. Definimos la estructura de una Cita para que Spyne genere el XML formal
class Cita(ComplexModel):
    id = Integer
    fecha_hora = Unicode
    dni_paciente = Unicode
    paciente = Unicode
    especialidad = Unicode
    medico = Unicode
    centro_salud = Unicode
    consultorio = Unicode
    estado = Unicode

class ConsultaService(ServiceBase):
    # 2. Cambiamos el retorno de Unicode a un Arreglo (Array) de objetos Cita
    @rpc(Unicode, _returns=Array(Cita))
    def consulta_cita(ctx, dni_paciente):
        conn = mysql.connector.connect(host="mysql-db", user="root", password="root", database="salud")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, fecha_hora, dni_paciente, paciente, especialidad, medico, centro_salud, consultorio, estado FROM citas WHERE dni_paciente=%s", 
            (dni_paciente,)
        )
        
        # 3. Cambiamos fetchone() por fetchall() para traer todos los registros
        results = cursor.fetchall()
        conn.close()
        
        citas_lista = []
        
        # 4. Mapeamos cada fila de la BD al modelo de Spyne
        for row in results:
            cita = Cita(
                id=int(row[0]),
                fecha_hora=str(row[1]),
                dni_paciente=row[2],
                paciente=row[3],
                especialidad=row[4],
                medico=row[5],
                centro_salud=row[6],
                consultorio=row[7],
                estado=row[8]
            )
            citas_lista.append(cita)
            
        return citas_lista

app = Flask(__name__)
application = Application([ConsultaService], tns='health.citas', in_protocol=Soap11(), out_protocol=Soap11())
app.wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
