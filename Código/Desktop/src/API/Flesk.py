from flask import Flask, request, jsonify
from model import Init
from controller import Controller
from model import Cliente
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/clientes", methods=["POST"])
def cadastrar_cliente():
    data = request.get_json()

    dados = (
        data["nome"],
        data["cpf"],
        data["rg"],
        data["telefone"],
        data["endereco"],
        data["email"]
    )

    resultado = Controller.cadastrar_cliente(dados)

    if resultado:
        Init.cliente_atual = Cliente.Cliente(dados[0], dados[1], dados[2],
                                             dados[3], dados[4], dados[5])

    return jsonify({"mensagem": resultado}), 201


@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    resultado = Init.loja.get_cliente_por_email(email)

    if resultado:
        Init.cliente_atual = resultado
        return jsonify({"mensagem": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"erro": "Email ou senha inválidos."}), 401


if __name__ == "__main__":
    app.run(debug=True)
