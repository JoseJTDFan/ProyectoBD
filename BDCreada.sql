-- Crear base de datos
CREATE DATABASE Ecommerce;
GO

-- Usar la base de datos
USE Ecommerce;
GO

-- Tabla: Usuario
CREATE TABLE Usuario (
    id_usuario INT PRIMARY KEY,
    nombre NVARCHAR(100) NOT NULL,
    apellido NVARCHAR(100) NOT NULL,
    correo_electronico NVARCHAR(100) UNIQUE NOT NULL,
    contrasena NVARCHAR(100) NOT NULL,
    telefono NVARCHAR(15),
    fecha_registro DATE DEFAULT GETDATE(),
    tipo_usuario NVARCHAR(50) NOT NULL CHECK (tipo_usuario IN ('admin', 'cliente')),
    estado BIT DEFAULT 1 -- Por defecto activo (1)
);

-- Tabla: Categoria
CREATE TABLE Categoria (
    idCategoria INT PRIMARY KEY,
    nombre NVARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: Marcas
CREATE TABLE Marcas (
    idMarca INT PRIMARY KEY,
    nombre NVARCHAR(100) UNIQUE NOT NULL
);

-- Tabla: Productos (dependiente de Categoria y Marcas)
CREATE TABLE Productos (
    idProducto INT PRIMARY KEY,
    idCategoria INT NOT NULL,
    idMarca INT NOT NULL,
    precio DECIMAL(10, 2) NOT NULL CHECK (precio > 0),
    nombre NVARCHAR(100) NOT NULL,
    stock INT NOT NULL CHECK (stock >= 0),
    descripcion NVARCHAR(255),
    popularidad INT DEFAULT 0 CHECK (popularidad >= 0),
    imagen NVARCHAR(255),
    FOREIGN KEY (idCategoria) REFERENCES Categoria(idCategoria),
    FOREIGN KEY (idMarca) REFERENCES Marcas(idMarca)
);

-- Tabla: Carrito (dependiente de Usuario)
CREATE TABLE Carrito (
    idCarrito INT PRIMARY KEY,
    idUsuario INT NOT NULL,
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id_usuario)
);

-- Tabla: DetallesCarrito (dependiente de Productos y Carrito)
CREATE TABLE DetallesCarrito (
    idDetalle INT PRIMARY KEY,
    idProducto INT NOT NULL,
    idCarrito INT NOT NULL,
    cantidad INT NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10, 2) NOT NULL CHECK (precio_unitario > 0),
    FOREIGN KEY (idProducto) REFERENCES Productos(idProducto),
    FOREIGN KEY (idCarrito) REFERENCES Carrito(idCarrito)
);

-- Tabla: Pedidos (dependiente de Usuario y Carrito)
CREATE TABLE Pedidos (
    idPedido INT PRIMARY KEY,
    idUsuario INT NOT NULL,
    idCarrito INT NOT NULL,
    fecha_pedido DATE DEFAULT GETDATE(),
    estado NVARCHAR(50) NOT NULL CHECK (estado IN ('pendiente', 'enviado', 'completado', 'cancelado')),
    FOREIGN KEY (idUsuario) REFERENCES Usuario(id_usuario),
    FOREIGN KEY (idCarrito) REFERENCES Carrito(idCarrito)
);

-- Tabla: Reseñas (dependiente de Productos y Usuario)
CREATE TABLE Reseñas (
    id_reseña INT PRIMARY KEY,
    id_producto INT NOT NULL,
    id_usuario INT NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion BETWEEN 1 AND 5),
    comentario NVARCHAR(255),
    fecha_reseña DATE DEFAULT GETDATE(),
    FOREIGN KEY (id_producto) REFERENCES Productos(idProducto),
    FOREIGN KEY (id_usuario) REFERENCES Usuario(id_usuario)
);

-- Tabla: Promocion (dependiente de Productos)
CREATE TABLE Promocion (
    id_promocion INT PRIMARY KEY,
    idProducto INT NOT NULL,
    descuento DECIMAL(5, 2) NOT NULL CHECK (descuento > 0 AND descuento <= 100),
    fechaInicio DATE NOT NULL,
    fechaFinal DATE NOT NULL,
    FOREIGN KEY (idProducto) REFERENCES Productos(idProducto)
);

-- Tabla: Oferta (dependiente de Productos)
CREATE TABLE Oferta (
    idOferta INT PRIMARY KEY,
    idProducto INT NOT NULL,
    descuento DECIMAL(5, 2) NOT NULL CHECK (descuento > 0 AND descuento <= 100),
    fechaInicio DATE NOT NULL,
    fechaFinal DATE NOT NULL,
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
