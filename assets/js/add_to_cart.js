$(document).ready(function() {

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally
                xhr.setRequestHeader("X-CSRFToken", $('input[name="csrfmiddlewaretoken"]').val());
            }
        }
    });


    $('.add-to-cart').click(function(e) {
        var product_id = $(this).data('product-id');

        $(this).html("adding <i class='fas fa-spinner fa-spin'/>");

        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/cart/add_to_cart/' + product_id + '/',
            data: {},
            success: function(data) {



                window.setTimeout(function() {
                    $('.add-to-cart').text("Add to Cart");
                    var popup = document.getElementById("myPopup");

                    popup.classList.toggle("show");
                    $('.cart_qty').html(data);

                    window.setTimeout(function() {
                        popup.classList.toggle("show");

                    }, 1000);

                }, 1000);






            }
        });
    });
});