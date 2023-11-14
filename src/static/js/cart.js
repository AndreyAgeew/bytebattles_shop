// Функция для обновления таблицы
async function updateTable() {
    try {
        console.log('updateTable function started');
        // Добавляем метку времени к URL для предотвращения кеширования
        const timestamp = new Date().getTime();
        const response = await fetch(`/pages/cart?timestamp=${timestamp}`, { method: 'GET' });

        // Проверяем успешность запроса
        if (response.ok) {
            // Получаем данные из ответа
            const newData = await response.json();

            // Получаем элемент tbody таблицы
            const tbody = document.querySelector('tbody');

            // Если tbody существует
            if (tbody) {
                // Очищаем содержимое tbody
                tbody.innerHTML = '';

                // Вставляем новые данные в tbody
                newData.forEach(item => {
                    const newRow = document.createElement('tr');
                    newRow.innerHTML = `<td>${item.field1}</td><td>${item.field2}</td>`; // Замените на ваши поля
                    tbody.appendChild(newRow);
                });
            }
        } else {
            // В случае неудачи выводим сообщение об ошибке в консоль
            console.error('Не удалось получить обновленные данные.');
        }
    } catch (error) {
        // В случае ошибки выводим сообщение об ошибке в консоль
        console.error('Ошибка во время запроса:', error);
    }
}

// Функция для обновления таблицы после удаления товара
async function removeFromCart(itemId) {
    try {
        const response = await fetch(`../cart/remove_to_cart/${itemId}`, { method: 'GET' });

        if (response.ok) {
            // Вызываем функцию обновления таблицы сразу после успешного удаления
            await updateTable();
        } else {
            console.error('Failed to remove item from the cart.');
        }
    } catch (error) {
        console.error('Error during the request:', error);
    }
}
