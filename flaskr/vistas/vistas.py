from flask_restful import Resource
from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Rol, RolSchema
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import jwt_required, create_access_token

usuario_schema = UsuarioSchema()
album_schema = RolSchema()

class VistaLogIn(Resource):
    def post(self):
        u_email = request.json["email"]
        u_contrasena = request.json["contrasena"]
        
        email = Usuario.query.filter_by(email=u_email).first()
        if email and email.verificar_contrasena(u_contrasena):
            return {'mensaje': 'Inicio de sesión exitoso'}, 200
        else:
            return {'mensaje': 'Email o contraseña incorrectos'}, 401

class VistaSignIn(Resource):
    def post(self):
        nuevo_usuario = Usuario(
            nombres=request.json["nombre"],
            apellidos=request.json.get("apellidos"),
            telefono=request.json.get("telefono"),
            email=request.json.get("email"),
            tipo_doc=request.json.get("tipo_doc"),
            num_documento=request.json.get("num_documento"),
            direccion=request.json.get("direccion"),
            contrasena=request.json.get("contrasena")
        )
        nuevo_usuario.id_rol = 'cliente'
        nuevo_usuario.contrasena = request.json["contrasena"]
        token_de_acceso = create_access_token(identity=request.json['nombre'])
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        
        return {'mensaje': 'Usuario creado exitosamente', 'token_de_acceso': token_de_acceso}
