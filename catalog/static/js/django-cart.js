function updateCartTag(q) {
    console.log(q)
    $("#cart-quantity").text(q);

    console.log("added to cart");
}

function updateCart() {
    $.ajax({
        method: "GET",
        url: "/cart/cart_quantity",
    }).done(function(t) {
        updateCartTag(t.quantity)
        console.log(t)
    }).fail(function(t) {
        console.log("fail to add to cart");
    })
}

function sendUpdateRequest(product_id, action) {
    var form = document.getElementById('form')
    const csrftoken = form.getElementsByTagName('input')[0].value
    var data = {
        product_id: product_id,
        quantity: 1,
        action: action
    }
    $.ajax({
        method: "POST",
        headers: {
            'x-CSRFToken': csrftoken,
        },
        url: "/cart/update_cart/",
        data: JSON.stringify(data)
    }).done(function(t) {
        console.log(t)
//        updateCart()
        location.reload()
    }).fail(function(t) {
        console.log("fail to add to cart");
    })
}
$( document ).ready(function() {
    console.log( "ready!" )
    updateCart()
    $(document).on("click", ".add-to-cart", function(){
        var product_id = $(this).attr("data-product-id")
        console.log(product_id)
        sendUpdateRequest(product_id, 'add')
    });

    $(document).on("click", ".sub-from-cart", function(){
        var product_id = $(this).attr("data-product-id")
        console.log(product_id)
        sendUpdateRequest(product_id, 'sub')
    });
});