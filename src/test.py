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
from utility import conditions_search


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
    author: Optional[str]
    borrowed: bool

class Books(BaseModel):
    # list of dict
    __root__: List[Book]

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

try:
    id_duplicate(id_list = [1,2,3], new_id_list=[1,2,3])
except ValidationError as e:
    msg = e
    print(e)

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
def get_books(request: Request, book: Book):
    """ 
    function to get all books 
    
    """
    global books
    
    condition = request.query_params   # GET query
    print(condition)
    print(type(condition))
    for key in condition.keys():
        if key == 'id':
            condition[key] = int(condition[key])
        elif key == 'borrowed':
            if condition[key] in ['false', 'False']:
                condition[key] = False
            else:
                condition[key] = True
    
    result = [book for book in books if conditions_search(book, condition)]
    return result


# %%
if __name__ == '__main__':
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    uvicorn.run(app, host="127.0.0.1", port=1234, log_config=log_config)
    # app.run(host='0.0.0.0', port=1234)
