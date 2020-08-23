function updateCartTag(q) {
    console.log(q)
    $("#cart-quantity").text(q);
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

function getCookie(cname) {
  var name = cname + "=";
  var decodedCookie = decodeURIComponent(document.cookie);
  var ca = decodedCookie.split(';');
  for(var i = 0; i <ca.length; i++) {
    var c = ca[i];
    while (c.charAt(0) == ' ') {
      c = c.substring(1);
    }
    if (c.indexOf(name) == 0) {
      return c.substring(name.length, c.length);
    }
  }
  return null;
}
function getCart() {
    var cart = JSON.parse(getCookie('cart'))
    if(cart == undefined) {
        cart = {}
        console.log('A cart is created')
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    }
    return cart
}

function addCookie(productId, action) {
    var cart = getCart()
    console.log('Not logged in...')
    if(action == 'add') {
        if (cart[productId] == undefined) {
            cart[productId] = {'quantity': 1}
        } else {
            cart[productId]['quantity'] += 1
        }
    } else if (action == 'sub') {
        cart[productId]['quantity'] -= 1
        if(cart[productId]['quantity'] <= 0) {
            console.log('Item deleted')
            delete cart[productId]
        }
    }
    console.log(cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
    location.reload()
}

function sendOrderData() {
    console.log('ordered')

    var form = document.getElementById('ship-form')
    var userInfo = {
        'name':null,
        'email': null,
    }

    var shipInfo = {
        'address': null,
        'city': null,
        'state': null,
        'zipcode': null
    }

    shipInfo.address = form.address.value
    shipInfo.city = form.city.value
    shipInfo.state = form.state.value
    shipInfo.zipcode = form.zipcode.value


    if(user == 'AnonymousUser') {
        userInfo.name = form.name.value
        userInfo.email = form.email.value
    }
    console.log(shipInfo)

    const csrftoken = form.getElementsByTagName('input')[0].value
    console.log(csrftoken + " sds")
    $.ajax({
        method: "POST",
        headers: {
            'x-CSRFToken': csrftoken,
        },
        url: "/cart/process_order/",
        data: JSON.stringify({'user-info':userInfo, 'ship-info': shipInfo})
    }).done(function(t) {
        console.log(t)
        cart = {}
        document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
        window.location.href = '/'

    }).fail(function(t) {
        console.log("failed");
    })

}
$( document ).ready(function() {
    console.log( "ready!" )
    updateCart()
    $(document).on("click", ".add-to-cart", function(){
        var product_id = $(this).attr("data-product-id")
        console.log(product_id)
        if(user == 'AnonymousUser') {
            addCookie(product_id, 'add')
        } else {
            sendUpdateRequest(product_id, 'add')
        }
    });

    $(document).on("click", ".sub-from-cart", function(){
        var product_id = $(this).attr("data-product-id")
        console.log(product_id)
        if(user == 'AnonymousUser') {
            addCookie(product_id, 'sub')
        } else {
            sendUpdateRequest(product_id, 'sub')
        }
    });


    $("#payment-info").hide()
    $("#form-wrapper").submit(function(e){
        e.preventDefault(e);
        $(this).hide()
        $("#payment-info").show()
    });
    if (user != 'AnonymousUser'){
        $("#user-info").html('')
    }

});