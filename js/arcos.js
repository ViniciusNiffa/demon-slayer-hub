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