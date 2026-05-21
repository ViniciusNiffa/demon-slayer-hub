function toggleArco(elemento) {
    // Adiciona ou remove a classe 'aberto'
    elemento.classList.toggle('aberto');
}

// Impede que clicar nos links feche o menu antes de navegar
document.querySelectorAll('.menu-escondido a').forEach(link => {
    link.addEventListener('click', (e) => {
        e.stopPropagation();
    });
});
document.addEventListener('DOMContentLoaded', () => {
    // Seleciona todos os divs de sub-arcos
    const subArcos = document.querySelectorAll('.menu-escondido div[id^="sub"]');
    
    subArcos.forEach(sub => {
        sub.addEventListener('click', (e) => {
            // Isso impede que o clique no sub-arco chegue no #arco1 
            // e feche o menu acidentalmente
            e.stopPropagation();
        });
    });
});