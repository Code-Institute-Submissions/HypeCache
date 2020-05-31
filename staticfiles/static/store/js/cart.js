var updateBtns = document.getElementsByClassName('update-cart')

for (i = 0; i < updateBtns.length; i++) {
    updateBtns[i].addEventListener('click', function () {
        var productId = this.dataset.product
        var action = this.dataset.action
        console.log('productId:', productId, 'Action:', action)
        console.log('USER:', user)

        if (user == 'AnonymousUser') {
            console.log('Not logged')
        } else {
            updateUserOrder(productId, action)
        }
    })
}

function updateUserOrder(productId, action, value = 1) {
    console.log('Auth sending data')

    var url = '/update_item/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({ 'productId': productId, 'action': action, 'value': value })
    })
        .then((response) => {
            console.log(response)
        })
        .then((data) => {
            console.log('data:', data)
            location.reload()
        })
}