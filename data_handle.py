import json
from pprint import pprint
from itertools import groupby
from pprint import pprint
import re
import numpy as np


# with open('whiskey.json') as f:
#     whiskey = f.read()
#     whiskey = json.loads(whiskey)
#     f.close()

# print(len(whiskey))
# for i in whiskey:
#     if ('identified' in i.keys()):
#         pprint(i)

# products = [i for i in whiskey if 'identified' in i.keys()]
# print(len(products))

with open('whiskey.json') as f:
    whiskey = f.read()
    whiskey = json.loads(whiskey)
    f.close()


for i in whiskey:

    i['identified'] = False
    if 'product_id' in i.keys():
        i.pop('product_id')
    if 'in_productData' in i.keys():
        i.pop('in_productData')

    whiskey[whiskey.index(i)] = i

with open('whiskey.json', 'w') as f:
    json.dump(whiskey, f, ensure_ascii=False, indent=2)

with open('productData.json') as f:
    products = f.read()
    products = json.loads(products)
    f.close()

products.clear()

with open('productData.json', 'w') as f:
    json.dump(products, f, ensure_ascii=False, indent=2)
    f.close()


# result_list = result_list + my_list
# # print(result_list)
# group_list = [i for i in my_list if 'product_id' in i.keys()]
# groups = groupby(group_list, lambda x: x['product_id'])
# print(list(groups))
# groups = groupby(group_list, lambda x: x['product_id'])
# # print(list(groups))
# print([i[0] for i in list(groups)])
# groups = [list(i[1]) for i in groups]
#
# for j in groups:
#     for k in j:
#         if k in result_list:
#             result_list.remove(k)

# pprint(result_list)

# my_string = '12345'
# result = my_string.isdigit()
# print(result)

# for group in groups:
#     print(group)
a = [{
    "_id": "ca99b96421b0e1a6b06d849b2227afb47a2ea947",
    "features": {
      "Артикул:": " ASTO27284",
      "Объем:": "0.7 л",
      "Тип:": "Виски",
      "Крепость:": "35%",
      "Тип виски:": "Теннесси",
      "Сырье:": "Кукуруза, Рожь, Ячмень",
      "Бренд:": "Jack Daniels",
      "Страна:": "США",
      "Поставщик:": "АСТ, WineStreet, ВАЙНС",
      "Срок годности:": " не ограничен при соблюдении условий хранения"
    },
    "image": [
      "https://static.winestreet.ru/off-line/goods_file/18153/file_S.jpg"
    ],
    "link": [
      "https://winestreet.ru/wiskey/jack-daniels/asto27284.html"
    ],
    "name": [
      "Виски американский «Jack Daniels Tennessee Honey», 0.7 л"
    ],
    "price": [
      "2 303",
      "2 233"
    ],
    "section": [
      "Виски"
    ],
    "spider": [
      "winestreet"
    ],
    "status": "New",
    "identified": True,
    "product_id": "4194243"
  }
]



# a[0]['identified'] = False
# print(a)
# a[0].pop('product_id')
# print(a)


