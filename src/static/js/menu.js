//Логика выезжающего меню
const burger = document.querySelector('.burger');
const navList = document.querySelector('.header__nav_list-min');
const close = document.querySelector('.close');

burger.addEventListener('click', ()=> {
    navList.classList.add('nav__list-active');
    burger.style.display = 'none';
})

close.addEventListener('click', ()=> {
    navList.classList.remove('nav__list-active');
    burger.style.display = 'flex';
})
