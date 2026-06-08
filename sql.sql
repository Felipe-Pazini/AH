CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL UNIQUE
);


ALTER TABLE cadastro DROP COLUMN categoria;
ALTER TABLE cadastro ADD categoria_id INT NOT NULL;
ALTER TABLE cadastro ADD FOREIGN KEY (categoria_id) REFERENCES categorias(id);