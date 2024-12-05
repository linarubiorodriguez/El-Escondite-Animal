from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
import enum
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Rol(db.Model):
    id_rol = db.Column(db.String(50), primary_key=True)
    Nombre = db.Column(db.String(50))
    Descripcion = db.Column(db.String(50))

class Usuario(db.Model):
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    telefono = db.Column(db.String(50))
    email = db.Column(db.String(50))
    tipo_doc = db.Column(db.String(50))
    num_documento = db.Column(db.String(50))
    direccion = db.Column(db.String(50))
    contrasena_hash = db.Column(db.String(50))

    id_rol = db.Column(db.String(50), db.ForeignKey('rol.id_rol'))
    rol = db.relationship('Rol', backref='usuarios')

    @property
    def contrasena(self):
        raise AttributeError("La contraseña no es un atributo legible.")
    
    @contrasena.setter
    
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)
    
    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)


class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationship = True
        load_instance = True

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        include_relationship = True
        load_instance = True