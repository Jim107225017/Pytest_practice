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
				* array
				* object
		* **description** : parameter description
			* type : string
		* **required** : requirement
			* type : boolean
		* schema : complicated data structure **(body only)**
			* usage : `$ref: "#/definitions/example1"`

* **definitions** : For **reuse schema**
	* key : schema name
	* value : data structure

* **responses**

## Reference
* [Swagger-OAS2](https://swagger.io/docs/specification/2-0/describing-responses/)
* [Swagger-OAS3](https://swagger.io/docs/specification/describing-responses/)
* [Swagger-editor](https://editor.swagger.io/)
* [chatGPT](https://chat.openai.com/)