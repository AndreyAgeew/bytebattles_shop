// Функция для обновления таблицы после удаления товара
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`../cart/remove_to_cart/${itemId}`, {method: 'GET'});

    } catch (error) {
        console.error('Error during the request:', error);
    }
}

