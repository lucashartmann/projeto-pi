async function deslogar() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/deslogar/", {
            method: "POST"
        });

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        nav = document.getElementsByTagName("nav");
        ul = nav[0].getElementsByTagName("ul");
        for (li of ul[0].children) {
            a = li.getElementsByTagName("a")[0];
            if (a.innerText == "Sair") {
                a.innerText = "Logar";
                a.removeEventListener("click", deslogar);
                a.href = "html/login.html";
            }
        }

        console.log("Deslogado com sucesso!");
        window.location.href = "../index.html";
        return;

    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }
}

async function carregarUser() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/usuario/");

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        } else {
            const dados = await resposta.json();
            usuario = dados.tipo;
            return usuario;
        }

    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }
}

function carregarTabs(usuario) {
    nav = document.getElementsByTagName("nav");
    ul = nav[0].getElementsByTagName("ul");

    switch (usuario) {
        case 'ADMIN':
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Atendimento";
            a.id = "tab_atendimento";
            a.href = "html/atendimento.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Imoveis";
            a.href = "html/cadastro-imovel.html";
            a.id = "tab_cadastro_imovel";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Pessoas";
            a.href = "html/cadastro-pessoa.html";
            a.id = "tab_cadastro_pessoa";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Estoque";
            a.href = "html/estoque.html";
            a.id = "tab_estoque";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Dados Cliente";
            a.href = "html/dados-cliente.html";
            a.id = "tab_dados_cliente";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Estoque Cliente";
            a.href = "html/estoque-cliente.html";
            a.id = "tab_comprar";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Dados da imobiliaria";
            a.href = "html/dados-imobiliaria.html";
            a.id = "tab_dados_imobiliaria";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Venda/Aluguel";
            a.href = "html/cadastro-venda-aluguel.html";
            a.id = "tab_cadastro_venda_aluguel";
            li.appendChild(a);
            ul[0].appendChild(li);
            break;
        case "CORRETOR":
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Atendimento";
            a.href = "html/atendimento.html";
            a.id = "tab_atendimento";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Imoveis";
            a.href = "html/cadastro-imovel.html";
            a.id = "tab_cadastro_imovel";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Pessoas";
            a.href = "html/cadastro-pessoa.html";
            a.id = "tab_cadastro_pessoa";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Estoque";
            a.href = "html/estoque.html";
            a.id = "tab_estoque";
            li.appendChild(a);
            ul[0].appendChild(li);
            break;
        case "GERENTE":
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Dados da imobiliaria";
            a.id = "tab_dados_imobiliaria";
            a.href = "html/dados-imobiliaria.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Pessoas";
            a.id = "tab_cadastro_pessoa";
            a.href = "html/cadastro-pessoa.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Estoque";
            a.href = "html/estoque.html";
            a.id = "tab_estoque";
            li.appendChild(a);
            ul[0].appendChild(li);
            break;
        case "CAPTADOR":
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Imoveis";
            a.id = "tab_cadastro_imovel";
            a.href = "html/cadastro-imovel.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Cadastro de Pessoas";
            a.id = "tab_cadastro_pessoa";
            a.href = "html/cadastro-pessoa.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Estoque";
            a.href = "html/estoque.html";
            a.id = "tab_estoque";
            li.appendChild(a);
            ul[0].appendChild(li);
            break;
        case "CLIENTE":
            var li = document.createElement("li");
            var a = document.createElement("a");
            a.innerText = "Dados Cliente";
            a.id = "tab_dados_cliente";
            a.href = "html/dados-cliente.html";
            li.appendChild(a);
            ul[0].appendChild(li);
            break;
    }

    for (li of ul[0].children) {
        a = li.getElementsByTagName("a")[0];
        if (a.innerText === "Login") {
            a.innerText = "Sair";
            a.addEventListener("click", deslogar);
            a.href = "#";
        }
    }
};

async function setup() {
    usuario = await carregarUser();

    if (usuario) {
        carregarTabs(usuario);
    }
}

window.addEventListener("DOMContentLoaded", () => {
    setup();
});

