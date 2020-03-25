const navigation = document.querySelector('.side-nav');
const nav_btn = document.querySelector('.nav-btn');
const nav_close_btn = document.querySelector('.nav-close-btn')
let is_open = false;

nav_btn.addEventListener('click', () => {
    navigation.classList.toggle('active');
    document.body.classList.toggle('active');
    is_open = !is_open
});

nav_close_btn.addEventListener('click', () => {
    nav_btn.click();
});

window.onresize = () => {
    if ((window.innerWidth >= 900) && (is_open)) nav_btn.click();
};


// Extend Navigation
navigation.addEventListener('mouseover', () => {
    navigation.classList.add('active');
});

navigation.addEventListener('mouseleave', () => {
    if (window.innerWidth >= 900) {
        navigation.classList.remove('active');
    }
});