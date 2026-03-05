var displays = {};

function openTab(evt, tabId) {
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }
    var tablinks = document.getElementsByClassName("tablinks");
    for (var i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }
    if (displays[tabId] === "none") {
        displays[tabId] = "block";
    }
    document.getElementById(tabId).style.display = displays[tabId];
}

window.addEventListener("DOMContentLoaded", () => {
    document.getElementById("tab_imovel")?.classList.add("active");
    var tabcontent = document.getElementsByClassName("tabcontent");
    for (var i = 0; i < tabcontent.length; i++) {
        displays[tabcontent[i].id] = tabcontent[i].style.display;
    }
});