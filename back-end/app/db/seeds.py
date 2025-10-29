first_product = {
    "name": "Chicken Dumplings",
    "name_ua": "Пельмені з куркою",
    "name_pl": "Pierogi z kurczakiem",
    "price": 15,
    "type": "by portion",
    "status": True,
    "img": "https://i.ibb.co/Q33Zbq12/unfinded.webp",
    "description": "Juicy chicken dumplings served with sour cream.",
    "description_ua": "Соковиті пельмені з куркою, подаються зі сметаною.",
    "description_pl": "Soczyste pierogi z kurczakiem, podawane ze śmietaną."
}
second_product = {
    "name": "Potato Dumplings",
    "name_ua": "Пельмені з картоплею",
    "name_pl": "Pierogi z ziemniakami",
    "price": 15,
    "type": "by portion",
    "status": True,
    "img": "https://i.ibb.co/Q33Zbq12/unfinded.webp",
    "description": "Juicy chicken dumplings served with sour cream.",
    "description_ua": "Соковиті пельмені з куркою, подаються зі сметаною.",
    "description_pl": "Soczyste pierogi z kurczakiem, podawane ze śmietaną."
}

tables = [
    'dumplings',
    'soups',
    'meats',
    'cakes',
]

update_data = {
    "name": "Updated Chicken Dumplings",
    "name_ua": "Оновлені пельмені з куркою",
    "name_pl": "Zaktualizowane pierogi z kurczakiem",
    "description": "Juicy chicken dumplings, now with more herbs.",
    "description_ua": "Соковиті пельмені з куркою, тепер з більше зелені.",
    "description_pl": "Soczyste pierogi z kurczakiem, teraz z większą ilością ziół.",
    "price": 18,
    "type": "by portion",
    "img": "https://i.ibb.co/Q33Zbq12/unfinded.webp",
    "status": True
}

order_payload = {
    "name1": {
        "tableName": "dumplings",
        "productId": 3,
        "quantity": 5,
        "weight": 200,
        "additions": {
            "cutlery": 1,
            "onion": 1,
            "cream": 1
        }
    },
    "name2": {
        "tableName": "dumplings",
        "productId": 2,
        "quantity": 7,
        "weight": 200,
        "additions": {
            "cutlery": 5,
            "onion": 3,
            "cream": 2
        }
    },
}

location_data = {
    "lat": 51.094807700392266,
    "long": 17.020823640221632
}

order_data = {
    "name": "Yurii Tkachenko",
    "phone_number": "884726638",
    "email": "Yurii.Tkachenko@student.wab.edu.pl",
    "total_amount": 354,
    "items": {
        "nameee": {
            "tableName": "dumplings",
            "productId": 2,
            "quantity": 5,
            "weight": 200,
            "additions": {
                "cutlery": 1,
                "onion": 1,
                "cream": 1
            }
        },
        "namee": {
            "tableName": "dumplings",
            "productId": 3,
            "quantity": 7,
            "weight": 200,
            "additions": {
                "cutlery": 5,
                "onion": 3,
                "cream": 2
            }
        },
        "nameeee": {
            "tableName": "dumplings",
            "productId": 4,
            "quantity": 1,
            "weight": 100,
            "additions": {
                "cutlery": 1,
                "onion": 1,
                "cream": 1
            }
        },
        "name3": {
            "tableName": "dumplings",
            "productId": 4,
            "quantity": 1,
            "weight": 100,
            "additions": {
                "cutlery": 0,
                "onion": 0,
                "cream": 0
            }
        }
    },
    "delivery_time": "05:00",
    "delivery_method": "contactless delivery",
    "location": {
        "street": "Gajowicka",
        "home": "146",
        "homeNumber": "12"
    }
}
