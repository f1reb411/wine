from collections import defaultdict
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from environs import Env
from jinja2 import Environment, FileSystemLoader, select_autoescape


def main():
    env = Env()
    env.read_env()
    environment = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html'])
    )
    template = environment.get_template('template.html')

    plant_foundation_year = env.int('PLANT_FOUNDATION_YEAR')
    years_since_foundation = datetime.now().year - plant_foundation_year

    filepath = env.str('FILE_PATH')
    products = pandas.read_excel(filepath, keep_default_na=False).to_dict(orient='records')

    beverages = defaultdict(list)

    for product in products:
        beverages[product['Категория']].append(product)

    rendered_page = template.render(years=years_since_foundation,
                                    beverages=beverages)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
