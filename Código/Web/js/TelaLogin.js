async function cadastro() {
    const cliente = {
        nome: document.getElementById("nome").value,
        cpf: document.getElementById("cpf").value,
        rg: document.getElementById("rg").value,
        telefone: document.getElementById("telefone").value,
        endereco: document.getElementById("endereco").value,
        email: document.getElementById("email").value
    };

    let res = await fetch("http://127.0.0.1:5000/clientes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(cliente)
    });

    let data = await res.json();
    console.log(data);
    alert(JSON.stringify(data));
}

async function login() {
    const credenciais = {
        email: document.getElementById("email").value,
        senha: document.getElementById("senha").value
    };

    let res = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(credenciais)
    });

    let data = await res.json();
    console.log(data);
    alert(JSON.stringify(data));
}

function mostrarCadastro() {
    document.getElementById("login").style.display = "none";
    document.getElementById("cadastro").style.display = "flex";
}