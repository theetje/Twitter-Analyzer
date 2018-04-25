# -*- coding: utf-8 -*-

import helpers
import requests

from Classes.Test import Test

def start():
    """Start the App"""
    page = requests.get('http://examplesite.com')
    contents = page.content
    print(contents)
