from flask import Flask, json, jsonify, request
import mysql.connector

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password ='',
    database = 'sistema',
    port =3306
    
)

app = Flask(__name__)

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
        correo=%s, contraseña=%s where id=%s''',(
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
    cursor.execute('DELETE FROM usuario where id=%s',(id,))


    db.commit()

    return jsonify({

        "mensaje": "usuario eliminado correctamente"
    })

@app.get('/usuarios/<id>')
def unUsuario(id):
    cursor = db.cursor()
    cursor.execute('SELECT * FROM usuario where id=%s',[id])

    usuario = cursor.fetchall()
    
    return jsonify(usuario)
    
app.run(debug=True)