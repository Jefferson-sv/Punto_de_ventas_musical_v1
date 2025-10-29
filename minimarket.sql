USE [master]
GO
/****** Object:  Database [minimarket]    Script Date: 9/10/2025 20:05:11 ******/
CREATE DATABASE [minimarket]
 CONTAINMENT = NONE
 ON  PRIMARY 
( NAME = N'minimarket', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\minimarket.mdf' , SIZE = 8192KB , MAXSIZE = UNLIMITED, FILEGROWTH = 65536KB )
 LOG ON 
( NAME = N'minimarket_log', FILENAME = N'C:\Program Files\Microsoft SQL Server\MSSQL16.MSSQLSERVER\MSSQL\DATA\minimarket_log.ldf' , SIZE = 8192KB , MAXSIZE = 2048GB , FILEGROWTH = 65536KB )
 WITH CATALOG_COLLATION = DATABASE_DEFAULT, LEDGER = OFF
GO
ALTER DATABASE [minimarket] SET COMPATIBILITY_LEVEL = 160
GO
IF (1 = FULLTEXTSERVICEPROPERTY('IsFullTextInstalled'))
begin
EXEC [minimarket].[dbo].[sp_fulltext_database] @action = 'enable'
end
GO
ALTER DATABASE [minimarket] SET ANSI_NULL_DEFAULT OFF 
GO
ALTER DATABASE [minimarket] SET ANSI_NULLS OFF 
GO
ALTER DATABASE [minimarket] SET ANSI_PADDING OFF 
GO
ALTER DATABASE [minimarket] SET ANSI_WARNINGS OFF 
GO
ALTER DATABASE [minimarket] SET ARITHABORT OFF 
GO
ALTER DATABASE [minimarket] SET AUTO_CLOSE OFF 
GO
ALTER DATABASE [minimarket] SET AUTO_SHRINK OFF 
GO
ALTER DATABASE [minimarket] SET AUTO_UPDATE_STATISTICS ON 
GO
ALTER DATABASE [minimarket] SET CURSOR_CLOSE_ON_COMMIT OFF 
GO
ALTER DATABASE [minimarket] SET CURSOR_DEFAULT  GLOBAL 
GO
ALTER DATABASE [minimarket] SET CONCAT_NULL_YIELDS_NULL OFF 
GO
ALTER DATABASE [minimarket] SET NUMERIC_ROUNDABORT OFF 
GO
ALTER DATABASE [minimarket] SET QUOTED_IDENTIFIER OFF 
GO
ALTER DATABASE [minimarket] SET RECURSIVE_TRIGGERS OFF 
GO
ALTER DATABASE [minimarket] SET  DISABLE_BROKER 
GO
ALTER DATABASE [minimarket] SET AUTO_UPDATE_STATISTICS_ASYNC OFF 
GO
ALTER DATABASE [minimarket] SET DATE_CORRELATION_OPTIMIZATION OFF 
GO
ALTER DATABASE [minimarket] SET TRUSTWORTHY OFF 
GO
ALTER DATABASE [minimarket] SET ALLOW_SNAPSHOT_ISOLATION OFF 
GO
ALTER DATABASE [minimarket] SET PARAMETERIZATION SIMPLE 
GO
ALTER DATABASE [minimarket] SET READ_COMMITTED_SNAPSHOT OFF 
GO
ALTER DATABASE [minimarket] SET HONOR_BROKER_PRIORITY OFF 
GO
ALTER DATABASE [minimarket] SET RECOVERY FULL 
GO
ALTER DATABASE [minimarket] SET  MULTI_USER 
GO
ALTER DATABASE [minimarket] SET PAGE_VERIFY CHECKSUM  
GO
ALTER DATABASE [minimarket] SET DB_CHAINING OFF 
GO
ALTER DATABASE [minimarket] SET FILESTREAM( NON_TRANSACTED_ACCESS = OFF ) 
GO
ALTER DATABASE [minimarket] SET TARGET_RECOVERY_TIME = 60 SECONDS 
GO
ALTER DATABASE [minimarket] SET DELAYED_DURABILITY = DISABLED 
GO
ALTER DATABASE [minimarket] SET ACCELERATED_DATABASE_RECOVERY = OFF  
GO
EXEC sys.sp_db_vardecimal_storage_format N'minimarket', N'ON'
GO
ALTER DATABASE [minimarket] SET QUERY_STORE = ON
GO
ALTER DATABASE [minimarket] SET QUERY_STORE (OPERATION_MODE = READ_WRITE, CLEANUP_POLICY = (STALE_QUERY_THRESHOLD_DAYS = 30), DATA_FLUSH_INTERVAL_SECONDS = 900, INTERVAL_LENGTH_MINUTES = 60, MAX_STORAGE_SIZE_MB = 1000, QUERY_CAPTURE_MODE = AUTO, SIZE_BASED_CLEANUP_MODE = AUTO, MAX_PLANS_PER_QUERY = 200, WAIT_STATS_CAPTURE_MODE = ON)
GO
USE [minimarket]
GO
/****** Object:  Table [dbo].[articulos]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[articulos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[articulo] [nvarchar](100) NULL,
	[precio] [decimal](10, 2) NULL,
	[costo] [decimal](10, 2) NULL,
	[stock] [int] NULL,
	[estado] [nvarchar](50) NULL,
	[image_path] [nvarchar](255) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[clientes]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[clientes](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NULL,
	[dui] [nvarchar](20) NULL,
	[celular] [nvarchar](15) NULL,
	[direccion] [nvarchar](255) NULL,
	[correo] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[pedidos]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[pedidos](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[numero_pedido] [int] NOT NULL,
	[proveedor] [nvarchar](100) NOT NULL,
	[producto] [nvarchar](100) NOT NULL,
	[cantidad] [int] NOT NULL,
	[fecha] [date] NOT NULL,
	[hora] [time](7) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[proveedores]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[proveedores](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NOT NULL,
	[identificacion] [nvarchar](20) NOT NULL,
	[celular] [nvarchar](15) NOT NULL,
	[direccion] [nvarchar](255) NOT NULL,
	[correo] [nvarchar](100) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[usuarios]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[usuarios](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[username] [nvarchar](50) NOT NULL,
	[password] [nvarchar](255) NOT NULL,
PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[ventas]    Script Date: 9/10/2025 20:05:11 ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[ventas](
	[factura] [int] IDENTITY(1,1) NOT NULL,
	[cliente] [nvarchar](100) NULL,
	[articulo] [nvarchar](100) NULL,
	[precio] [decimal](10, 2) NULL,
	[cantidad] [int] NULL,
	[total] [decimal](10, 2) NULL,
	[fecha] [date] NULL,
	[hora] [time](7) NULL,
	[costo] [decimal](10, 2) NULL,
PRIMARY KEY CLUSTERED 
(
	[factura] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
USE [master]
GO
ALTER DATABASE [minimarket] SET  READ_WRITE 
GO
/*HABILITAR Y DESHABILITAR ARTICULOS*/
ALTER TABLE articulos
DROP CONSTRAINT DF_articulos_estado;
GO


ALTER TABLE articulos
ADD estado_bit BIT;
GO

UPDATE articulos
SET estado_bit = CASE 
                    WHEN estado = 'Habilitado' THEN 1
                    ELSE 0
                 END;
GO


ALTER TABLE articulos
DROP COLUMN estado;
GO


EXEC sp_rename 'articulos.estado_bit', 'estado', 'COLUMN';
GO


ALTER TABLE articulos
ADD CONSTRAINT DF_articulos_estado DEFAULT 1 FOR estado;
GO

SELECT * FROM articulos;

UPDATE articulos SET estado = 0 WHERE id = 5; -- Deshabilitar
UPDATE articulos SET estado = 1 WHERE id = 1; -- Habilitar

CREATE OR ALTER VIEW vista_articulos_habilitados AS
SELECT *
FROM articulos
WHERE estado = 1;
GO

CREATE OR ALTER VIEW vista_articulos_deshabilitados AS
SELECT *
FROM articulos
WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_articulos_todos AS
SELECT *,
       CASE 
           WHEN estado = 1 THEN 'Habilitado'
           ELSE 'Deshabilitado'
       END AS estado_articulo
FROM articulos;
GO

SELECT * FROM vista_articulos_todos;
GO

/*HABILITAR Y DESHABILITAR CLIENTES*/


ALTER TABLE clientes DROP CONSTRAINT DF__clientes__estado__37C5420D;
GO


ALTER TABLE clientes ADD estado_bit BIT;
GO

UPDATE clientes
SET estado_bit = CASE 
                    WHEN estado = 'Habilitado' THEN 1
                    ELSE 0
                 END;
GO


ALTER TABLE clientes DROP COLUMN estado;
GO


EXEC sp_rename 'clientes.estado_bit', 'estado', 'COLUMN';
GO


ALTER TABLE clientes ADD CONSTRAINT DF_clientes_estado DEFAULT 1 FOR estado;
GO


UPDATE clientes SET estado = 0 WHERE id = 2;
GO
UPDATE clientes SET estado = 1 WHERE id = 1;
GO


SELECT * FROM clientes WHERE estado = 1;
GO
SELECT * FROM clientes WHERE estado = 0;
GO


CREATE OR ALTER VIEW vista_clientes_habilitados AS
SELECT * FROM clientes WHERE estado = 1;
GO

CREATE OR ALTER VIEW vista_clientes_deshabilitados AS
SELECT * FROM clientes WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_clientes_todos AS
SELECT *,
       CASE 
           WHEN estado = 1 THEN 'Habilitado'
           ELSE 'Deshabilitado'
       END AS estado_cliente
FROM clientes;
GO

SELECT * FROM vista_clientes_todos;
GO




INSERT INTO clientes (nombre, dui, celular, direccion, correo)
VALUES ('Fernando Moisés Alvarado', '01234567-8', '7890-1234', 'Col. Escalón, San Salvador', 'fernando@example.com');
GO
INSERT INTO articulos (articulo, precio, costo, stock, image_path)
VALUES ('RTX 5070 Ti', 898.90, 750.00, 5, 'imagenes/rtx5070ti.jpg');
GO
INSERT INTO articulos (articulo, precio, costo, stock, image_path)
VALUES ('RTX 5060 Super', 599.90, 500.00, 8, 'imagenes/rtx5060super.jpg');
GO
INSERT INTO clientes (nombre, dui, celular, direccion, correo)
VALUES ('Ana López', '98765432-1', '7012-3456', 'Col. San Benito, San Salvador', 'ana.lopez@example.com');
GO
/*HABILITAR Y DESHABILITAR PROVEEDORES*/
ALTER TABLE proveedores ADD estado_bit BIT;
GO

UPDATE proveedores
SET estado_bit = CASE WHEN estado = 'Habilitado' THEN 1 ELSE 0 END;
GO

ALTER TABLE proveedores DROP COLUMN estado;
GO

EXEC sp_rename 'proveedores.estado_bit', 'estado', 'COLUMN';
GO

ALTER TABLE proveedores ADD CONSTRAINT DF_proveedores_estado DEFAULT 1 FOR estado;
GO

UPDATE proveedores SET estado = 0 WHERE id = 1;
GO

UPDATE proveedores SET estado = 1 WHERE id = 4;
GO

SELECT * FROM proveedores WHERE estado = 1;
GO

SELECT * FROM proveedores WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_proveedores_habilitados AS
SELECT * FROM proveedores WHERE estado = 1;
GO

CREATE OR ALTER VIEW vista_proveedores_deshabilitados AS
SELECT * FROM proveedores WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_proveedores_todos AS
SELECT *,
       CASE WHEN estado = 1 THEN 'Habilitado' ELSE 'Deshabilitado' END AS estado_proveedor
FROM proveedores;
GO

SELECT * FROM vista_proveedores_todos;
GO




INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo)
VALUES ('Tech Solutions S.A.', '12345678-9', '7012-3456', 'Col. Escalón, San Salvador', 'contacto@techsolutions.com');
GO

INSERT INTO proveedores (nombre, identificacion, celular, direccion, correo)
VALUES ('Distribuidora López', '98765432-1', '7890-1234', 'Col. San Benito, San Salvador', 'ventas@distribuidoralopez.com');
GO

/*HABILITAR Y DESHABILITAR USUARIOS*/
ALTER TABLE usuarios ADD estado_bit BIT;
GO

UPDATE usuarios
SET estado_bit = CASE WHEN estado = 'Habilitado' THEN 1 ELSE 0 END;
GO

ALTER TABLE usuarios DROP COLUMN estado;
GO

ALTER TABLE usuarios DROP CONSTRAINT DF__usuarios__estado__4242D080;
GO

EXEC sp_rename 'usuarios.estado_bit', 'estado', 'COLUMN';
GO

ALTER TABLE usuarios ADD CONSTRAINT DF_usuarios_estado DEFAULT 1 FOR estado;
GO

UPDATE usuarios SET estado = 0 WHERE id = 4;
GO
UPDATE usuarios SET estado = 1 WHERE id = 3;
GO

SELECT * FROM usuarios WHERE estado = 1;
GO
SELECT * FROM usuarios WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_usuarios_habilitados AS
SELECT * FROM usuarios WHERE estado = 1;
GO

CREATE OR ALTER VIEW vista_usuarios_deshabilitados AS
SELECT * FROM usuarios WHERE estado = 0;
GO

CREATE OR ALTER VIEW vista_usuarios_todos AS
SELECT *,
       CASE WHEN estado = 1 THEN 'Habilitado' ELSE 'Deshabilitado' END AS estado_usuario
FROM usuarios;
GO

SELECT * FROM vista_usuarios_todos;
GO

INSERT INTO usuarios (username, password)
VALUES ('admin', 'admin123');
GO

INSERT INTO usuarios (username, password)
VALUES ('usuario1', 'usuario123');
GO
ALTER TABLE articulos ALTER COLUMN estado BIT NOT NULL;
GO
ALTER TABLE clientes ALTER COLUMN estado BIT NOT NULL;
GO
ALTER TABLE proveedores ALTER COLUMN estado BIT NOT NULL;
GO
ALTER TABLE usuarios ALTER COLUMN estado BIT NOT NULL;
GO

