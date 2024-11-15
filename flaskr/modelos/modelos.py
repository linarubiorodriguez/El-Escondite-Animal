from marshmallow import fields
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()

class Estado(enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombres = db.Column(db.String(50))
    apellidos = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    empleados = db.relationship('Empleado', backref='usuario', lazy=True)
    clientes = db.relationship('Cliente', backref='usuario', lazy=True)
    contrasena = db.relationship('Contraseña', uselist=False, backref='usuario')

class Contraseña(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contrasena_hash = db.Column(db.String(128))
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    def set_contrasena(self, contrasena):
        self.contrasena_hash = generate_password_hash(contrasena)

    def check_contrasena(self, contrasena):
        return check_password_hash(self.contrasena_hash, contrasena)
    
class Empleado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cargo = db.Column(db.String(50))
    salario = db.Column(db.Float)
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(15))
    direccion = db.Column(db.String(100))
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    compras = db.relationship('Compra', backref='cliente', lazy=True)

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    contacto = db.Column(db.String(50))
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    descripcion = db.Column(db.String(200))
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(200))
    imagen = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    precio = db.Column(db.Float)
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    total = db.Column(db.Float)
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)

class Factura(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.Date)
    monto = db.Column(db.Float)
    estado = db.Column(db.Enum(Estado), default=Estado.ACTIVO)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
    contrasena = fields.Method("set_contrasena", deserialize="load_contrasena")

    def set_contrasena(self, contrasena):
        usuario = self.context.get("usuario")
        if usuario:
            usuario.contrasena.set_contrasena(contrasena)

class ContraseñaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Contraseña
        exclude = ("contrasena_hash",)


class EmpleadoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Empleado
        include_relationships = True
        load_instance = True

class ClienteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Cliente
        include_relationships = True
        load_instance = True

class ProveedorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Proveedor
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        load_instance = True

class CompraSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Compra
        include_relationships = True
        load_instance = True

class FacturaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Factura
        include_relationships = True
        load_instance = True
