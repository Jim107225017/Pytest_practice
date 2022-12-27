# Swagger tips

## Sections
* **tags** : URL 標籤
	* type : list

* **produces** : Response content type
	* type : list
	* options : 
		* **application/json**
		* application/xml
		* text/plain

* **parameters** : 
	* type : list of dictionary
		* **name** : parameter name
			* type : string
		* **in** : parameter location
			* type : option
			* options : 
				* **"body"** (POST、PUT)
				* **path** (GET、DELETE)
				* **query** (GET)
		* **type** : data type
			* type : option
			* options : 
				* string
				* number
				* integer
				* boolean
				* array (list)
				* object (dictionary)
		* **description** : parameter description
			* type : string
		* **required** : requirement
			* type : boolean
		* schema : complicated data structure **(body only)**
			* usage : `$ref: "#/definitions/example1"`

* **definitions** : For **reuse schema**
	* key : schema name
	* value : data **type**

* **responses**
    * key : status code
    * value : **description** and/or **schema**

## sample code
* Object type
    * part : 
        * **type** (object)
        * **properties**
        * **required**
    * example : 
        ```yml=
        book_body:
            type: object
            properties:
                id:
                    type: integer
                    format: int64
                title:
                    type: string
                description:
                    type: string
                author:
                    type: string
                borrowed:
                    type: boolean
            required:
                - id
                - title
                - description
                - author
                - borrowed
        ```
    
    * demo : 

        > ![sample_0.png](https://i.imgur.com/Ic02fkE.png)

* Array type
    * part : 
        * **type** (array)
        * **items**
    * example : 
        ```yml=
        books_body:
            type: array
            items:
                $ref: "#/definitions/book_body"
        ```
    
    * demo : 
    
        > ![sample_1.png](https://i.imgur.com/j9tUYbm.png)

* response
    * part : 
        * **description**
        * **schema**
    * example : 
        ```yml=
        200:
            description: A list of books
            schema:
                type: object
                properties:
                    books:
                        $ref: "#/definitions/books_body"
        ```
    
    * demo : 
        
        > ![sample_2.png](https://i.imgur.com/RtbkhoJ.png)


## Reference
* [Swagger-OAS2](https://swagger.io/docs/specification/2-0/describing-responses/)
* [Swagger-OAS3](https://swagger.io/docs/specification/describing-responses/)
* [Swagger-editor](https://editor.swagger.io/)
* [chatGPT](https://chat.openai.com/)