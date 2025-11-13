/*HABILITAR Y DESHABILITAR ARTICULOS*/

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

UPDATE articulos SET estado = 1 
GO


/*HABILITAR Y DESHABILITAR CLIENTES*/

USE minimarket

ALTER TABLE clientes ADD estado BIT;
GO

ALTER TABLE clientes ADD CONSTRAINT DF_clientes_estado DEFAULT 1 FOR estado;
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


UPDATE clientes
SET estado = 1;
GO


/*HABILITAR Y DESHABILITAR PROVEEDORES*/

USE minimarket

ALTER TABLE proveedores ADD estado BIT;
GO          
            
ALTER TABLE proveedores ADD CONSTRAINT DF_proveedores_estado DEFAULT 1 FOR estado;
GO

CREATE OR ALTER VIEW vista_proveedores_habilitados AS
SELECT * FROM proveedores WHERE estado = 1;
GO


CREATE OR ALTER VIEW vista_proveedores_deshabilitados AS
SELECT * FROM proveedores WHERE estado = 0;
GO


CREATE OR ALTER VIEW vista_proveedores_todos AS
SELECT *,
       CASE 
           WHEN estado = 1 THEN 'Habilitado'
           ELSE 'Deshabilitado'
       END AS estado_proveedor
FROM proveedores;
GO


SELECT * FROM vista_proveedores_todos;
GO


UPDATE proveedores
SET estado = 1;
GO


