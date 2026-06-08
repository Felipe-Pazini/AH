from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///estoque.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Cadastro(db.Model):
    __tablename__ = 'cadastro'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    quantidade = db.Column(db.Integer, nullable=False, default=0)
    categoria = db.Column(db.String(50))
    preco = db.Column(db.Numeric(10, 2), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "quantidade": self.quantidade,
            "categoria": self.categoria,
            "preco": float(self.preco)
        }


@app.route('/produtos', methods=['GET'])
def listar_produtos():
    itens = Cadastro.query.all()
    return jsonify([item.to_dict() for item in itens]), 200


@app.route('/produtos', methods=['POST'])
def criar_produto():
    dados = request.get_json()

    try:
        novo_item = Cadastro(
            nome=dados['nome'].strip(),
            quantidade=dados.get('quantidade', 0),
            categoria=dados.get('categoria', ''),
            preco=dados['preco']
        )

        db.session.add(novo_item)
        db.session.commit()

        return jsonify({
            "mensagem": "Produto cadastrado com sucesso!",
            "produto": novo_item.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400


@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Cadastro.query.get(id)

    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    db.session.delete(produto)
    db.session.commit()

    return jsonify({"mensagem": "Produto deletado com sucesso"}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)