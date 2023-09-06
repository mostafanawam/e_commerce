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
        e.preventDefault();
        var product_id = $(this).data('product-id');
        $.ajax({
            type: 'POST',
            url: '/cart/add_to_cart/' + product_id + '/',
            data: {},
            success: function(data) {
                $('.cart_qty').text(data);
                var popup = document.getElementById("myPopup");
                popup.classList.toggle("show");

                window.setTimeout(function() {
                    popup.classList.toggle("show");
                }, 2000);

            }
        });
    });
});