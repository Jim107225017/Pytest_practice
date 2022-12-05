# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 17:08:35 2022

@author: ChiChun.Chen
"""

# %%
# Include Packages
import pytest
import requests
from threading import Thread


# %%
# Include Modules
from src.api_bookstore import app


# %%
URL = 'http://127.0.0.1:1234'


# %%
@pytest.fixture(scope="module", autouse=True)
def setup():
    # Start running mock server in a separate thread.
    # Daemon threads automatically shut down when the main process exits.
    mock_server_thread = Thread(target=app.run, args=('0.0.0.0', '1234'))
    mock_server_thread.setDaemon(True)
    mock_server_thread.start()


# %%
def test_get_books():
    global URL
    
    books = [
        {
            "id": 1,
            "title": "CS50",
            "description": "Intro to CS and art of programming!",
            "author": "Havard",
            "borrowed": True
        },
        {
            "id": 2,
            "title": "Python 101",
            "description": "little python code book.",
            "author": "Will",
            "borrowed": False
        }
    ]
    
    url_a = f'{URL}/api/books'
    response_a = requests.request('GET', url_a)
    
    url_b = f'{URL}/api/books?author=Havard'   # query
    response_b = requests.request('GET', url_b)
    
    url_c = f'{URL}/api/books?author=Havard&title=CS50'   # query
    response_c = requests.request('GET', url_c)
    
    url_d = f'{URL}/api/books?author=Jim'   # query
    response_d = requests.request('GET', url_d)
    
    url_e = f'{URL}/api/book'
    response_e = requests.request('GET', url_e)
    
    url_f = f'{URL}/api/books?description=little python code book.'   # query
    response_f = requests.request('GET', url_f)
    
    url_g = f'{URL}/api/books?borrowed=false'   # query
    response_g = requests.request('GET', url_g)
    
    url_h = f'{URL}/api/books?id=1'   # query
    response_h = requests.request('GET', url_h)
    
    
    assert response_a.status_code == 200
    assert isinstance(response_a.json()['books'], list)
    assert isinstance(response_a.json()['books'][0], dict)
    assert response_a.json()['books'] == books
    
    assert response_b.status_code == 200
    assert isinstance(response_b.json()['books'], list)
    assert isinstance(response_b.json()['books'][0], dict)
    assert response_b.json()['books'][0]['author'] == 'Havard'
    
    assert response_c.status_code == 200
    assert isinstance(response_c.json()['books'], list)
    assert isinstance(response_c.json()['books'][0], dict)
    assert response_c.json()['books'][0]['author'] == "Havard"
    assert response_c.json()['books'][0]['title'] == "CS50"
    
    assert response_d.status_code == 200
    assert isinstance(response_d.json()['books'], list)
    assert len(response_d.json()['books']) == 0   # empty result
    
    assert response_e.status_code == 404   # page not found
    
    assert response_f.status_code == 200
    assert isinstance(response_f.json()['books'], list)
    assert isinstance(response_f.json()['books'][0], dict)
    assert response_f.json()['books'][0]['id'] == 2
    
    assert response_g.status_code == 200
    assert isinstance(response_g.json()['books'], list)
    assert isinstance(response_g.json()['books'][0], dict)
    assert response_g.json()['books'][0]['id'] == 2
    
    assert response_h.status_code == 200
    assert isinstance(response_h.json()['books'], list)
    assert isinstance(response_h.json()['books'][0], dict)
    assert response_h.json()['books'][0]['author'] == 'Havard'
    

# %%
def test_get_books_fail_sample():
    global URL
    
    url_e = f'{URL}/api/book'
    response_e = requests.request('GET', url_e)
    
    assert response_e.status_code == 403   # page not found
    

# %%
def test_add_books():
    global URL
    
    url = f'{URL}/api/books'
    
    new_books_a = [
        {
            "id": 1,
            "title": "test",
            "description": "Python Unitest",
            "author": "Jim",
            "borrowed": False
        }
    ]
    
    new_books_b = {"id": 3,
                   "title": "testA",
                   "description": "Python Unitest",
                   "author": "Jim",
                   "borrowed": True}
    
    new_books_c = [{"id": 3,
                    "description": "Python Unitest",
                    "author": "Jim",
                    "borrowed": True}]
    
    new_books_d = [
        {
            "id": 3,
            "title": "testA",
            "description": "Python Unitest",
            "author": "Jim",
            "borrowed": True
        },
        {
            "id": 4,
            "title": "testB",
            "description": "Python Unitest",
            "author": "Jim",
            "borrowed": False
        }
    ]
    
    response_a = requests.request('POST', url, json=new_books_a)
    response_b = requests.request('POST', url, json=new_books_b)
    response_c = requests.request('POST', url, json=new_books_c)
    response_d = requests.request('POST', url, json=new_books_d)
    
    url_e = f'{URL}/api/books?id=3'   # query
    response_e = requests.request('GET', url_e)
    
    url_f = f'{URL}/api/books?id=4'   # query
    response_f = requests.request('GET', url_f)
    
    assert response_a.status_code == 400
    
    assert response_b.status_code == 400
    
    assert response_c.status_code == 400
    
    assert response_d.status_code == 200
    assert response_d.json() == 'Add books success'
    
    assert response_e.status_code == 200
    assert isinstance(response_e.json()['books'], list)
    assert isinstance(response_e.json()['books'][0], dict)
    assert response_e.json()['books'][0]['author'] == 'Jim'
    
    assert response_f.status_code == 200
    assert isinstance(response_f.json()['books'], list)
    assert isinstance(response_f.json()['books'][0], dict)
    assert response_f.json()['books'][0]['author'] == 'Jim'
    
    
# %%
def test_update_books():
    global URL
    
    url = f'{URL}/api/books'
    
    new_books_a = [
        {
            "id": 1,
            "author": "Jim"
        }
    ]
    
    new_books_b = {"id": 3,
                   "title": "testA",
                   "description": "Python Unitest",
                   "author": "Jim",
                   "borrowed": True}
    
    new_books_c = [{"id": 300,
                    "description": "Python Unitest",
                    "author": "Jim",
                    "borrowed": True}]
    
    response_a = requests.request('PUT', url, json=new_books_a)
    response_b = requests.request('PUT', url, json=new_books_b)
    response_c = requests.request('PUT', url, json=new_books_c)
    
    url_d = f'{URL}/api/books?id=1'   # query
    response_d = requests.request('GET', url_d)
    
    assert response_a.status_code == 200
    assert response_a.json() == 'Update books success'
    
    assert response_b.status_code == 400
    
    assert response_c.status_code == 400    
    
    assert response_d.status_code == 200
    assert isinstance(response_d.json()['books'], list)
    assert isinstance(response_d.json()['books'][0], dict)
    assert response_d.json()['books'][0]['author'] == 'Jim'
    
    
# %%
def test_delete_books():
    global URL
    
    url_a = f'{URL}/api/books/100'
    response_a = requests.request('DELETE', url_a)
    
    url_b = f'{URL}/api/books/1'
    response_b = requests.request('DELETE', url_b)
    
    url_c = f'{URL}/api/books?id=1'   # query
    response_c = requests.request('GET', url_c)
    
    assert response_a.status_code == 400
    
    assert response_b.status_code == 200
    assert response_b.json() == 'Delete book success'
    
    assert response_c.status_code == 200
    assert isinstance(response_c.json()['books'], list)
    assert len(response_c.json()['books']) == 0   # empty result
    
    