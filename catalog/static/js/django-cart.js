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
       $.ajax({
            method: "POST",
            url: "/cart/cartitem/",
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