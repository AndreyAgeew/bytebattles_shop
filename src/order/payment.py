import stripe
from config import STRIPE_API_KEY, DOMAIN_NAME


def get_stripe_session(goods, user):
    stripe.api_key = STRIPE_API_KEY
    line_items = []
    for game in goods:
        item = {
            'price': game.create_stripe_product_price(),
            'quantity': 1,
        }
        line_items.append(item)

    session_for_stripe = stripe.checkout.Session.create(
        line_items=line_items,
        mode='payment',
        success_url=DOMAIN_NAME + 'pages/orders',
        cancel_url=DOMAIN_NAME + 'pages/orders',
        customer_email=f'{user.email}'
    )
    return session_for_stripe.url
