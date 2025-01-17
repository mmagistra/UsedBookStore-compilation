test_data = {
    'Authors': [
        'Александр Пушкин',
        'Лев Толстой',
        'Михаил Лермонтов',
        'Николай Гоголь',
        'Федор Достоевский',
        'Иван Тургенев',
        'Иван Гончаров',
        'Антон Чехов',
        'Михаил Шолохов',
    ],
    'Genres': [
        'Роман',
        'Поэзия',
        'Приключения',
        'Фантастика',
        'Детектив',
        'Сатира',
        'История',
        
    ],
    'Publishers': [
        'Эксмо',
        'АСТ',
        'Молодая гвардия',
        'Азбука-Аттикус',
        'Просвещение'
    ],
    'Conditions': [
        {
            'degree_of_wear': 1,
            'description': 'Идеальное',
        },
        {
            'degree_of_wear': 2,
            'description': 'Хорошее',
        },
        {
            'degree_of_wear': 3,
            'description': 'Удовлетворительное',
        },
        {
            'degree_of_wear': 4,
            'description': 'Плохое',
        },
        {
            'degree_of_wear': 5,
            'description': 'Критическое',
        }
    ],
    'Users': [
        {
            'username': 'employee1',
            'email': 'employee@example.com',
            'password': 'cjnhelybr1',
            'group': ['Employee'],
        },
        {
            'username': 'visitor1',
            'email': 'client@example.com',
            'password': 'gjctnbntkm1',
            'group': ['Visitor'],
        }
    ],
    'Profiles': [
        {
            'username': 'admin',
        },
        {
            'username': 'employee1',
        },
        {
            'username': 'visitor1',
        }
    ],
    'Books': [
        {
            'title': 'Война и мир',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Эксмо',
            'published_year': 1869,
            'genres': ['Роман', 'Приключения'],
            'authors': ['Лев Толстой'],
        },
        {
            'title': 'Преступление и наказание',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Просвещение',
            'published_year': 1866,
            'genres': ['Роман', 'Приключения'],
            'authors': ['Федор Достоевский'],
        },
        {
            'title': 'Мастер и Маргарита',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Просвещение',
            'published_year': 1867,
            'genres': ['Роман', 'Приключения'],
            'authors': ['Михаил Лермонтов'],
        },
        {
            'title': 'Отцы и дети',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'АСТ',
            'published_year': 1862,
            'genres': ['Роман'],
            'authors': ['Иван Тургенев'],
        },
        {
            'title': 'Мертвые души',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Азбука-Аттикус',
            'published_year': 1842,
            'genres': ['Роман', 'Сатира'],
            'authors': ['Николай Гоголь'],
        },
        {
            'title': 'Евгений Онегин',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Молодая гвардия',
            'published_year': 1833,
            'genres': ['Поэзия'],
            'authors': ['Александр Пушкин'],
        },
        {
            'title': 'Детство',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Эксмо',
            'published_year': 1852,
            'genres': ['Роман'],
            'authors': ['Лев Толстой'],
        },
        {
            'title': 'Тихий Дон',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'Просвещение',
            'published_year': 1940,
            'genres': ['Роман', 'История'],
            'authors': ['Михаил Шолохов'],
        },
        {
            'title': 'Обломов',
            'description': 'Описание книги',
            'cover': '',
            'publisher': 'АСТ',
            'published_year': 1859,
            'genres': ['Роман'],
            'authors': ['Иван Гончаров'],
        }
    ],
    'BookInstances': [
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 1,
            'storage_cell': 'A1',
            'purchase_price': 120,
            'sale_price': 58,
        },
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 1,
            'storage_cell': 'A21',
            'purchase_price': 100,
            'sale_price': 46,
        },
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 2,
            'storage_cell': 'A31',
            'purchase_price': 92,
            'sale_price': 85,
        },
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 4,
            'storage_cell': 'A41',
            'purchase_price': 124,
            'sale_price': 65,
        },
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 5,
            'storage_cell': 'A51',
            'purchase_price': 46,
            'sale_price': 42,
        },
        {
            'book': {
                'title': 'Преступление и наказание',
                'publisher': 'Просвещение',
                'published_year': 1866
            },
            'condition': 2,
            'storage_cell': 'A2',
            'purchase_price': 200,
            'sale_price': 100,
        },
        {
            'book': {
                'title': 'Преступление и наказание',
                'publisher': 'Просвещение',
                'published_year': 1866
            },
            'condition': 2,
            'storage_cell': 'A2',
            'purchase_price': 342,
            'sale_price': 432,
        },
        {
            'book': {
                'title': 'Преступление и наказание',
                'publisher': 'Просвещение',
                'published_year': 1866
            },
            'condition': 4,
            'storage_cell': 'A2',
            'purchase_price': 32,
            'sale_price': 32,
        },
        {
            'book': {
                'title': 'Мастер и Маргарита',
                'publisher': 'Просвещение',
                'published_year': 1867
            },
            'condition': 3,
            'storage_cell': 'A3',
            'purchase_price': 300,
            'sale_price': 150,
        },
        {
            'book': {
                'title': 'Война и мир',
                'publisher': 'Эксмо',
                'published_year': 1869
            },
            'condition': 4,
            'storage_cell': 'A4',
            'purchase_price': 400,
            'sale_price': 200,
        },
        {
            'book': {
                'title': 'Отцы и дети',
                'publisher': 'АСТ',
                'published_year': 1862
            },
            'condition': 2,
            'storage_cell': 'B1',
            'purchase_price': 150,
            'sale_price': 75,
        },
        {
            'book': {
                'title': 'Отцы и дети',
                'publisher': 'АСТ',
                'published_year': 1862
            },
            'condition': 3,
            'storage_cell': 'B2',
            'purchase_price': 140,
            'sale_price': 70,
        },
        {
            'book': {
                'title': 'Мертвые души',
                'publisher': 'Азбука-Аттикус',
                'published_year': 1842
            },
            'condition': 1,
            'storage_cell': 'C1',
            'purchase_price': 180,
            'sale_price': 90,
        },
        {
            'book': {
                'title': 'Мертвые души',
                'publisher': 'Азбука-Аттикус',
                'published_year': 1842
            },
            'condition': 4,
            'storage_cell': 'C2',
            'purchase_price': 160,
            'sale_price': 80,
        },
        {
            'book': {
                'title': 'Евгений Онегин',
                'publisher': 'Молодая гвардия',
                'published_year': 1833
            },
            'condition': 2,
            'storage_cell': 'D1',
            'purchase_price': 120,
            'sale_price': 60,
        },
        {
            'book': {
                'title': 'Евгений Онегин',
                'publisher': 'Молодая гвардия',
                'published_year': 1833
            },
            'condition': 3,
            'storage_cell': 'D2',
            'purchase_price': 110,
            'sale_price': 55,
        },
        {
            'book': {
                'title': 'Детство',
                'publisher': 'Эксмо',
                'published_year': 1852
            },
            'condition': 1,
            'storage_cell': 'E1',
            'purchase_price': 130,
            'sale_price': 65,
        },
        {
            'book': {
                'title': 'Детство',
                'publisher': 'Эксмо',
                'published_year': 1852
            },
            'condition': 2,
            'storage_cell': 'E2',
            'purchase_price': 125,
            'sale_price': 62,
        },
        {
            'book': {
                'title': 'Тихий Дон',
                'publisher': 'Просвещение',
                'published_year': 1940
            },
            'condition': 3,
            'storage_cell': 'F1',
            'purchase_price': 140,
            'sale_price': 70,
        },
        {
            'book': {
                'title': 'Тихий Дон',
                'publisher': 'Просвещение',
                'published_year': 1940
            },
            'condition': 4,
            'storage_cell': 'F2',
            'purchase_price': 135,
            'sale_price': 68,
        },
        {
            'book': {
                'title': 'Обломов',
                'publisher': 'АСТ',
                'published_year': 1859
            },
            'condition': 5,
            'storage_cell': 'G1',
            'purchase_price': 170,
            'sale_price': 85,
        },
        {
            'book': {
                'title': 'Обломов',
                'publisher': 'АСТ',
                'published_year': 1859
            },
            'condition': 3,
            'storage_cell': 'G2',
            'purchase_price': 165,
            'sale_price': 83,
        }
    ],
}