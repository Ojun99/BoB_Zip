$(function() {
    let header = $('header');
    let depth1 = $('.depth1');

    $('header').on('mouseover', function() {
        $(this).addClass('on'); 
      /*   $(this).css('background', '#f6f285')   */
        $(this).css('transition', 'all 0.7s')  
    })

    $('header').on('mouseleave', function() {
        $(this).removeClass('on'); 
        $(this).css('background', 'none')  
        $(this).css('transition', 'all 0.5s')  
    })

    


    $('.subYes').on('mouseover', function() {
        $(this).children('.depth1').stop().fadeIn(700)
        $('.gnb').perents('.inner').siblings('.depthAboutBg').stop().fadeIn(500)
        $(this).siblings('li').removeClass('on')        
    });

    $('.subYes').on('mouseleave', function() {
        $(this).children('.depth1').stop().fadeOut(50)
        $('.gnb').perents('.inner').siblings('.depthAboutBg').stop().fadeOut(500)
    
    });

});


/* main swiper */
let swiper = new Swiper(".mySwiper1", {  
    spaceBetween: 30,
    centeredSlides: true,
    autoplay: {
        delay: 2000,
        disableOnInteraction: false,
      },
    pagination: {
      el: ".swiper-pagination",
      clickable: true,
    },
  });


/* header rolling */

