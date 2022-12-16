# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:19:56 2022

@author: ChiChun.Chen
"""


# %%
# Includes Packages
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


# %%
# Include Modules
from src.utility import conditions_search


# %%
app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    description: str
    author: Optional[str]
    borrowed: bool


# %%
# Mock data
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


# %%
# C(create)
@app.post("/api/books")
def add_books(book: Book):
    """ 
    function to add books 
    
    """
    global books
    
    body_data = book.dict()
    
    if body_data == None:
        msg = "Invalid header"
        app.logger.error(msg)
        return msg, 400
    
    if not isinstance(body_data, list):
        msg = "Body type is not array"
        app.logger.error(msg)
        return msg, 400
    
    RequireKeys = ['id', 'title', 'description', 'author', 'borrowed']
    # check if format valid
    if any(key not in book_info.keys() for book_info in body_data for key in RequireKeys):
        msg = f"Invalid format without required key{RequireKeys}"
        app.logger.error(msg)
        return msg, 400
    
    id_list = [book['id'] for book in books]
    # check if id exists
    if any(book_info['id'] in id_list for book_info in body_data):
        msg = "Invalid value ID already exists"
        app.logger.error(msg)
        return msg, 400
    
    books += body_data
    books.sort(key=lambda x: x['id'])
    
    return 'Add books success'


# %%
# R(read)
@app.route("/api/books", methods=["GET"])
def get_books():
    """ 
    function to get all books 
    
    """
    global books
    
    condition = request.args.to_dict()   # GET query
    for key in condition.keys():
        if key == 'id':
            condition[key] = int(condition[key])
        elif key == 'borrowed':
            if condition[key] in ['false', 'False']:
                condition[key] = False
            else:
                condition[key] = True
    
    result = [book for book in books if conditions_search(book, condition)]
    return jsonify({"books": result})


# %%
# U(update)
@app.route("/api/books", methods=["PUT"])
def update_books():
    """ 
    function to update books 
    
    """
    global books
    
    body_data = request.get_json()
    
    if body_data == None:
        msg = "Invalid header"
        app.logger.error(msg)
        return msg, 400
    
    if not isinstance(body_data, list):
        msg = "Body type is not array"
        app.logger.error(msg)
        return msg, 400
    
    RequireKeys = ['id']
    # check if format valid
    if any(key not in book_info.keys() for book_info in body_data for key in RequireKeys):
        msg = f"Invalid format without required key{RequireKeys}"
        app.logger.error(msg)
        return msg, 400
    
    id_list = [book['id'] for book in books]
    # check if id exists
    if any(book_info['id'] not in id_list for book_info in body_data):
        msg = "Invalid value ID not exists"
        app.logger.error(msg)
        return msg, 400
    
    body_data.sort(reverse=True, key=lambda x: x['id'])
    start_idx = 0
    while body_data:
        book_info = body_data.pop()
        
        for i in range(start_idx, len(books)):
            if books[i]['id'] != book_info['id']:
                continue
            
            start_idx = i
            books[i].update(book_info)
            break
    
    return jsonify('Update books success')


# %%
# D(delete)
@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id: int):
    """ 
    function to delete book 
    
    """
    global books

    id_list = [book['id'] for book in books]
    # check if id exists
    if book_id not in id_list:
        msg = "Invalid value ID not exists"
        app.logger.error(msg)
        return msg, 400
    
    for i in range(len(books)):
        if books[i]['id'] != book_id:
            continue
        
        books.pop(i)
        break
    
    return jsonify('Delete book success')


# %%
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1234)