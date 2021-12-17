from http.server import HTTPServer, SimpleHTTPRequestHandler
from datetime import datetime

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from collections import defaultdict
from environs import Env

env = Env()
env.read_env()
environment = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html'])
)
template = environment.get_template('template.html')

plant_year_foundation = env.int('plant_year_foundation')
years_since_foundation = datetime.now().year - plant_year_foundation

data_file = env.str('data_file')
products = pandas.read_excel(data_file, keep_default_na=False).to_dict(orient='records')

categories_dict = {'Белые вина': [], 'Красные вина': [], 'Напитки': []}
beverages = defaultdict(list, categories_dict)

for product in products:
    beverages[product['Категория']].append(product)

rendered_page = template.render(years=years_since_foundation,
                                beverages=beverages)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
