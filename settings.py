from os.path import join, dirname
from dotenv import load_dotenv
import json


def load_requirements():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    with open('config.json', encoding='UTF-8') as file:
        config = json.load(file)

    return config
