from flask import Flask
from spyne import Application, rpc, ServiceBase, Unicode, DateTime
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import mysql.connector

class ActualizacionService(ServiceBase):
    @rpc(Unicode, DateTime, Unicode,_returns=Unicode)
    def actualizar_cita(ctx, id, nueva_fecha_hora, nuevo_estado):
        conn = mysql.connector.connect(host="mysql-db", user="root", password="root", database="salud")
        cursor = conn.cursor()
        cursor.execute("UPDATE citas SET fecha_hora=%s, estado=%s WHERE id=%s", (nueva_fecha_hora, nuevo_estado, id))
        conn.commit()
        conn.close()
        return "Cita actualizada exitosamente"

app = Flask(__name__)
application = Application([ActualizacionService], tns='health.citas', in_protocol=Soap11(), out_protocol=Soap11())
app.wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
