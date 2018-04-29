import requests

""" Get the content of the page with requests. """
def getPageContent(url):
    page = requests.get(url)
    return page.content
