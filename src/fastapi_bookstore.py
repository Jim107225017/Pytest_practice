# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:40:38 2022

@author: ChiChun.Chen
"""


# %%
# Includes Packages
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, ValidationError, validator, root_validator
from typing import Optional, List
import uvicorn


# %%
# Include Modules
from src.utility import conditions_search


# %%
description = """
BookStoreAPI build by FastAPI

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "create",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "read",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app = FastAPI(title="BookStoreAPI", 
              description=description, 
              version="0.0.0", 
              terms_of_service="https://wise-paas.advantech.com/en-us/marketplace/product/advantech.aifs-phm", 
              contact={"name": "ADVANTECH",
                       "url": "https://wise-paas.advantech.com/en-us/marketplace/product/advantech.aifs-phm",
                       "email": "chichun.chen@advantech.com.tw"}, 
              license_info={"name": "Apache 2.0",
                            "url": "https://www.apache.org/licenses/LICENSE-2.0.html"}, 
              docs_url='/v2/docs', 
              redoc_url='/v2/redoc', 
              openapi_url='/v2/openapi.json', 
              openapi_tags=tags_metadata)


# %%
# define pydantic class
class Book(BaseModel):
    id: int
    title: str
    description: str
    author: str
    borrowed: bool

class Books(BaseModel):
    # list of dict
    __root__: List[Book]

class Book_opt(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    borrowed: Optional[bool]

class Books_opt(BaseModel):
    # list of dict
    __root__: List[Book_opt]

class id_duplicate(BaseModel):
    id_list: list
    new_id_list: list
    
    @root_validator()
    def id_cannot_duplicate(cls, field_value):
        id_list = field_value['id_list']
        new_id_list = field_value['new_id_list']
        if any(new_id in id_list for new_id in new_id_list):
            # 自訂義錯誤訊息
            raise ValueError('ID duplicate error')
        # 返回傳進來的值
        return field_value
    
class id_exist(BaseModel):
    id_list: list
    new_id_list: list
    
    @root_validator()
    def id_need_exist(cls, field_value):
        id_list = field_value['id_list']
        new_id_list = field_value['new_id_list']
        if any(new_id not in id_list for new_id in new_id_list):
            # 自訂義錯誤訊息
            raise ValueError('ID not exist error')
        # 返回傳進來的值
        return field_value


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
@app.post("/api/books", tags=['create'])
def add_books(batch_book: Books):
    """ 
    function to add books 
    
    """
    global books
    
    body_data = batch_book.dict()['__root__']
    
    id_list = [book['id'] for book in books]
    new_id_list = [book['id'] for book in body_data]
    
    try:
        id_duplicate(id_list=id_list, new_id_list=new_id_list)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(e.errors()),
            )
    
    books += body_data
    books.sort(key=lambda x: x['id'])
    
    return 'Add books success'


# %%
# R(read)
@app.get("/api/books", tags=['read'])
def get_books(request: Request, 
              id: Optional[int] = None, 
              title: Optional[str] = None, 
              description: Optional[str] = None, 
              author: Optional[str] = None, 
              borrowed: Optional[bool] = None):
    """ 
    function to get all books 
    
    equal to :
    id: Union[int, None] = None, 
    title: Union[str, None] = None, 
    description: Union[str, None] = None, 
    author: Union[str, None] = None, 
    borrowed: Union[bool, None] = None
    
    """
    global books
    
    condition = dict(request.query_params)
    for key in condition.keys():
        if key == 'id':
            condition[key] = int(condition[key])
        elif key == 'borrowed':
            if condition[key] in ['false', 'False']:
                condition[key] = False
            else:
                condition[key] = True
    
    result = [book for book in books if conditions_search(book, condition)]
    return {"books": result}


# %%
# U(update)
@app.put("/api/books", tags=['update'])
def update_books(batch_book: Books_opt):
    """ 
    function to update books 
    
    """
    global books
    
    body_data = batch_book.dict()['__root__']
    
    id_list = [book['id'] for book in books]
    new_id_list = [book['id'] for book in body_data]
    
    try:
        id_exist(id_list=id_list, new_id_list=new_id_list)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(e.errors()),
            )
    
    start_idx = 0
    body_data.sort(reverse=True, key=lambda x: x['id'])
    while body_data:
        book_info = body_data.pop()
        for i in range(start_idx, len(books)):
            if books[i]['id'] != book_info['id']:
                continue
            
            start_idx = i
            books[i].update(book_info)
            break
    
    return 'Update books success'


# %%
# D(delete)
@app.delete("/api/books/{book_id}", tags=['delete'])
def delete_book(book_id: int):
    """ 
    function to delete book 
    
    """
    global books

    id_list = [book['id'] for book in books]
    new_id_list = [book_id]
    
    try:
        id_exist(id_list=id_list, new_id_list=new_id_list)
    except ValidationError as e:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(e.errors()),
            )
    
    for i in range(len(books)):
        if books[i]['id'] != book_id:
            continue
        
        books.pop(i)
        break
    
    return 'Delete book success'


# %%
if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host="0.0.0.0", port=1234, log_config=log_config)
    # app.run(host='0.0.0.0', port=1234)
