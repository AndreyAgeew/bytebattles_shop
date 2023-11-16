import stripe
from config import STRIPE_API_KEY, DOMAIN_NAME


def get_stripe_session(order_id, amount, user):
    stripe.api_key = STRIPE_API_KEY

    product_for_stripe = stripe.Product.create(name=order_id)
    price_for_stripe = stripe.Price.create(
        unit_amount=amount * 100,
        currency="rub",
        product=f"{product_for_stripe.id}",
    )
    session_for_stripe = stripe.checkout.Session.create(
        line_items=[
            {
                # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                'price': f'{price_for_stripe.id}',
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=DOMAIN_NAME + 'success.html',
        cancel_url=DOMAIN_NAME + 'cancel.html',
        customer_email=f'{user.email}'
    )
    return session_for_stripe.url
