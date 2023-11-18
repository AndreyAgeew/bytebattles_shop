async function initiatePayment() {
    try {
        const response = await fetch(`../order/create_order/`, { method: 'POST' });

        // Переход по ссылке на оплату
        if (response.ok) {
            const responseData = await response.json();
            const paymentUrl = responseData.payment_url;

            // Простой переход по ссылке
            window.location.href = paymentUrl;
        } else {
            console.error('Error during the request. Status:', response.status);
        }
    } catch (error) {
        console.error('Error during the request:', error);
    }
}