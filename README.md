# Pytest_practice
Bookstore CRUD API with **flask** & **pytest** practice

## Why Unitest?
* [Unitest 實踐](https://yu-jack.github.io/2020/09/14/unit-test-best-practice-part-1/)
* [Unitest 介紹](https://hsien-w-wei.medium.com/ut-whats-unit-test-%E5%9C%A8%E5%89%8D%E7%AB%AF%E6%98%AF%E8%A6%81%E6%B8%AC%E4%BB%80%E9%BA%BC-a11efc529204)

## Hint : 
* Test API 重點 : 
	* 回傳資料正確性
	* 資料型態
	* 不符規則的輸入
* Test function 重點 : 
	* 回傳資料正確性
* 不該一昧追求覆蓋率
* 只能測試已知的情境

## Usage : 
1. `cd Pytest_practice`
2. `python -m pytest`

## Reference : 
* [Pytest-Beginner](https://www.minglunwu.com/notes/2022/pytest_101.html)
* [Pytest-FlaskAPI](https://jerryeml.coderbridge.io/2021/07/11/Create-an-API-with-Flask-and-test-with-pytest/)

## FAQ : 
1. PATH issue with pytest **ImportError**
> Ans : Run `pytest` itself as a module with: `python -m pytest`
> [stack overflow](https://stackoverflow.com/questions/10253826/path-issue-with-pytest-importerror-no-module-named-yadayadayada)

