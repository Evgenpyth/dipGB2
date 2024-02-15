import requests
class ParseWB:
    def __init__(self,url):
        self.utl = url,\


       @staticmethod
       def __get_brand_id(surl:str):


response = requests.get(
    'https://catalog.wb.ru/catalog/electronic15/catalog'
                        )



print(response.status_code)
print(response.json())
