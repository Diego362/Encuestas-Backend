from flask import Flask, json, jsonify, request
from flask_cors import CORS
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password ='',
    database = 'sistema',
    port =3306
    
)

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'Hello world'



@app.post('/usuarios')
def crearUsuario():
    #request  => envia el cliente
    #response => lo que le voy a responder
    datos = request.json
    
    print(datos)

    cursor = db.cursor()

    cursor.execute('''INSERT INTO usuario(nombre, correo, contraseña)
        VALUE(%s, %s, %s)''', (
        datos['Nombre'],
        datos['Correo'],
        datos['Contraseña'],
    ))

    db.commit()
    
    return jsonify({

        "mensaje": "usuario almacenado correctamente"
    })


@app.get('/usuarios')
def listaUsuarios():
    cursor = db.cursor(dictionary=True)

    cursor.execute('select * from usuario')

    registros = cursor.fetchall()

    return jsonify(registros)





@app.put('/usuarios/<id>')
def actualizarUsuario(id):

    datos=request.json

    cursor = db.cursor()


    cursor.execute('''UPDATE usuario set nombre=%s, 
        correo=%s, contraseña=%s where id_usuario=%s''',(
            datos['Nombre'],
            datos['Correo'],
            datos['Contraseña'],
            id
        ))
    
    db.commit()

    return jsonify({

        "mensaje": "usuario actualizado correctamente"
    })  
    
    
@app.delete('/usuarios/<id>')
def eliminarUsuario(id):


    cursor = db.cursor()
    cursor.execute('DELETE FROM usuario where id_usuario=%s',(id))


    db.commit()

    return jsonify({

        "mensaje": "usuario eliminado correctamente"
    })

@app.get('/usuarios/<id>')
def unUsuario(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM usuario where id_usuario=%s',[id])

    usuario = cursor.fetchall()
    
    return jsonify(usuario)

@app.post('/usuarios/<id_usuario>/encuestas')
def crearEncuesta(id_usuario):
    #request  => envia el cliente
    #response => lo que le voy a responder
    datos = request.json
    
    cursor = db.cursor()

    cursor.execute('''INSERT INTO encuesta(nombre, id_usuario)
        VALUE(%s, %s)''', (
        datos['Nombre'],
        id_usuario,
    ))

    db.commit()
    
    return jsonify({

        "mensaje": "encuesta almacenada correctamente"
    })
    
@app.get('/usuarios/encuestas')
def listaEncuesta():
    cursor = db.cursor(dictionary=True)

    cursor.execute('select * from encuesta')

    registros = cursor.fetchall()

    return jsonify(registros)

@app.put('/usuarios/<id_usuario>/encuestas/<id_encuesta>')
def actualizarEncuesta(id_usuario, id_encuesta):

    datos=request.json

    cursor = db.cursor()


    cursor.execute('''UPDATE encuesta set nombre=%s, id_usuario=%s
        where id_encuesta=%s''',(
            datos['Nombre'],
            id_usuario,
            id_encuesta
        ))
    
    db.commit()

    return jsonify({

        "mensaje": "encuesta actualizada correctamente"
    })  

@app.delete('/usuarios/<id_usuario>/encuestas/<id_encuesta>')
def eliminarEncuesta(id_usuario, id_encuesta):


    cursor = db.cursor()
    cursor.execute('DELETE FROM encuesta where id_usuario=%s AND id_encuesta=%s',(id_usuario, id_encuesta))


    db.commit()

    return jsonify({

        "mensaje": "encuesta eliminada correctamente"
    })

@app.post('/encuestas/<id_encuesta>/secciones')
def crearSeccion(id_encuesta):
    #request  => envia el cliente
    #response => lo que le voy a responder
    datos = request.json
    
    cursor = db.cursor()

    cursor.execute('''INSERT INTO seccion(nombre, id_encuesta)
        VALUE(%s, %s)''', (
        datos['Nombre'],
        id_encuesta,
    ))

    db.commit()
    
    return jsonify({

        "mensaje": "seccion almacenada correctamente"
    })

@app.get('/encuestas/secciones')
def listaSeccion():
    cursor = db.cursor(dictionary=True)

    cursor.execute('select * from seccion')

    registros = cursor.fetchall()

    return jsonify(registros)

@app.put('/encuestas/<id_encuesta>/secciones/<id_seccion>')
def actualizarSeccion(id_encuesta, id_seccion):

    datos=request.json

    cursor = db.cursor()


    cursor.execute('''UPDATE seccion set nombre=%s, id_encuesta=%s
        where id_seccion=%s''',(
            datos['Nombre'],
            id_encuesta,
            id_seccion
        ))
    
    db.commit()

    return jsonify({

        "mensaje": "seccion actualizada correctamente"
    })  

@app.delete('/encuestas/<id_encuesta>/secciones/<id_seccion>')
def eliminarSeccion(id_encuesta, id_seccion):


    cursor = db.cursor()
    cursor.execute('DELETE FROM seccion where id_encuesta=%s AND id_seccion=%s',(id_encuesta, id_seccion))


    db.commit()

    return jsonify({

        "mensaje": "seccion eliminada correctamente"
    })

@app.post('/secciones/<id_seccion>/preguntas/<id_tipopregunta>')
def crearPregunta(id_seccion, id_tipopregunta):
    #request  => envia el cliente
    #response => lo que le voy a responder
    datos = request.json
    
    cursor = db.cursor()

    cursor.execute('''INSERT INTO pregunta(nombre, id_seccion, id_tipopregunta)
        VALUE(%s, %s, %s)''', (
        datos['Nombre'],
        id_seccion,
        id_tipopregunta
    ))

    db.commit()
    
    return jsonify({

        "mensaje": "pregunta almacenada correctamente"
    })

@app.get('/secciones/preguntas')
def listaPregunta():
    cursor = db.cursor(dictionary=True)

    cursor.execute('select * from pregunta')

    registros = cursor.fetchall()

    return jsonify(registros)

@app.put('/secciones/<id_seccion>/preguntas/<id_pregunta>')
def actualizarPregunta(id_seccion, id_pregunta):

    datos=request.json

    cursor = db.cursor()


    cursor.execute('''UPDATE pregunta set nombre=%s, id_seccion=%s
        where id_pregunta=%s''',(
            datos['Nombre'],
            id_seccion,
            id_pregunta
        ))
    
    db.commit()

    return jsonify({

        "mensaje": "pregunta actualizada correctamente"
    })  

@app.delete('/secciones/<id_seccion>/preguntas/<id_pregunta>')
def eliminarPregunta(id_seccion, id_pregunta):


    cursor = db.cursor()
    cursor.execute('DELETE FROM pregunta where id_seccion=%s AND id_pregunta=%s',(id_seccion, id_pregunta))


    db.commit()

    return jsonify({

        "mensaje": "pregunta eliminada correctamente"
    })

app.run(debug=True)