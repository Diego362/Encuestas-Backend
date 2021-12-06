from flask import Flask, json, jsonify, request
from flask_cors import CORS
import mysql.connector
from flask_jwt_extended import (
    create_access_token,
    JWTManager,
    jwt_required,
    get_jwt_identity,
)

db = mysql.connector.connect(
    host="academia.c1mebdhdxytu.us-east-1.rds.amazonaws.com",
    user="p3",
    password="milEbEANiCOLEwDo",
    database="p3",
    port=3306,
)

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = "nMBsZ&pP@Bc@6VzVAqahzZnC!JrZBHbf"
jwt = JWTManager(app)


@app.route("/")
def index():
    return "Hello world"


@app.post("/usuarios")
def crearUsuario():
    # request  => envia el cliente
    # response => lo que le voy a responder
    datos = request.json

    print(datos)

    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO usuario(nombre, correo, contraseña)
        VALUE(%s, %s, %s)""",
        (
            datos["Nombre"],
            datos["Correo"],
            datos["Contraseña"],
        ),
    )

    db.commit()
    return jsonify({"mensaje": "usuario almacenado correctamente"})


@app.post("/login")
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    cursor = db.cursor(dictionary=True)
    cursor.execute(
        """select * from usuario where correo = %s and contraseña = %s """,
        (
            email,
            password,
        ),
    )

    usuario = cursor.fetchone()

    cursor.close

    if not usuario:
        return jsonify({"message": "Datos de acceso invalidos"})

    token = create_access_token(identity=usuario["id_usuario"])

    return jsonify({"token": token})


@app.get("/usuarios")
@jwt_required()
def listaUsuarios():
    usuario = get_jwt_identity()
    print(usuario)
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from usuario")

    registros = cursor.fetchall()

    return jsonify(registros)


@app.put("/usuarios/<id>")
def actualizarUsuario(id):

    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """UPDATE usuario set nombre=%s, 
        correo=%s, contraseña=%s where id_usuario=%s""",
        (datos["Nombre"], datos["Correo"], datos["Contraseña"], id),
    )

    db.commit()

    return jsonify({"mensaje": "usuario actualizado correctamente"})


@app.delete("/usuarios/<id_usuario>")
def eliminarUsuario(id_usuario):

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM usuario WHERE id_usuario=%s",
        (id_usuario,),
    )

    db.commit()

    return jsonify({"mensaje": "usuario eliminado correctamente"})


@app.get("/usuarios/<id>")
def unUsuario(id):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario where id_usuario=%s", [id])

    usuario = cursor.fetchone()

    return jsonify(usuario)


@app.post("/encuestas")
def crearEncuesta():
    # request  => envia el cliente
    # response => lo que le voy a responder
    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO encuesta(nombre, id_usuario)
        VALUE(%s, %s)""",
        (
            datos["Nombre"],
            datos["id_usuario"],
        ),
    )

    db.commit()

    return jsonify({"mensaje": "encuesta almacenada correctamente"})


@app.get("/encuestas")
@jwt_required()
def listaEncuesta():
    cursor = db.cursor(dictionary=True)
    GetUsuarioLog = get_jwt_identity()

    cursor.execute("select * from encuesta where id_usuario=%s ", (GetUsuarioLog,))

    registros = cursor.fetchall()

    return jsonify(registros)


@app.put("/encuestas/<id_encuesta>")
def actualizarEncuesta(id_encuesta):

    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """UPDATE encuesta set nombre=%s, id_usuario=%s
        where id_encuesta=%s""",
        (
            datos["Nombre"],
            datos["id_usuario"],
            id_encuesta,
        ),
    )

    db.commit()

    return jsonify({"mensaje": "encuesta actualizada correctamente"})


@app.delete("/encuestas/<id_encuesta>")
def eliminarEncuesta(id_encuesta):

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM encuesta where id_encuesta=%s",
        (id_encuesta,),
    )

    db.commit()

    return jsonify({"mensaje": "encuesta eliminada correctamente"})


@app.get("/encuestas/<id>")
def unaEncuesta(id):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM encuesta where id_encuesta=%s", [id])

    encuesta = cursor.fetchall()

    return jsonify(encuesta)


@app.post("/secciones")
def crearSeccion():
    # request  => envia el cliente
    # response => lo que le voy a responder
    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO seccion(nombre, id_encuesta)
        VALUE(%s, %s)""",
        (
            datos["Nombre"],
            datos["id_encuesta"],
        ),
    )

    db.commit()

    return jsonify({"mensaje": "seccion almacenada correctamente"})


@app.get("/secciones")
@jwt_required()
def listaSeccion():
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from seccion")

    registros = cursor.fetchall()

    return jsonify(registros)


@app.put("/secciones/<id_seccion>")
def actualizarSeccion(id_seccion):

    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """UPDATE seccion set nombre=%s, id_encuesta=%s
        where id_seccion=%s""",
        (
            datos["Nombre"],
            datos["id_encuesta"],
            id_seccion,
        ),
    )

    db.commit()

    return jsonify({"mensaje": "seccion actualizada correctamente"})


@app.delete("/secciones/<id_seccion>")
def eliminarSeccion(id_seccion):

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM seccion where id_seccion=%s",
        (id_seccion,),
    )

    db.commit()

    return jsonify({"mensaje": "seccion eliminada correctamente"})


@app.get("/secciones/<id>")
def unaSeccion(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM seccion where id_seccion=%s", [id])

    seccion = cursor.fetchall()

    return jsonify(seccion)


@app.post("/preguntas")
def crearPregunta():
    # request  => envia el cliente
    # response => lo que le voy a responder
    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """INSERT INTO pregunta(nombre, id_seccion, id_tipopregunta)
        VALUE(%s, %s, %s)""",
        (
            datos["Nombre"],
            datos["id_seccion"],
            datos["id_tipopregunta"],
        ),
    )

    db.commit()

    return jsonify({"mensaje": "pregunta almacenada correctamente"})


@app.get("/preguntas")
@jwt_required()
def listaPregunta():
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from pregunta")

    registros = cursor.fetchall()

    return jsonify(registros)


@app.put("/preguntas/<id_pregunta>")
def actualizarPregunta(id_pregunta):

    datos = request.json

    cursor = db.cursor()

    cursor.execute(
        """UPDATE pregunta set nombre=%s, id_seccion=%s , id_tipopregunta=%s
        where id_pregunta=%s""",
        (
            datos["Nombre"],
            datos["id_seccion"],
            datos["id_tipopregunta"],
            id_pregunta,
        ),
    )

    db.commit()

    return jsonify({"mensaje": "pregunta actualizada correctamente"})


@app.delete("/preguntas/<id_pregunta>")
def eliminarPregunta(id_pregunta):

    cursor = db.cursor()
    cursor.execute(
        "DELETE FROM pregunta where id_pregunta=%s",
        (id_pregunta,),
    )

    db.commit()

    return jsonify({"mensaje": "pregunta eliminada correctamente"})


@app.get("/tipopreguntas")
def listaTipoPregunta():
    cursor = db.cursor(dictionary=True)

    cursor.execute("select * from tipo_pregunta")

    registros = cursor.fetchall()

    return jsonify(registros)


@app.get("/preguntas/<id>")
def unaPregunta(id):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM pregunta where id_pregunta=%s", [id])

    pregunta = cursor.fetchall()

    return jsonify(pregunta)


app.run(debug=True)
