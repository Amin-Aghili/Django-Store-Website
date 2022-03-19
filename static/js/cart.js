var updateBtns = document.getElementsByClassName("update-cart")

for (var i = 0; i < updateBtns.length; i++){
    updateBtns[i].addEventListener("click", function(){
        var product_id = this.dataset.product
        var action = this.dataset.action
        console.log('product_id:', product_id, 'action:', action)

        console.log('USER:', user)
        if (user == 'AnonymousUser'){
            addCookieItem(product_id, action)
        }else{
            updateUserOrder(product_id, action)
        }
    })
}

function addCookieItem(product_id, action){
    console.log("User is not logged in, using cookies")
    if (action == 'add'){
        if (cart[product_id] == undefined){
            cart[product_id] = {'quantity': 1}
        }else{
            cart[product_id]['quantity'] += 1
        }
    }

    if (action == 'remove'){
        cart[product_id]['quantity'] -= 1
        if (cart[product_id]['quantity'] <= 0){
            delete cart[product_id]
        }
    }
    console.log('cart:', cart)
    document.cookie = 'cart=' + JSON.stringify(cart) + ';domain=;path=/'
    location.reload()
}

function updateUserOrder(product_id, action){
    console.log('User is logged in, sending data...')

    var url = '/cart/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'product_id': product_id, 'action': action})
    })
    .then(response => {
        return response.json()
    })

    .then(data => {
        console.log('data:', data)
        location.reload()
    })
}



function getToken(name) {
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
const csrftoken = getToken('csrftoken');

function getCookie(name) {
    var cookieArr = document.cookie.split(';');
    for(var i = 0; i < cookieArr.length; i++) {
        var cookiePair = cookieArr[i].split('=');
        if(name == cookiePair[0].trim()) {
            return decodeURIComponent(cookiePair[1]);
        }
    }
    return null;
}
var cart = JSON.parse(getCookie('cart'))
if(cart == undefined) {
    cart = {}
    console.log('Cart was created')
    document.cookie = 'cart=' + JSON.stringify(cart) + ";domain=;path=/"
}
console.log('Cart:', cart)
