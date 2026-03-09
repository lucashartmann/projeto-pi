function setupDados(dados) {
    div = document.getElementById("dados_imovel");
    div_titulo = document.creatElement("div")
    div_titulo.id = "div_titulo";
    titulo = document.createElement("h3");
    titulo.innerText = dados.anuncio.titulo;
    div_titulo.appendChild(titulo);
    descricao = document.createElement("p")
    descricao.innerText = dados.anuncio.descricao;
    div_titulo.appendChild(descricao);
    localizacao = document.createElement("p")
    localizacao.innerText = `${dados.endereco.rua}, ${dados.endereco.numero}, ${dados.endereco.bairro}`;
    div_titulo.appendChild(div_localizacao);
    div.appendChild(div_titulo);

    div_imagens = document.createElement("div");
    if (dados.anuncio.imagens) {
        for (const imagem of dados.anuncio.imagens) {
            const img = document.createElement("img");
            img.src = `data:image/jpeg;base64,${imagem}`;
            div_imagens.appendChild(img);
        }
    }
    div.appendChild(div_imagens);

    //TODO: adicionar filtros, localizacao, valores, etc
}

async function getDadosImovel(id) {
    try {
        const resposta = await fetch(`http://127.0.0.1:8000/imoveis/${id}`);

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