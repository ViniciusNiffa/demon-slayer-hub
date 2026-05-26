function toggleArco(elemento) {
    console.log("Arco clicado:", elemento.id); 
    elemento.classList.toggle('aberto');
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.menu-escondido a').forEach(link => {
        link.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
    const subArcos = document.querySelectorAll('.menu-escondido div, .menu-escondido a, .menu-escondido img');
    
    subArcos.forEach(sub => {
        sub.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    });
});