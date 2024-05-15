import os, sys
from dotenv import load_dotenv, dotenv_values, find_dotenv

class Config():

    def __init__(self):
        load_dotenv(find_dotenv())
        self.env = dotenv_values(os.path.join(os.path.dirname(__file__), '.env'))