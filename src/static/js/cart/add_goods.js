// Функция для добавления товара в корзину
async function addToCart(itemId) {
    try {
        const response = await fetch(`../cart/add_to_cart/${itemId}`, {method: 'GET'});

    } catch (error) {
        console.error('Error during the request:', error);
    }
}