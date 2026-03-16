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
    let imovel, b64;
    while (true) {
        var randomIndex = Math.floor(Math.random() * dados.length);
        imovel = dados[randomIndex];
        b64 = imovel.anuncio?.imagens?.[0];
        if (b64) break;
    }
    var banner = document.getElementById("imovelDestaque");
    if (!banner) return;
    let preco = imovel.valor_venda ? `<p class='sobrepor'>${imovel.valor_venda}</p>` : (imovel.valor_aluguel ? `<p class='sobrepor'>${imovel.valor_aluguel}</p>` : "");
    banner.innerHTML = `
        <img id="imgDestaque" src="data:image/jpeg;base64,${b64}" style="cursor:pointer;" onclick="abrirAnuncio(${imovel.id})" />
        <h2 class="sobrepor">${imovel.anuncio.titulo}</h2>
        ${preco}
    `;
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
    var div = document.getElementsByClassName("swiper-wrapper")[0];
    var banner = document.createElement("div")
    banner.className = "swiper-slide";
        var wrapper = document.querySelector(".swiper-wrapper");
        if (!wrapper) return;
        let html = "";
        for (var i = 0; i < 5; i++) {
            var imovel = dados[i];
            if (!imovel) continue;
            var b64 = imovel.anuncio?.imagens?.[0];
            if (!b64) continue;
            let preco = imovel.valor_venda ? `<p class='sobrepor'>${imovel.valor_venda}</p>` : (imovel.valor_aluguel ? `<p class='sobrepor'>${imovel.valor_aluguel}</p>` : "");
            html += `
                <div class="swiper-slide">
                    <img class="imgBanner" src="data:image/jpeg;base64,${b64}" onclick="abrirAnuncio(${imovel.id})" />
                    <h2 class="sobrepor">${imovel.anuncio.titulo}</h2>
                    ${preco}
                </div>
            `;
        }
        wrapper.innerHTML = html;
        if (window.Swiper) {
            if (window.swiperInstance) window.swiperInstance.destroy(true, true);
            window.swiperInstance = new Swiper('.swiper', {
                loop: true,
                pagination: { el: '.swiper-pagination', clickable: true },
                navigation: { nextEl: '.swiper-button-next', prevEl: '.swiper-button-prev' },
                scrollbar: { el: '.swiper-scrollbar' },
            });
        }
}

function nextSlide() {
    if (window.swiperInstance) {
        window.swiperInstance.slideNext();
    }
}

function prevSlide() {
    if (window.swiperInstance) {
        window.swiperInstance.slidePrev();
    }
}

async function carregarAnuncios() {
    const dados = await listarImoveis();
    const section = document.getElementById("anuncios");

    console.log(dados)

    if (!section || !dados) return;

    let html = "";
    for (const imovel of dados) {
        const b64 = imovel.anuncio?.imagens?.[0] || "";
        const preco = imovel.endereco.valor_venda
            ? `<p>Preço: <span>${imovel.endereco.valor_venda}</span></p>`
            : (imovel.endereco.valor_aluguel ? `<p>${imovel.endereco.valor_aluguel}</p>` : "");
        html += `
            <div class="anuncio_imovel" onclick="abrirAnuncio(${imovel.id})">
                <img src="data:image/jpeg;base64,${b64}" />
                <h2>${imovel.anuncio.titulo}</h2>
                <p>${imovel.endereco.rua}, ${imovel.endereco.numero}, ${imovel.endereco.bairro}</p>
                ${preco}
                <p>${imovel.anuncio.descricao}</p>
            </div>
        `;
    }
    section.innerHTML = html;

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