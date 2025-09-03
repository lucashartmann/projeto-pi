from flask import Flask, request, jsonify
from model import Init
from controller import Controller

app = Flask(__name__)

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

    if resultado is True:
        return jsonify({"mensagem": "Cliente cadastrado com sucesso!"}), 201
    else:
        return jsonify({"erro": resultado}), 400

@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    data = request.get_json()
    email = data.get("email")
    senha = data.get("senha")

    resultado = Init.loja.get_cliente_por_email(email)

    if resultado is True:
        return jsonify({"mensagem": "Login bem-sucedido!"}), 200
    else:
        return jsonify({"erro": resultado}), 401

if __name__ == "__main__":
    app.run(debug=True)
