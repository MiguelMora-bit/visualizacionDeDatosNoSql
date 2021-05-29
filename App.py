from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient


app = Flask(__name__)

#Metodo para mi pagina principal
@app.route('/')
def Index():
    resultados = materias.find()
    results = []
    for r in resultados:
        valor = (r["_id"], r["nombre"],  r["calificacion"], r["estatus"])
        results.append(valor)
    return render_template("index.html", materias = results)

#Metodo para agregar materia
@app.route('/add_materia', methods=['POST'])
def add_materia():
    if request.method == 'POST':
        nombre = request.form['nombre']
        calificacion = request.form['calificacion']
        estatus = request.form['estatus']
        materias.insert_one({'nombre': nombre, 'calificacion': calificacion, 'estatus': estatus})
        flash("Materia agregada satisfactoriamente")
        return redirect(url_for("Index"))

#Metodo para borrar una materia
@app.route('/delete/<string:id>')
def eliminar(id):
    materias.delete_many({"nombre": id})
    flash("Materia eliminada satisfactoriamente")
    return redirect(url_for('Index'))

#Medtodo para obtener la materia
@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_materia(id):
    print(id)
    r = materias.find_one({"nombre": str(id)})
    valor = (r["_id"], r["nombre"],  r["calificacion"], r["estatus"])
    return render_template('editar.html', materia = valor)

#Metodo para editar la materia
@app.route('/actualizar/<id>', methods=['POST'])
def actualizar(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        calificacion = request.form['calificacion']
        estatus = request.form['estatus']
        materias.update_one({"nombre": id}, {"$set": {"nombre":nombre, "calificacion": calificacion, "estatus" : estatus }})
        return redirect(url_for('Index'))


# Conexion a MongoDB
app.secret_key = "mysecretkey"
MONGO_URI = 'mongodb://localhost'
client = MongoClient(MONGO_URI)

db = client["examen"]
materias = db["materias"]

if __name__ == "__main__":
    app.run(port=3000, debug=True)