from usuarios_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

PASSWORD_REGEX = re.compile (r'^[a-zA-Z0-9._-]{8}$')


class Usuario:
    def __init__( self, first_name,last_name, email, password, created_at, updated_at ):
        self.first_name = first_name
        self.last_name =last_name
        self.email = email
        self.password = password
        self.created_at= created_at
        self.updated_at = updated_at


    @classmethod
    def agregaUsuario(cls, nuevoUsuario):
        query  = "INSERT INTO usuarios (first_name,last_name, email, password) VALUES (%(first_name)s, %(last_name)s,%(email)s,%(password)s);"
        resultado = connectToMySQL("usuarios_db").query_db(query,nuevoUsuario)
        return resultado

    #@classmethod
    #def seleccionarUsuario(klass, id):
     #   query = "SELECT * FROM usuarios WHERE id = %(id);"
    #  resultado = connectToMySQL ("usuarios_db").query_db (query,id)
    # miobjeto = klass(resultado[0])
        #return resultado

    @classmethod
    def verificaUsuario (cls, usuario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL ("usuarios_db").query_db(query,usuario)
        if len (resultado) > 0:
            usuarioResultado = Usuario (resultado[0]["first_name"], resultado[0]["last_name"], resultado[0]["email"], resultado[0]["password"],resultado[0]["created_at"],resultado[0]["updated_at"])
            return usuarioResultado
        else:
            return None

    


    @classmethod
    def obtenerListaUsuarios(cls):
        query = "SELECT * FROM usuarios;"
        resultado = connectToMySQL ("usuarios_db").query_db(query)
        listaUsuarios = []
        for usuario in resultado:
            listaUsuarios.append(Usuario(usuario["first_name"],usuario["last_name"], usuario["email"],usuario["password"],usuario["created_at"],usuario["updated_at"] ))
        return listaUsuarios


    @staticmethod
    def validate_user( cls,email ):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL("usuarios_db").query_db(query,email)
        print (type (resultado, "SOY UN VALIDADOR"))
        if len(resultado) < 1:
            return False
        return cls(results[0])



    @staticmethod
    def validate_registro(usuario):
        is_valid = True
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL("usuarios_db").query_db(query,usuario)
        if len(resultado) >= 1:
            flash("Email en uso.","registro")
            is_valid=False
        if not EMAIL_REGEX.match(usuario['email']):
            flash("Email invalido","registro")
            is_valid=False
        if len(usuario['first_name']) < 2:
            flash("First name debe contener al menos 2 characters","registro")
            is_valid= False
        if len(usuario['last_name']) < 2:
            flash("Last name debe contener al menos 2 characters","registro")
            is_valid= False
        if len(usuario['password']) > 9:
            flash("Password debe contener máximo 8 caracteres entre letras y numeros","registro")
            is_valid= False
        if usuario['password'] != usuario['confirmPassword']:
            flash("Password no coinciden","registro")
        return is_valid