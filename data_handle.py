import json
from pprint import pprint
from itertools import groupby
from pprint import pprint
import re
import numpy as np
import os


# answer = list(os.popen('heroku ps:copy productData.json'))
# print(answer)
# os.rename('productData_.json', 'productData.json')

os.system('git add .')
os.system('git commit -am "optimised"')
answer = list(os.popen('git push heroku master'))
print(answer)

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

# with open('whiskey.json') as f:
#     whiskey = f.read()
#     whiskey = json.loads(whiskey)
#     f.close()
#
# with open('whiskey.json', 'w') as f:
#     json.dump(whiskey[:5], f, ensure_ascii=False, indent=2)
#     f.close()
#
#
# for i in whiskey:
#
#     i['identified'] = False
#     if 'product_id' in i.keys():
#         i.pop('product_id')
#     if 'in_productData' in i.keys():
#         i.pop('in_productData')
#
#     whiskey[whiskey.index(i)] = i
#
# with open('whiskey.json', 'w') as f:
#     json.dump(whiskey, f, ensure_ascii=False, indent=2)


# with open('productData.json') as f:
#     products = f.read()
#     products = json.loads(products)
#     f.close()
#
# products.clear()
#
# with open('productData.json', 'w') as f:
#     json.dump(products, f, ensure_ascii=False, indent=2)
#     f.close()


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

# a = ['https://winestreet.ru/wiskey/jack-daniels/5099873046050.html', 'https://winestreet.ru/wiskey/jack-daniels/5099873046050.html', 'https://winestreet.ru/wiskey/jack-daniels/5099873046050.html']

# with open('link_list.json', 'w') as f:
#     json.dump([], f, ensure_ascii=False, indent=2)

# with open('test_file.json') as f:
#     test = f.read()
#     test = json.loads(test)
#     f.close()
#
# for i in test:
#     if i.isdigit():
#         print(i)


# a[0]['identified'] = False
# print(a)
# a[0].pop('product_id')
# print(a)


