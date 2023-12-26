
document.addEventListener('DOMContentLoaded', () => { // DOM готов к взаимодейтсвию

	const onScrollHeader = () => { // объявляем основную функцию onScrollHeader

		const header = document.querySelector('.header') // находим header и записываем в константу
 		let prevScroll = window.pageYOffset // узнаем на сколько была прокручена страница ранее
		let currentScroll // на сколько прокручена страница сейчас (пока нет значения)

		window.addEventListener('scroll', () => { // при прокрутке страницы

			currentScroll = window.pageYOffset // узнаем на сколько прокрутили страницу

			const headerHidden = () => header.classList.contains('header_hidden') // узнаем скрыт header или нет

			if (currentScroll > prevScroll && !headerHidden()) { // если прокручиваем страницу вниз и header не скрыт
				header.classList.add('header_hidden') // то скрываем header
			}
			if (currentScroll < prevScroll && headerHidden()) { // если прокручиваем страницу вверх и header скрыт
				header.classList.remove('header_hidden') // то отображаем header
			}

			prevScroll = currentScroll // записываем на сколько прокручена страница на данный момент

		})

	}

	onScrollHeader() // вызываем основную функцию onScrollHeader


	//Модальное окно
	const btnOpen = document.querySelectorAll('.feedback');
	const btnClose = document.querySelector('.close-modal-img');
	const modal = document.querySelector('.modal');
	const form = document.querySelector('.form');
	modal.style.display = 'flex';

	const modalViewHandler = () => {

		modal.classList.toggle('modal--open');
	}

	btnOpen.forEach((item) => {
		item.addEventListener('click', modalViewHandler);
	})

	btnClose.addEventListener('click', (e) => {
		modalViewHandler
	} );

$(function(){
	$('.form').submit(function(e){
		// e.preventDefault();
		// modal.classList.remove('modal--open');
		var data = $(this).serialize();
		$.ajax({
			url: '../php/form.php',
			type: 'POST',
			data: data,
			beforeSend: function(){
				$('#submit').next().text('Отправляю...');
			},
			success: function(res){
				$('.form').find('input').val('');
				$('#submit').next().html(res);
				modal.classList.remove('modal--open');
				// window.location.href = "../php/form.php";
			},
			error: function(){
				alert('Ошибка!');
				modal.classList.remove('modal--open');
			}
		});
	});
});

	modal.addEventListener('click', (e)=> {
		if(!e.target.closest('.modal-wrap')) {
			modal.classList.remove('modal--open');
		}
	})

	const handleReload = () => {
		location.reload();
	}

});


