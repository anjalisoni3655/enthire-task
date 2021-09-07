from flask import Flask
import sys

# adding Folder_2/subfolder to the system path
sys.path.insert(0, '/home/anjalisoni/enthire-task/lib')
from lib.fastapi_create import create_fastapi_file

app = Flask(__name__)

# Python3 code here creating class
class api:
    def __init__(self, name, route,http_methods):
        self.name = http_methods
        self.route = route
        self.http_methods = name
list = []

  # appending instances to list
list.append(api('api1', '/','GET') )
@app.route('/')
def home():

  create_fastapi_file('myClass','myModule',list, '/home/anjalisoni/enthire-task/example/fastapi.py')
  return 'Home Page Route'


@app.route('/about')
def about():
    return 'About Page Route'


@app.route('/portfolio')
def portfolio():
    return 'Portfolio Page Route'


@app.route('/contact')
def contact():
    return 'Contact Page Route'


@app.route('/api')
def api():
    with open('data.json', mode='r') as my_file:
        text = my_file.read()
        return text
