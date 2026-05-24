function closeModal() {
    const modal = document.getElementById('flashModal');
    if (modal) {
        modal.style.display = 'none';
    }
}
window.onclick = function(event) {
    let modal = document.getElementById('flashModal');
    if (modal && event.target == modal) closeModal();
}