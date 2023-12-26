const swiper = new Swiper('.swiper', {
    slidesPerView: 4,
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

  autoplay: {
    delay: 3000,
    stopOnLastSlide: false,
    disableOnInteration: false,
  },

});