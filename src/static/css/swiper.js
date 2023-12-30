const swiper = new Swiper('.swiper', {
    slidesPerView: 1,
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },

  autoplay: {
    delay: 4000,
    stopOnLastSlide: false,
    disableOnInteration: false,
  },

});