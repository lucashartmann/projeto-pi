function setupDados(dados) {
    var div = document.getElementById("dados_imovel");
    const div_titulo = document.createElement("div");
    const div_pai = document.createElement("div");
    div_pai.id = "div_pai";
    div_titulo.id = "div_titulo";
    const titulo = document.createElement("h3");
    titulo.innerText = dados.anuncio.titulo;
    div_titulo.appendChild(titulo);
    const localizacao = document.createElement("p")
    localizacao.innerText = `${dados.endereco.rua}, ${dados.endereco.numero}, ${dados.endereco.bairro}`;
    div_titulo.appendChild(localizacao);
    div_pai.appendChild(div_titulo);
    div.insertBefore(div_pai, div.firstChild);
    const label_condominio = document.getElementById("condominio");
    const label_iptu = document.getElementById("iptu");
    if (dados.valor_condominio) {
        var p = document.createElement("p");
        p.color = "green";
        p.innerText = `${dados.valor_condominio}`;
        label_condominio.appendChild(p);
    } else {
        if (label_condominio) {
            label_condominio.style.display = "none";
        }
    }

    if (dados.valor_iptu) {
        var p = document.createElement("p");
        p.color = "green";
        p.innerText = `${dados.valor_iptu}`;
        label_iptu.appendChild(p);
    } else {
        if (label_iptu) {
            label_iptu.style.display = "none";
        }
    }

    var ul_imagens = document.createElement("ul");
    ul_imagens.id = "ul_imagens";

    if (dados.anuncio.imagens) {
        var primeira_imagem = dados.anuncio.imagens[0];
        if (primeira_imagem) {
            var img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${primeira_imagem}`;
            div_titulo.appendChild(img);
        }
        for (const imagem of dados.anuncio.imagens) {
            var img = document.createElement("img");
            var li = document.createElement("li");
            img.src = `data:image/jpeg;base64,${imagem}`;
            li.appendChild(img);
            ul_imagens.appendChild(li);
        }
    }
    div_pai.appendChild(ul_imagens);

    const h3_descricao = document.createElement("h3");
    h3_descricao.innerText = "Descrição";
    div_pai.appendChild(h3_descricao);
    const descricao = document.createElement("p")
    descricao.innerText = dados.anuncio.descricao;
    div_pai.appendChild(descricao);

    //TODO: adicionar filtros, localizacao, valores, etc
}

async function getDadosImovel(id) {
    console.log("Buscando dados do imóvel com id:", id);
    try {
        const resposta = await fetch(`http://127.0.0.1:8000/imoveis/${id}/`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        );

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }

}

window.addEventListener("DOMContentLoaded", async () => {
    id = sessionStorage.getItem("imovel_id");
    if (!id) {
        alert("Imóvel não encontrado!");
        window.location.href = "../html/index.html";
        return;
    }
    dados = await getDadosImovel(id);
    if (dados) {
        setupDados(dados);
    }
});