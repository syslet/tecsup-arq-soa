from flask import Flask
from spyne import Application, rpc, ServiceBase, Unicode, DateTime
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector

class RegistroService(ServiceBase):
    @rpc(DateTime, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, Unicode, _returns=Unicode)
    def registrar_cita(ctx, fecha_hora, especialidad, medico, dni_paciente, paciente, centro_salud, consultorio, estado):
        conn = mysql.connector.connect(host="mysql-db", user="root", password="root", database="salud")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO citas (fecha_hora, especialidad, medico, dni_paciente, paciente, centro_salud, consultorio, estado) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)",
            (fecha_hora, especialidad, medico, dni_paciente, paciente, centro_salud, consultorio, estado)
        )
        conn.commit()
        conn.close()
        return "Cita registrada exitosamente"

app = Flask(__name__)
application = Application([RegistroService], tns='health.citas', in_protocol=Soap11(), out_protocol=Soap11())
app.wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
