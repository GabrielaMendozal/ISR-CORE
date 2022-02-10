from flask import Flask, render_template, request , redirect,session, flash
from usuarios_app import app
from usuarios_app.modelos.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

listaUsuarios = []

#rutas
@app.route ('/', methods = ['GET'])
def despliegaRegistroYLogin():
    return render_template('index.html')


@app.route ('/dashboard', methods =['GET'] )
def despliegaDasboard():
    if "email" in session:
        listaUsuarios = Usuario.obtenerListaUsuarios()
        return render_template ('dashboard.html', usuarios = listaUsuarios)
    else:
        return redirect ("/")


@app.route ('/registroUsuario', methods = ['POST'])
def registrarUsuario():
    if not Usuario.validate_registro(request.form):
        return redirect ("/")

    passwordEncriptado = bcrypt.generate_password_hash(request.form["password"])
    print(request.form, "ÏNFO DE FORMULARIO DE REGISTRO")

    nuevoUsuario = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : passwordEncriptado
    }
    session ["first_name"] = request.form["first_name"]
    session ["last_name"] = request.form["last_name"]
    session ["email"] = request.form ["email"]
    resultado = Usuario.agregaUsuario (nuevoUsuario)
    

    if type (resultado) is int and resultado == 0:
        print (resultado, "HOLA SOY RESULTADO")
        print (type (resultado))
        return redirect ("/dashboard")
    


@app.route ("/login" , methods=["POST"])
def loginUsuario():
    loginEmail = request.form ["loginEmail"]
    loginPassword = request.form ["loginPassword"]

    usuario = {
        "email" : loginEmail,
    }
    
    resultado = Usuario.verificaUsuario(usuario)
    print (resultado,"YO SOY RESULTADO")

    if resultado == None:
        flash("Ingresar email y password", "login")
        return redirect ("/")
    else:
#        print (resultado.password[0])
        if not bcrypt.check_password_hash (resultado.password,loginPassword):
            flash ("El password es incorrecto", "login")
            return redirect ("/")
        else:
            print(session, "MOSTRAR SESION")
            session ["email"]  = resultado.email
            #session ["last_name"] = usuario ["last_name"]
            return redirect ("/dashboard") 
    

    #for usuario in listaUsuarios:
        #if usuario ["email"] == loginEmail and usuario ["password"] == loginPassword:



@app.route ("/logout" , methods = ["GET"])
def logoutUsuario():
    session.clear()
    return redirect ("/")



#@app.route ('/usuario/<id>')
#def unusuario(id):
#    miusuario = Usuario.seleccionarUsuario(id)
#    return render_template('index2.html', miusuario=miusuario)



