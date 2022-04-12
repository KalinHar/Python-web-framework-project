(function ($) {
    "use strict";


    // alert messages
    var message_ele = document.getElementById("message_container");

    setTimeout(function(){
       message_ele.style.display = "none";
    }, 2000);


    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner();
    
    
    // Back to top button
    $(window).scroll(function () {
        if ($(this).scrollTop() > 300) {
            $('.back-to-top').fadeIn('slow');
        } else {
            $('.back-to-top').fadeOut('slow');
        }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 1500, 'easeInOutExpo');
        return false;
    });


    // Testimonials carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        smartSpeed: 1000,
        items: 1,
        dots: true,
        loop: true,
        nav : false
    });


    // Single Bar Chart
    var ctx3 = $("#line-chart").get(0).getContext("2d");
    var myChart3 = new Chart(ctx3, {
        type: "bar",
        data: {
            labels: parse_labels,
            datasets: [{
                label: "kW",
                fill: false,
                backgroundColor: parse_data_color,
                data: parse_data
            }]
        },
        options: {
            responsive: true
        }
    });


})(jQuery);

