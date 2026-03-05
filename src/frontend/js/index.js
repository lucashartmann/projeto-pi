async function listarImoveis() {
    try {
        const resposta = await fetch("http://127.0.0.1:8000/imoveis/");

        if (!resposta.ok) {
            throw new Error(`HTTP ${resposta.status}`);
        }

        return await resposta.json();
    } catch (erro) {
        console.error("Falha ao conectar com o backend:", erro);
        return null;
    }
}

async function carregarAnuncios() {
    const dados = await listarImoveis(); 
    const section = document.getElementById("anuncios");

    console.log(dados)

    if (!section || !dados) return;

    for (const imovel of dados) {
        const div = document.createElement("div");
        div.className = "anuncio_imovel";
        div.addEventListener("click", () => abrirAnuncio(imovel.id));

        const imagem = document.createElement("img");
        const b64 = imovel.anuncio?.imagens?.[0];
        if (b64) {
            imagem.src = `data:image/jpeg;base64,${b64}`;
        }
        div.appendChild(imagem);
        const p_titulo = document.createElement("h2");
        p_titulo.textContent = imovel.anuncio.p_titulo;
        div.appendChild(p_titulo);

        const p_localizacao = document.createElement("p");
        p_localizacao.textContent = `${imovel.endereco.rua}, ${imovel.endereco.numero}, ${imovel.endereco.bairro}`;
        div.appendChild(p_localizacao);

        if (imovel.endereco.valor_venda){
            const p_preco_venda = document.createElement("p");
            const span_preco_venda = document.createElement("span");
            span_preco_venda.textContent = imovel.endereco.valor_venda;
            p_preco_venda.innerText = "Preço:";
            p_preco_venda.appendChild(span_preco_venda);
            div.appendChild(p_preco_venda);
        }else if (imovel.endereco.valor_aluguel){
            const p_preco_aluguel = document.createElement("p");
            p_preco_aluguel.textContent = imovel.endereco.valor_aluguel;
            div.appendChild(p_preco_aluguel);
        }
        const p_descricao = document.createElement("p");
        p_descricao.textContent = imovel.anuncio.descricao;
        div.appendChild(p_descricao);

        section.appendChild(div);
    }
}

async function abrirAnuncio(imovel_id) {
    return;
}

carregarAnuncios()