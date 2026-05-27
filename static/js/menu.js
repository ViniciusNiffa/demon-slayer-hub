function myFunction(){
var x = document.getElementById("myTopnav");
if(x.className === "topnav"){
    x.className += " responsive";
}else{
    x.className = "topnav";
}
}

function toggleProfileMenu(event) {
    event.stopPropagation();
    const dropdown = document.getElementById("profileDropdown");
    dropdown.style.display = (dropdown.style.display === "flex") ? "none" : "flex";
}

function togglePasswordVisibility() {
    const passwordInput = document.getElementById("senha");
    const toggleIcon = document.getElementById("togglePassword");

    if (passwordInput && toggleIcon) {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            toggleIcon.src = "/static/uploads/login/ocultar.png";
        } else {
            passwordInput.type = "password";
            toggleIcon.src = "/static/uploads/login/visualizar.png";
        }
    }
}

window.addEventListener('click', function(e) {
    const dropdown = document.getElementById("profileDropdown");
    if (dropdown && !dropdown.contains(e.target)) {
        dropdown.style.display = "none";
    }
});

function confirmarRemocao() {
    return confirm("Tem certeza que deseja remover sua foto de perfil e voltar para a imagem padrão?");
}

// Lógica para abrir imagens de fanarts em tela cheia
document.addEventListener('DOMContentLoaded', function() {
    // Cria o modal dinamicamente se ele não existir
    let modal = document.getElementById('imageFullscreenModal');
    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'imageFullscreenModal';
        modal.className = 'image-modal';
        modal.innerHTML = '<img class="image-modal-content" id="fullscreenImg" alt="Fanart ampliada">';
        document.body.appendChild(modal);

        // Ao clicar no modal (fundo ou imagem), voltamos no histórico para fechar
        modal.addEventListener('click', function() {
            if (history.state && history.state.fullscreen) {
                history.back();
            } else {
                fecharModalImagem();
            }
        });
    }

    // Função isolada para esconder o modal
    function fecharModalImagem() {
        const modalImg = document.getElementById('imageFullscreenModal');
        if (modalImg) {
            modalImg.style.display = 'none';
            document.body.style.overflow = 'auto';
        }
    }

    // Escuta o botão "Voltar" do navegador
    window.addEventListener('popstate', function(event) {
        fecharModalImagem();
    });

    // Event listener global para capturar cliques em imagens de fanarts
    document.addEventListener('click', function(e) {
        const target = e.target;
        if (target.tagName === 'IMG' && (target.classList.contains('fanart-img') || target.closest('#outrasF') || target.closest('#fanartMes'))) {
            e.preventDefault(); // Impede que o navegador siga o link ou recarregue a página
            const modalImg = document.getElementById('fullscreenImg');
            modalImg.src = target.src;
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Trava o scroll da página
            
            // Adiciona um estado no histórico para que o "Voltar" funcione
            history.pushState({ fullscreen: true }, "");
        }
    });
});