from flask_restful import Resource
from flask import request
from ..modelos import db, Proveedor, ProveedorSchema, Producto, ProductoSchema, \
                      Categoria, CategoriaSchema, Cliente, ClienteSchema, \
                      Compra, CompraSchema, Factura, FacturaSchema, \
                      Usuario, UsuarioSchema, Contraseña, ContraseñaSchema, Empleado, EmpleadoSchema

proveedor_schema = ProveedorSchema()
producto_schema = ProductoSchema()
categoria_schema = CategoriaSchema()
cliente_schema = ClienteSchema()
compra_schema = CompraSchema()
factura_schema = FacturaSchema()
usuario_schema = UsuarioSchema()
contraseña_schema = ContraseñaSchema()
empleado_schema = EmpleadoSchema()

class VistaProveedores(Resource):
    def get(self):
        return [proveedor_schema.dump(proveedor) for proveedor in Proveedor.query.all()]

    def post(self):
        nuevo_proveedor = Proveedor(
            nombre=request.json["nombre"],
            contacto=request.json["contacto"],
            estado=request.json["estado"]
        )
        db.session.add(nuevo_proveedor)
        db.session.commit()
        return proveedor_schema.dump(nuevo_proveedor), 201

    def put(self, id_proveedor):
        proveedor = Proveedor.query.get_or_404(id_proveedor)
        proveedor.nombre = request.json.get("nombre", proveedor.nombre)
        proveedor.contacto = request.json.get("contacto", proveedor.contacto)
        proveedor.estado = request.json.get("estado", proveedor.estado)
        db.session.commit()
        return proveedor_schema.dump(proveedor)

    def delete(self, id_proveedor):
        proveedor = Proveedor.query.get_or_404(id_proveedor)
        db.session.delete(proveedor)
        db.session.commit()
        return '', 204

class VistaProductos(Resource):
    def get(self):
        return [producto_schema.dump(producto) for producto in Producto.query.all()]

    def post(self):
        nuevo_producto = Producto(
            nombre=request.json["nombre"],
            descripcion=request.json["descripcion"],
            estado=request.json["estado"],
            imagen=request.json["imagen"],
            stock=request.json["stock"],
            precio=request.json["precio"]
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto), 201

    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.nombre = request.json.get("nombre", producto.nombre)
        producto.descripcion = request.json.get("descripcion", producto.descripcion)
        producto.estado = request.json.get("estado", producto.estado)
        producto.imagen = request.json.get("imagen", producto.imagen)
        producto.stock = request.json.get("stock", producto.stock)
        producto.precio = request.json.get("precio", producto.precio)
        db.session.commit()
        return producto_schema.dump(producto)

    def delete(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        db.session.delete(producto)
        db.session.commit()
        return '', 204

class VistaCategorias(Resource):
    def get(self):
        return [categoria_schema.dump(categoria) for categoria in Categoria.query.all()]

    def post(self):
        nueva_categoria = Categoria(
            nombre=request.json["nombre"],
            descripcion=request.json["descripcion"]
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria), 201

    def put(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        categoria.nombre = request.json.get("nombre", categoria.nombre)
        categoria.descripcion = request.json.get("descripcion", categoria.descripcion)
        db.session.commit()
        return categoria_schema.dump(categoria)

class VistaClientes(Resource):
    def get(self):
        return [cliente_schema.dump(cliente) for cliente in Cliente.query.all()]

    def post(self):
        nuevo_cliente = Cliente(
            telefono=request.json["telefono"],
            direccion=request.json["direccion"],
            estado=request.json["estado"]
        )
        db.session.add(nuevo_cliente)
        db.session.commit()
        return cliente_schema.dump(nuevo_cliente), 201

    def put(self, id_cliente):
        cliente = Cliente.query.get_or_404(id_cliente)
        cliente.telefono = request.json.get("telefono", cliente.telefono)
        cliente.direccion = request.json.get("direccion", cliente.direccion)
        cliente.estado = request.json.get("estado", cliente.estado)
        db.session.commit()
        return cliente_schema.dump(cliente)

class VistaFacturas(Resource):
    def get(self):
        return [factura_schema.dump(factura) for factura in Factura.query.all()]

    def post(self):
        nueva_factura = Factura(
            fecha=request.json["fecha"],
            monto=request.json["monto"],
            estado=request.json["estado"]
        )
        db.session.add(nueva_factura)
        db.session.commit()
        return factura_schema.dump(nueva_factura), 201

    def put(self, id_factura):
        factura = Factura.query.get_or_404(id_factura)
        factura.fecha = request.json.get("fecha", factura.fecha)
        factura.monto = request.json.get("monto", factura.monto)
        factura.estado = request.json.get("estado", factura.estado)
        db.session.commit()
        return factura_schema.dump(factura)

class VistaCompras(Resource):
    def get(self):
        return [compra_schema.dump(compra) for compra in Compra.query.all()]

    def post(self):
        nueva_compra = Compra(
            fecha=request.json["fecha"],
            total=request.json["total"],
            estado=request.json["estado"]
        )
        db.session.add(nueva_compra)
        db.session.commit()
        return compra_schema.dump(nueva_compra), 201

class VistaUsuarios(Resource):
    def post(self):
        nuevo_usuario = Usuario(
            nombres=request.json["nombres"],
            apellidos=request.json["apellidos"],
            email=request.json["email"]
        )
        nueva_contraseña = Contraseña()
        nueva_contraseña.set_contrasena(request.json["contrasena"])

        nuevo_usuario.contrasena = nueva_contraseña

        db.session.add(nuevo_usuario)
        db.session.add(nueva_contraseña)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario), 201

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.nombres = request.json.get("nombres", usuario.nombres)
        usuario.apellidos = request.json.get("apellidos", usuario.apellidos)
        usuario.email = request.json.get("email", usuario.email)

        nueva_contraseña = request.json.get("contrasena")
        if nueva_contraseña:
            usuario.contrasena.set_contrasena(nueva_contraseña)

        db.session.commit()
        return usuario_schema.dump(usuario)

    def check_contrasena(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        contrasena = request.json["contrasena"]
        if usuario.contrasena.check_contrasena(contrasena):
            return {"mensaje": "Contraseña correcta"}, 200
        return {"mensaje": "Contraseña incorrecta"}, 400

class VistaEmpleados(Resource):
    def get(self):
        return [empleado_schema.dump(empleado) for empleado in Empleado.query.all()]

    def post(self):
        nuevo_empleado = Empleado(
            estado=request.json["estado"],
            cargo=request.json["cargo"],
            salario=request.json["salario"]
        )
        db.session.add(nuevo_empleado)
        db.session.commit()
        return empleado_schema.dump(nuevo_empleado), 201

    def put(self, id_empleado):
        empleado = Empleado.query.get_or_404(id_empleado)
        empleado.estado = request.json.get("estado", empleado.estado)
        empleado.cargo = request.json.get("cargo", empleado.cargo)
        empleado.salario = request.json.get("salario", empleado.salario)
        db.session.commit()
        return empleado_schema.dump(empleado)
