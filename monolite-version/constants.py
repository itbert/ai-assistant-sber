# constants.py

from typing import Dict, List

# Категории и подкатегории
CATEGORIES: Dict[str, List[str]] = {
    "Safety": [
        "Emergencies (Environmental)",
        "Physical Impacts",
        "Community health and Safety",
        "Employee Health and Safety",
        "Product Safety and Quality"
    ],
    "Environmental": [
        "Waste Management",
        "Climate Risks",
        "Greenhouse Gas Emissions",
        "Air Pollution",
        "Energy Efficiency and Renewable",
        "Hazardous Materials Management",
        "Soil and Groundwater Impact",
        "Wastewater Management",
        "Water Consumption",
        "Surface Water Pollution",
        "Natural Resources",
        "Landscape Transformation",
        "Land Rehabilitation",
        "Biodiversity",
        "Animal Welfare",
        "Environmental Management"
    ],
    "Sustainable Cities": [
        "Planning Limitations",
        "Land Acquisition and Resettlement (Environmental)"
    ],
    "Manufacturing": [
        "Supply Chain (Environmental)"
    ],
    "Culture": [
        "Cultural Heritage"
    ]
}

# Периоды
PERIODS: List[str] = ['Эта неделя', 'Прошлая неделя', 'За весь месяц']

# Источники
SOURCES: List[List[str]] = [
    ['rbc.ru', 'ferra.ru', 'pro.rbc.ru', 'ekb.plus.rbc.ru', 'realty.rbc.ru', 'editorial.rbc.ru', 'wine.rbc.ru', 'rbcrealty.ru'],
    ['Nature.com', 'https://www.artificialintelligence-news.com'], 
    ['RBC.ru', 'Ferra.ru', 'Nature.com', 'https://www.artificialintelligence-news.com'] 
]

# Перевод категорий
TRANSLATION_DICT: Dict[str, str] = {
    "Safety": "Безопасность",
    "Environmental": "Экология",
    "Sustainable Cities": "Устойчивые города",
    "Manufacturing": "Производство",
    "Culture": "Культура",
    "Emergencies (Environmental)": "Чрезвычайные ситуации (экологические)",
    "Physical Impacts": "Физические воздействия",
    "Community health and Safety": "Здоровье и безопасность сообществ",
    "Employee Health and Safety": "Здоровье и безопасность сотрудников",
    "Product Safety and Quality": "Безопасность и качество продукции",
    "Waste Management": "Управление отходами",
    "Climate Risks": "Климатические риски",
    "Greenhouse Gas Emissions": "Выбросы парниковых газов",
    "Air Pollution": "Загрязнение воздуха",
    "Energy Efficiency and Renewable": "Энергоэффективность и возобновляемые источники энергии",
    "Hazardous Materials Management": "Управление опасными материалами",
    "Soil and Groundwater Impact": "Воздействие на почву и подземные воды",
    "Wastewater Management": "Управление сточными водами",
    "Water Consumption": "Потребление воды",
    "Surface Water Pollution": "Загрязнение поверхностных вод",
    "Natural Resources": "Природные ресурсы",
    "Landscape Transformation": "Преобразование ландшафта",
    "Land Rehabilitation": "Восстановление земель",
    "Biodiversity": "Биоразнообразие",
    "Animal Welfare": "Благополучие животных",
    "Environmental Management": "Управление окружающей средой",
    "Supply Chain (Environmental)": "Цепочка поставок (экологическая)",
    "Planning Limitations": "Ограничения планирования",
    "Land Acquisition and Resettlement (Environmental)": "Приобретение земель и переселение (экологические)",
    "Cultural Heritage": "Культурное наследие"
}