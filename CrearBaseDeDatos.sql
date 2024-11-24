-- Crear base de datos
CREATE DATABASE Ecommerce;
GO

-- Usar la base de datos
USE Ecommerce;
GO

-- Tabla: Usuario
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    nombre NVARCHAR(100),
    apellido NVARCHAR(100),
    correo_electronico NVARCHAR(100),
    contrasena NVARCHAR(100),
    telefono NVARCHAR(15),
    fecha_registro DATE,
    tipo_usuario NVARCHAR(50),
    estado BIT
);

-- Tabla: Categoria
CREATE TABLE Categoria (
    idCategoria INT PRIMARY KEY,
    nombre NVARCHAR(100)
);

-- Tabla: Marcas
CREATE TABLE Marcas (
    idMarca INT PRIMARY KEY,
    nombre NVARCHAR(100)
);

-- Tabla: Productos (dependiente de Categoria y Marcas)
CREATE TABLE Productos (
    idProducto INT PRIMARY KEY,
    idCategoria INT,
    idMarca INT,
    precio DECIMAL(10, 2),
    nombre NVARCHAR(100),
    stock INT,
    descripcion NVARCHAR(255),
    popularidad INT,
    imagen NVARCHAR(255),
    FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria),
    FOREIGN KEY (idMarca) REFERENCES Marcas(idMarca)
);

-- Tabla: Carrito (dependiente de Usuario)
CREATE TABLE Carrito (
    idCarrito INT PRIMARY KEY,
    idUsuario INT,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id_usuario)
);

-- Tabla: DetallesCarrito (dependiente de Productos y Carrito)
CREATE TABLE DetallesCarrito (
    idDetalle INT PRIMARY KEY,
    idProducto INT,
    idCarrito INT,
    cantidad INT,
    precio_unitario DECIMAL(10, 2),
    FOREIGN KEY (idProducto) REFERENCES Productos(idProducto),
    FOREIGN KEY (idCarrito) REFERENCES Carrito(idCarrito)
);

-- Tabla: Pedidos (dependiente de Usuario y Carrito)
CREATE TABLE Pedidos (
    idPedido INT PRIMARY KEY,
    idUsuario INT,
    idCarrito INT,
    fecha_pedido DATE,
    estado NVARCHAR(50),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (idCarrito) REFERENCES Carrito(idCarrito)
);

-- Tabla: Reseñas (dependiente de Productos y Usuario)
CREATE TABLE Reseñas (
    id_reseña INT PRIMARY KEY,
    id_producto INT,
    id_usuario INT,
    calificacion INT,
    comentario NVARCHAR(255),
    fecha_reseña DATE,
    FOREIGN KEY (id_producto) REFERENCES Productos(idProducto),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Tabla: Promocion (dependiente de Productos)
CREATE TABLE Promocion (
    id_promocion INT PRIMARY KEY,
    idProducto INT,
    descuento DECIMAL(5, 2),
    fechaInicio DATE,
    fechaFinal DATE,
    FOREIGN KEY (idProducto) REFERENCES Productos(idProducto)
);

-- Tabla: Oferta (dependiente de Productos)
CREATE TABLE Oferta (
    idOferta INT PRIMARY KEY,
    idProducto INT,
    descuento DECIMAL(5, 2),
    fechaInicio DATE,
    fechaFinal DATE,
    FOREIGN KEY (idProducto) REFERENCES Productos(idProducto)
);

-- Visualización de los datos ingresados
SELECT * FROM Usuario;
SELECT * FROM Carrito;
SELECT * FROM DetallesCarrito;
SELECT * FROM Pedidos;
SELECT * FROM Productos;
SELECT * FROM Categoria;
SELECT * FROM Marcas;
SELECT * FROM Reseñas;
SELECT * FROM Promocion;
SELECT * FROM Oferta;
