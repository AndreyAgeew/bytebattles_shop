from email.message import EmailMessage

from src.config import SMTP_USER


def create_order_confirmation_template(email_to, order):
    email = EmailMessage()

    email['Subject'] = "Подтверждение заказа в магазине ByteBattles"
    email["From"] = SMTP_USER
    email["To"] = email_to
    email.set_content(
        f"""
        <h1>Поздравляем с покупкой в магазине ведоигр ByteBattles</h1>
        Спасибо за покупку!\n\nНомер заказа: {order['id']}\nДата заказа: {order['created_at']}\n\nТовары: 
        {'; '.join([game for game in order["games"]])}   
        """,
        subtype='html'
    )
    return email
