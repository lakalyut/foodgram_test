"""Тестовые данные для рецептов."""

TEST_RECIPES = [
    {
        'name': 'Омлет с овощами',
        'text': '''Взбейте яйца, добавьте нарезанные овощи
        и обжарьте на сковороде. Готовьте под крышкой до пышности''',
        'cooking_time': 15,
        'ingredients': [
            ('яйцо', 3),
            ('молоко', 50),
            ('болгарский перец', 50),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic1.jpg',
    },

    {
        'name': 'Куриный суп с лапшой',
        'text': '''Отварите куриное филе, достаньте и разберите на волокна.
        В кипящий бульон добавьте лапшу, морковь и лук.''',
        'cooking_time': 30,
        'ingredients': [
            ('куриное филе', 200),
            ('вода', 1),
            ('лапша', 30),
        ],
        'tags': ['lunch'],
        'image': 'test_pic2.jpg',
    },

    {
        'name': 'Борщ с говядиной',
        'text': '''Отварите мясо, добавьте картофель, капусту и овощную зажарку
         из свеклы, моркови и лука. Варите до готовности.''',
        'cooking_time': 60,
        'ingredients': [
            ('говядина', 300),
            ('вода', 1000),
            ('картофель', 200),
        ],
        'tags': ['lunch'],
        'image': 'test_pic3.jpg',
    },

    {
        'name': 'Овсяная каша с орехами и медом',
        'text': '''Залейте овсянку молоком или водой. Добавьте мед и орехи.''',
        'cooking_time': 10,
        'ingredients': [
            ('овсяные хлопья', 50),
            ('молоко', 150),
            ('мёд', 10),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic4.jpg',
    },

    {
        'name': 'Творожные сырники',
        'text': '''Смешайте творог, яйцо, муку и сахар.
        Обжарьте на сковороде до золотистой корочки.''',
        'cooking_time': 20,
        'ingredients': [
            ('творог', 200),
            ('яйцо', 1),
            ('мука', 30),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic5.jpg',
    },

    {
        'name': 'Овощной суп с чечевицей',
        'text': '''Обжарьте морковь и лук, добавьте воду,
         чечевицу и картофель.''',
        'cooking_time': 30,
        'ingredients': [
            ('чечевица', 100),
            ('картофель', 150),
            ('морковь', 50),
        ],
        'tags': ['lunch'],
        'image': 'test_pic6.jpg',
    },

    {
        'name': 'Гречка с грибами и луком',
        'text': '''Обжарьте нарезанные грибы с луком,
        добавьте отварную гречку и перемешайте.''',
        'cooking_time': 20,
        'ingredients': [
            ('гречека', 100),
            ('вода', 200),
            ('шампиньоны', 100),
        ],
        'tags': ['lunch'],
        'image': 'test_pic7.jpg',
    },

    {
        'name': 'Гречневая каша с яйцом',
        'text': '''Отварите гречку в подсоленной воде.
        Подавайте с вареным яйцом и сливочным маслом.''',
        'cooking_time': 20,
        'ingredients': [
            ('гречка', 50),
            ('вода', 500),
            ('яйцо', 1),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic8.jpg',
    },

    {
        'name': 'Банановые панкейки',
        'text': '''Разомните банан, смешайте с яйцом и мукой.
         Обжаривайте на сухой сковороде по 2 минуты с каждой стороны.''',
        'cooking_time': 15,
        'ingredients': [
            ('банан', 1),
            ('яйцо', 1),
            ('мука', 50),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic9.jpg',
    },

    {
        'name': 'Запеченная рыба с овощами',
        'text': '''Выложите рыбу и нарезанные овощи в форму,
        сбрызните маслом и запекайте при 180°C''',
        'cooking_time': 30,
        'ingredients': [
            ('филе рыбы', 200),
            ('болгарскйи перец', 50),
            ('кабачок', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic10.jpg',
    },

    {
        'name': 'Куриное филе с брокколи',
        'text': '''Обжарьте курицу до румяной корочки,
        добавьте брокколи и тушите под крышкой 10 минут.''',
        'cooking_time': 20,
        'ingredients': [
            ('куриное филе', 200),
            ('брокколи', 150),
            ('чеснок', 5),
        ],
        'tags': ['dinner'],
        'image': 'test_pic11.jpg',
    },

    {
        'name': 'Тушеные кабачки с мясом',
        'text': '''Обжарьте мясо, добавьте нарезанные
        кабачки и тушите под крышкой''',
        'cooking_time': 30,
        'ingredients': [
            ('говядина', 200),
            ('кабачок', 150),
            ('лук', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic12.jpg',
    },

    {
        'name': 'Овощное рагу с фасолью',
        'text': '''Обжарьте лук и морковь, добавьте
        фасоль, томаты и тушите.''',
        'cooking_time': 25,
        'ingredients': [
            ('фасоль', 150),
            ('томатная паста', 30),
            ('морковь', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic13.jpg',
    },

    {
        'name': 'Рис с курицей и овобщами',
        'text': '''Обжарьте курицу, добавьте нарезанные
        овощи и рис, тушите.''',
        'cooking_time': 30,
        'ingredients': [
            ('рис', 100),
            ('куриное филе', 150),
            ('болгарский перец', 50),
        ],
        'tags': ['lunch'],
        'image': 'test_pic14.jpg',
    },

    {
        'name': 'Рыбные котлеты с картофелем',
        'text': '''Измельчите рыбу с луком, слепите котлеты и обжарьте.
        Подавайте с картофельным пюре.''',
        'cooking_time': 40,
        'ingredients': [
            ('филе рыбы', 200),
            ('картофель', 200),
            ('лук', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic15.jpg',
    },

    {
        'name': 'Салат с тунцом и яйцом',
        'text': '''Нарежьте овощи, добавьте тунец и яйцо, заправьте маслом.''',
        'cooking_time': 15,
        'ingredients': [
            ('тунец', 100),
            ('яйцо', 1),
            ('огурец', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic16.jpg',
    },

    {
        'name': 'Гречка с печенью и луком',
        'text': '''Обжарьте печень с луком, добавьте вареную гречку,
        перемешайте и подогрейте.''',
        'cooking_time': 25,
        'ingredients': [
            ('куриная печень', 150),
            ('гречка', 100),
            ('лук', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic17.jpg',
    },

    {
        'name': 'Паста с курицей и грибами',
        'text': '''Обжарьте курицу с грибами, добавьте сливки.
        Смешайте с отваренной пастой.''',
        'cooking_time': 30,
        'ingredients': [
            ('паста', 100),
            ('куриное филе', 150),
            ('шампиньоны', 100),
        ],
        'tags': ['dinner'],
        'image': 'test_pic18.jpg',
    },

    {
        'name': 'Спагетти с томатным соусом и сыром',
        'text': '''Отварите спагетти, смешайте с соусом из томатов,
        чеснока и лука. Посыпьте сыром.''',
        'cooking_time': 25,
        'ingredients': [
            ('спагетти', 100),
            ('томатный соус', 100),
            ('лук', 50),
        ],
        'tags': ['lunch'],
        'image': 'test_pic19.jpg',
    },

    {
        'name': 'Картофельное пюре с котлетой',
        'text': '''Отварите картофель и разомните с молоком.
        Приготовьте мясные котлеты на сковороде.''',
        'cooking_time': 40,
        'ingredients': [
            ('картофель', 200),
            ('молоко', 50),
            ('фарш', 150),
        ],
        'tags': ['lunch'],
        'image': 'test_pic20.jpg',
    },

    {
        'name': 'Омлет с помидорами и сыром',
        'text': '''Взбейте яйца, добавьте нарезанные помидоры и тертый сыр.''',
        'cooking_time': 15,
        'ingredients': [
            ('яйцо', 3),
            ('помидор', 50),
            ('сыр', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic21.jpg',
    },

    {
        'name': 'Пшенная каша с тыквой',
        'text': '''Отварите пшено с тыквой и молоком до мягкости.
        Добавьте сахар по вкусу.''',
        'cooking_time': 30,
        'ingredients': [
            ('пшено', 50),
            ('тыква', 100),
            ('молоко', 150),
        ],
        'tags': ['lunch'],
        'image': 'test_pic22.jpg',
    },

    {
        'name': 'Цезарь с курицей',
        'text': '''Обжарьте курицу, нарежьте листья салата и добавьте сухарики.
        Заправьте соусом.''',
        'cooking_time': 20,
        'ingredients': [
            ('куриное филе', 150),
            ('листья салата', 100),
            ('сухарики', 30),
        ],
        'tags': ['lunch'],
        'image': 'test_pic23.jpg',
    },

    {
        'name': 'Куриное филе в сливочном соусе с рисом',
        'text': '''Обжарьте курицу, добавьте сливки, тушите 10 минут.
        Подавайте с отварным рисом.''',
        'cooking_time': 30,
        'ingredients': [
            ('куриное филе', 150),
            ('рис', 100),
            ('сливки', 100),
        ],
        'tags': ['lunch'],
        'image': 'test_pic24.jpg',
    },

    {
        'name': 'Запеканка из кабачков с сыром',
        'text': '''Натертые кабачки смешайте с яйцом и сыром,
        выложите в форму и запекайте при 180°C''',
        'cooking_time': 40,
        'ingredients': [
            ('кабачок', 200),
            ('яйцо', 1),
            ('сыр', 50),
        ],
        'tags': ['dinner'],
        'image': 'test_pic25.jpg',
    },

    {
        'name': 'Тушеная капуста с куриным филе',
        'text': '''Обжарьте куриное филе, добавьте нашинкованную капусту,
        морковь и томатную пасту. ''',
        'cooking_time': 30,
        'ingredients': [
            ('куриное филе', 200),
            ('капуста', 300),
            ('морковь', 50),
        ],
        'tags': ['lunch'],
        'image': 'test_pic26.jpg',
    },

    {
        'name': 'Омлет с сыром и зеленью',
        'text': '''Взбейте яйца, добавьте тертый сыр и зелень.
        Жарьте на сковороде под крышкой.''',
        'cooking_time': 15,
        'ingredients': [
            ('яйцо', 3),
            ('сыр', 50),
            ('петрушка', 10),
        ],
        'tags': ['lunch'],
        'image': 'test_pic27.jpg',
    },

    {
        'name': 'Гречневые оладьи',
        'text': '''Перемешайте вареную гречку с яйцом и мукой.
        Обжарьте на сковороде до золотистой корочки.''',
        'cooking_time': 15,
        'ingredients': [
            ('гречка', 100),
            ('яйцо', 1),
            ('мука', 30),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic28.jpg',
    },

    {
        'name': 'Рисовая каша яблоками',
        'text': '''Отварите рис в молоке, добавьте нарезанное яблоко и сахар.
        Варите до мягкости.''',
        'cooking_time': 25,
        'ingredients': [
            ('рис', 50),
            ('молоко', 150),
            ('яблоко', 50),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic29.jpg',
    },

    {
        'name': 'Тост с авокадо и яйцом',
        'text': '''Разомните авокадо, выложите на тост,
        добавьте нарезанное вареное яйцо.''',
        'cooking_time': 10,
        'ingredients': [
            ('тост', 1),
            ('авакадо', 50),
            ('яйцо', 1),
        ],
        'tags': ['breakfast'],
        'image': 'test_pic30.jpg',
    },
]
