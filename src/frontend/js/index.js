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

function imovelPrincipal(dados) {
    while (true) {
        var randomIndex = Math.floor(Math.random() * dados.length);
        var imovel = dados[randomIndex];
        var b64 = imovel.anuncio?.imagens?.[0];
        if (b64) {
            break;
        }
    }

    var banner = document.getElementById("imovelDestaque");
    var img = document.createElement("img");
    img.id = "imgDestaque";
    img.src = `data:image/jpeg;base64,${b64}`;
    img.style.cursor = "pointer";
    img.onclick = () => abrirAnuncio(imovel.id);
    if (!banner) return;
    banner.appendChild(img);
    var titulo = imovel.anuncio.titulo;
    var p_titulo = document.createElement("h2");
    p_titulo.className = "sobrepor";
    p_titulo.textContent = titulo;
    banner.appendChild(p_titulo);
    if (imovel.valor_venda) {
        var p_preco_venda = document.createElement("p");
        p_preco_venda.className = "sobrepor";
        p_preco_venda.textContent = imovel.valor_venda;
        banner.appendChild(p_preco_venda);
    } else if (imovel.valor_aluguel) {
        var p_preco_aluguel = document.createElement("p");
        p_preco_aluguel.className = "sobrepor";
        p_preco_aluguel.textContent = imovel.valor_aluguel;
        banner.appendChild(p_preco_aluguel);
    }
}

function proximoAnuncio() {
    var imagens = document.getElementsByClassName("imgBanner");
    const atual = document.querySelector(".imgBanner:nth-child(1+n)");
    var proximo;
    for (var i = 0; i < imagens.length; i++) {
        if (imagens[i] === atual) {
            proximo = imagens[(i + 1) % imagens.length];
            break;
        }
    }
    if (proximo) {
        proximo.style.display = "block";
    }
    atual.style.display = "none";
}

function anuncioAnterior() {
    var imagens = document.getElementsByClassName("imgBanner");
    const atual = document.querySelector(".imgBanner:nth-child(1+n)");
    var anterior;
    for (var i = 0; i < imagens.length; i++) {
        if (imagens[i] === atual) {
            anterior = imagens[(i - 1 + imagens.length) % imagens.length];
            break;
        }
    }
    if (anterior) {
        anterior.style.display = "block";
    }
    atual.style.display = "none";

}


function bannerImoveis(dados) {
    var banner = document.getElementById("principaisAnuncios");
    for (var i = 0; i < 5; i++) {
        var imovel = dados[i];
        var b64 = imovel.anuncio?.imagens?.[0];
        if (!b64) {
            break;
        }
        var img = document.createElement("img");
        img.className = "imgBanner";
        img.src = `data:image/jpeg;base64,${b64}`;
        img.onclick = () => abrirAnuncio(imovel.id);
        if (!banner) return;
        banner.appendChild(img);
        var titulo = imovel.anuncio.titulo;
        var p_titulo = document.createElement("h2");
        p_titulo.className = "sobrepor";
        p_titulo.textContent = titulo;
        banner.appendChild(p_titulo);
        if (imovel.valor_venda) {
            var p_preco_venda = document.createElement("p");
            p_preco_venda.className = "sobrepor";
            p_preco_venda.textContent = imovel.valor_venda;
            banner.appendChild(p_preco_venda);
        } else if (imovel.valor_aluguel) {
            var p_preco_aluguel = document.createElement("p");
            p_preco_aluguel.className = "sobrepor";
            p_preco_aluguel.textContent = imovel.valor_aluguel;
            banner.appendChild(p_preco_aluguel);
        }
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

        if (imovel.endereco.valor_venda) {
            const p_preco_venda = document.createElement("p");
            const span_preco_venda = document.createElement("span");
            span_preco_venda.textContent = imovel.endereco.valor_venda;
            p_preco_venda.innerText = "Preço:";
            p_preco_venda.appendChild(span_preco_venda);
            div.appendChild(p_preco_venda);
        } else if (imovel.endereco.valor_aluguel) {
            const p_preco_aluguel = document.createElement("p");
            p_preco_aluguel.textContent = imovel.endereco.valor_aluguel;
            div.appendChild(p_preco_aluguel);
        }
        const p_descricao = document.createElement("p");
        p_descricao.textContent = imovel.anuncio.descricao;
        div.appendChild(p_descricao);

        section.appendChild(div);
    }

    imovelPrincipal(dados);
    bannerImoveis(dados);
}

async function abrirAnuncio(imovel_id) {
    sessionStorage.setItem("imovel_id", imovel_id);
    window.location.href = "html/dados-imovel.html";
}
window.addEventListener("DOMContentLoaded", () => {
    carregarAnuncios();
});

