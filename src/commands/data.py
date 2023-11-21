from src.auth.router import pwd_context

goods_data = [
    {
        "name": "GRAND THEFT AUTO V: PREMIUM ONLINE EDITION",
        "price": 2299,
        "quantity": 50,
        "is_active": True,
        "image_url": "/static/img/goods/gta.jpg",
    },
    {
        "name": "DARK SOULS 4",
        "price": 2599,
        "quantity": 100,
        "is_active": True,
        "image_url": "/static/img/goods/DS.jpg",
    },
    {
        "name": "RESIDENT EVIL 4 - SEPARATE WAYS",
        "price": 1299,
        "quantity": 150,
        "is_active": True,
        "image_url": "/static/img/goods/RE4.jpg",
    },
    {
        "name": "HEARTS OF IRON IV: CADET EDITION",
        "price": 499,
        "quantity": 200,
        "is_active": True,
        "image_url": "/static/img/goods/HOI4.jpg",
    },
    {
        "name": "SESSION: SKATE SIM ABANDONNED MALL",
        "price": 320,
        "quantity": 300,
        "is_active": True,
        "image_url": "/static/img/goods/SesSAM.jpg",
    },
    {
        "name": "ELDEN RING",
        "price": 2799,
        "quantity": 350,
        "is_active": True,
        "image_url": "/static/img/goods/ER.jpg",
    },
    {
        "name": "CITIES: SKYLINES II - ULTIMATE EDITION",
        "price": 3799,
        "quantity": 400,
        "is_active": True,
        "image_url": "/static/img/goods/CS4.jpg",
    },
]
roles_data = [{"name": "user"}, {"name": "moderator"}, {"name": "admin"}]
users_data = [
    {
        "name": "User",
        "surname": "UserSurname",
        "phone_number": "+71111111111",
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("Userpassword1!"),
        "role_id": 1,
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    },
    {
        "name": "Moderator",
        "surname": "ModeratorSurname",
        "phone_number": "+72222222222",
        "email": "moderator@example.com",
        "hashed_password": pwd_context.hash("Moderatorpassword1!"),
        "role_id": 2,
        "is_active": True,
        "is_superuser": False,
        "is_verified": True,
    },
    {
        "name": "Admin",
        "surname": "AdminSurname",
        "phone_number": "+73333333333",
        "email": "admin@example.com",
        "hashed_password": pwd_context.hash("Admin1password1!"),
        "role_id": 3,
        "is_active": True,
        "is_superuser": True,
        "is_verified": True,
    },
]
