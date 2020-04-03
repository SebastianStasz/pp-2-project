// Zmiana zdjęć
const current_photo = document.querySelector('.current-photo').querySelector('img');
const choose_photos = document.querySelector('.choose-photos').querySelectorAll('img');

choose_photos.forEach(photo => {
    photo.addEventListener('click', () => {
        current_photo.src = photo.src;
    });
});