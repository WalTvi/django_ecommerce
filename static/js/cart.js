var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function(){
		var productId = this.dataset.product
		var action = this.dataset.action
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}

function updateUserOrder(productId, action) {
    console.log('User is authenticated, sending data to API...');

    var url = 'http://54.172.236.64:8000/api/cart_items/';  // URL de la API externa para almacenar datos del carrito

    // Datos del carrito a enviar a la API
    var cartData = {
        items: [
            { product_id: parseInt(productId), quantity: action === 'add' ? 1 : -1 }
            // Ajusta según la estructura requerida por tu API externa
        ],
    };

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(cartData)
    })
    .then(function(response) {
        if (!response.ok) {
            throw new Error('Error al almacenar datos del carrito en la API');
        }
        return response.json();
    })
    .then(function(data) {
        console.log('Datos del carrito almacenados correctamente en la API:', data);
        location.reload();  // Recargar la página después de almacenar en la API
    })
    .catch(function(error) {
        console.error('Error:', error);
    });
}

function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		cart[productId]['quantity'] -= 1

		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}
	console.log('CART:', cart)
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	location.reload()
}