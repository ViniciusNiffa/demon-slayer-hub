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