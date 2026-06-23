from flask import Flask, render_template, request, redirect, url_for
from zeep import Client
from datetime import datetime

app = Flask(__name__)

# ---------------------------
# Registro de citas
# ---------------------------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        fecha_hora = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        especialidad = request.form["especialidad"]
        medico = request.form["medico"]
        dni_paciente = request.form["dni_paciente"]
        paciente = request.form["paciente"]
        centro_salud = request.form["centro_salud"]
        consultorio = request.form["consultorio"]
        estado = request.form["estado"]

        client = Client("http://localhost:5001/?wsdl")
        result = client.service.registrar_cita(
            fecha_hora, especialidad, medico, dni_paciente, paciente, centro_salud, consultorio, estado
        )
        return f"Resultado: {result} <hr/><a href='http://127.0.0.1:8888/'>volver</a>"

    return render_template("registro.html")

# ---------------------------
# Consulta de citas
# ---------------------------
@app.route("/consulta/<dni_paciente>")
def consulta(dni_paciente):    
    client = Client("http://localhost:5002/?wsdl")
    citas = client.service.consulta_cita(dni_paciente)
    return render_template("consulta.html", citas=citas, dni=dni_paciente)

# ---------------------------
# Actualización de citas
# ---------------------------
@app.route("/actualizacion/<id>", methods=["GET", "POST"])
def actualizacion(id):
    if request.method == "POST":
        nueva_fecha = request.form["fecha_hora"]
        nuevo_estado = request.form["estado"]

        client = Client("http://localhost:5003/?wsdl")
        result = client.service.actualizar_cita(id, nueva_fecha, nuevo_estado)
        return f"Resultado: {result} <hr/><a href='http://127.0.0.1:8888/'>volver</a>"

    return render_template("actualizacion.html", id=id)

# ---------------------------
# Inicio
# ---------------------------
@app.route("/")
def home():
    return """
    <h2>Menú Principal</h2>
    <ul>
      <li><a href='/registro'>Registrar Cita</a></li>
      <li><a href='/consulta/10602835'>Consultar Citas (ejemplo DNI)</a></li>
    </ul>
    """

if __name__ == "__main__":
    app.run(port=8888, debug=True)
