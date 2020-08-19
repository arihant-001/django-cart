function updateCartCount(q) {
    console.log(q)
    $("#cart-quantity").text(q);

    console.log("added to cart");
}

function updateCart() {
    $.ajax({
        method: "GET",
        url: "/cart/" + $("#cart").attr("data-id"),
    }).done(function(t) {
        updateCartCount(t.quantity)
        console.log(t)
    }).fail(function(t) {
        console.log("fail to add to cart");
    })
}

$( document ).ready(function() {
    console.log( "ready!" )
    updateCart()
    $(document).on("click", ".add-to-cart", function(){
        var form = document.getElementById('form')
        const csrftoken = form.getElementsByTagName('input')[0].value
       $.ajax({
            method: "POST",
            headers: {
                'x-CSRFToken': csrftoken,
            },
            url: "/cart/updatecartitem/",
            data: {
                product: $(this).attr("data-id"),
                quantity: 1,
                cart_id: $("#cart").attr("data-id")
            }
        }).done(function(t) {
            console.log(t)
            updateCart()
        }).fail(function(t) {
            console.log("fail to add to cart");
        })
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}