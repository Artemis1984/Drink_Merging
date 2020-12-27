import json
from pprint import pprint
from ftplib import FTP
import os
import time
from multiprocessing import Pool
from main import Merger_DB


def get_from_site(file_name):
    ftp = FTP(host='130.193.59.64', user='ftpimport', passwd='die4ro')
    ftp.cwd('upload')
    ftp.retrbinary('RETR ' + file_name, open(file_name, 'wb').write)
    ftp.close()


def put_to_site(file_name):
    ftp = FTP(host='130.193.59.64', user='ftpimport', passwd='die4ro')
    ftp.cwd('upload')
    ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))
    ftp.close()


def get_from_merger(file_name):
    ftp = FTP(host='185.26.122.77',  user='host1823810', passwd='tSjtEi6lAt')
    ftp.cwd('host1823810.hostland.pro')
    ftp.cwd('htdocs')
    ftp.cwd('www')
    ftp.retrbinary('RETR ' + file_name, open(file_name, 'wb').write)


def put_to_merger(file_name):
    ftp = FTP(host='185.26.122.77',  user='host1823810', passwd='tSjtEi6lAt')
    ftp.cwd('host1823810.hostland.pro')
    ftp.cwd('htdocs')
    ftp.cwd('www')
    ftp.storbinary('STOR ' + file_name, open(file_name, 'rb'))


def delete_from_merger(file_name):
    ftp = FTP(host='185.26.122.77', user='host1823810', passwd='tSjtEi6lAt')
    ftp.cwd('host1823810.hostland.pro')
    ftp.cwd('htdocs')
    ftp.cwd('www')
    ftp.delete(file_name)


def change_file_name_in_merger(change_from, change_to):
    ftp = FTP(host='185.26.122.77', user='host1823810', passwd='tSjtEi6lAt')
    ftp.cwd('host1823810.hostland.pro')
    ftp.cwd('htdocs')
    ftp.cwd('www')
    ftp.rename(change_from, change_to)


def read_file(file_name):
    with open(file_name) as f:
        file = f.read()
        file = json.loads(file)
        f.close()
    return file


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()
    return


def get_all_files_from_merger():
    get_from_merger('whiskey.json')
    get_from_merger('vodka.json')
    get_from_merger('cognac.json')
    get_from_merger('champagne.json')
    get_from_merger('productData.json')


# def count_new_products(section):
#
#     whiskey = read_file('whiskey.json')
#     vodka = read_file('vodka.json')
#     cognac = read_file('cognac.json')
#     champagne = read_file('champagne.json')
#     counter = 0
#     sections = {'Виски': whiskey, 'Водка': vodka, 'Коньяк': cognac, 'Шампанское и игристое вино': champagne}
#
#     for i in list(Bonk_base[section].find()):
#         found = [k for k in sections[section] if k['_id'] == i['_id']]
#         if not found:
#             counter += 1
#
#     print(counter)


# def update_db(section):
#
#     get_all_files_from_merger()
#
#     whiskey = read_file('whiskey.json')
#     vodka = read_file('vodka.json')
#     cognac = read_file('cognac.json')
#     champagne = read_file('champagne.json')
#
#     sections = {'Виски': whiskey, 'Водка': vodka, 'Коньяк': cognac, 'Шампанское и игристое вино': champagne}
#
#     for i in Bonk_base[section].find():
#         found = [k for k in sections[section] if k['_id'] == i['_id']]
#         if found:
#             found = found[0]
#             if 'in_productData' in found.keys():
#                 Bonk_base[section].update_one({'_id': found['_id']}, {'$set': {'in_productData': True, 'product_id': found['product_id'], 'id': found['id'], 'identified': True}})
#             elif 'product_id' in found.keys():
#                 Bonk_base[section].update_one({'_id': found['_id']}, {'$set': {'product_id': found['product_id'], 'id': found['id'], 'identified': True}})
#             elif 'id' in found.keys():
#                 Bonk_base[section].update_one({'_id': found['_id']}, {'$set': {'id': found['id']}})
#
#
# def saving_to_files_new_data():
#     collections_files = {'Виски': 'whiskey.json', 'Водка': 'vodka.json', 'Коньяк': 'cognac.json', 'Шампанское и игристое вино': 'champagne.json'}
#     for i in collections_files:
#         collection = list(Bonk_base[i].find())
#         write_file(collections_files[i], collection)
#
#
# def handle_productData():
#
#     get_from_merger('productData.json')
#     productData = read_file('productData.json')
#     for product in productData:
#         product.pop('_id')
#         product.pop('links')
#         product['name'] = product['name'].strip(' ').replace('"', '').replace(',', '').replace('«', '').replace('»', '').replace('  ', '').lower().capitalize()
#         for feature in product['features']:
#             product['features'][feature] = product['features'][feature].strip(' ').replace('  ', '').replace(' Подробнее: https://winestyle.ru', '').lower().capitalize() if type(product['features'][feature]) == str else product['features'][feature]
#
#     write_file('productData.json', productData)
#
#
# def handle_offerData():
#
#     get_from_site('offerData.json')
#     offerData = read_file('offerData.json')
#     collections = ['Виски', 'Водка', 'Коньяк', 'Шампанское и игристое вино']
#     for i in offerData:
#         i['active'] = False
#     for collection in collections:
#         for item in Bonk_base[collection].find({'$and': [{'in_productData': {'$exists': True}}, {'active': True}, {"features.Объем": {"$exists": True}}]}):
#             found = [offer for offer in offerData if offer['id'] == item['id']]
#             if found:
#                 ind = offerData.index(found[0])
#                 found[0]['price'] = item['price']
#                 found[0]['active'] = item['active']
#                 found[0]['Идентификатор поставщика'] = item['data_id']
#                 offerData[ind] = found[0]
#             else:
#                 new_offer = dict()
#                 new_offer['id'] = item['id']
#                 new_offer['product_id'] = item['product_id']
#                 new_offer['name'] = item['name']
#                 new_offer['price'] = item['price']
#                 new_offer['url'] = item['link']
#                 new_offer['provider'] = item['spider']
#                 new_offer['active'] = item['active']
#                 new_offer['Идентификатор поставщика'] = item['data_id']
#                 new_offer['volume'] = item['features']['Объем']
#                 offerData.append(new_offer)
#
#     write_file('offerData.json', offerData)
#

# убираем повторы с productData
# delete_list = set([i for i in pd_id if pd_id.count(i) > 1])
#
# for i in delete_list:
#     for j in productData:
#         if j['id'] == i:
#             for k in range(pd_id.count(i) - 1):
#                 productData.remove(j)
#             break


# Проверка уникальности ID
# productData = read_file('productData.json')
# whiskey = read_file('whiskey.json')
# vodka = read_file('vodka.json')
# cognac = read_file('cognac.json')
# champagne = read_file('champagne.json')
# pd_id = ([i['id'] for i in champagne if 'id' in i.keys()])
# pprint(([i for i in pd_id if pd_id.count(i) > 1]))


# Обновляем БД и записываем в файлы
# collections = ['Виски', 'Водка', 'Коньяк', 'Шампанское и игристое вино']
# for i in collections:
#     count_new_products(i)
#     Bonk_base[i].delete_many({})
#     Bonk_base[i].update_many({}, {'$set': {'active': True}})
    # update_db(i)
# saving_to_files_new_data()


# testing save
# def save_coll_reserve(file_name, data):
#     with open('test dir/' + file_name, 'w') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#         f.close()
#
#
# def read_file_from_test(file_name):
#     with open('test dir/' + file_name) as f:
#         file = f.read()
#         file = json.loads(file)
#         f.close()
#     return file


# repair db
# for i in read_file_from_test('whiskey.json'):
#     Bonk_base['Виски'].update_one({'_id': i['_id']}, {'$set': i}, upsert=True)
#
# for i in read_file_from_test('vodka.json'):
#     Bonk_base['Водка'].update_one({'_id': i['_id']}, {'$set': i}, upsert=True)
#
# for i in read_file_from_test('cognac.json'):
#     Bonk_base['Коньяк'].update_one({'_id': i['_id']}, {'$set': i}, upsert=True)
#
# for i in read_file_from_test('champagne.json'):
#     Bonk_base['Шампанское и игристое вино'].update_one({'_id': i['_id']}, {'$set': i}, upsert=True)

# def saving_to_files_new_data_test():
#     collections_files = {'Виски': 'whiskey.json', 'Водка': 'vodka.json', 'Коньяк': 'cognac.json', 'Шампанское и игристое вино': 'champagne.json'}
#     for i in collections_files:
#         collection = list(Bonk_base[i].find())
#         save_coll_reserve(collections_files[i], collection)

# brend_country_provider.json


# def update_bcp():
#     get_from_site('brend_country_provider.json')
#     bcp = read_file('brend_country_provider.json')[0]
#     productData = read_file('productData.json')
#     new_bcp = dict()
#     new_bcp['Страны'] = []
#     new_bcp['Бренды'] = []
#     for i in productData:
#         if not (i['features']['Страна'].lower() in [i.lower() for i in bcp['Страны']]):
#             new_bcp['Страны'].append(i['features']['Страна'])
#
#         if not (i['features']['Бренд'] in bcp['Бренды']):
#             new_bcp['Бренды'].append(i['features']['Бренд'])
#
#     new_bcp['Страны'] = set(new_bcp['Страны'])
#     new_bcp['Бренды'] = set(new_bcp['Бренды'])
#     pprint(new_bcp)


# get_from_merger('whiskey.json')
# get_from_merger('productData.json')
# get_from_merger('articles.txt')
# Merger_DB['Виски'].delete_many({})
# Merger_DB['productData'].delete_many({})
#
# for i in read_file('whiskey.json'):
#     Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
#
# for i in read_file('productData.json'):
#     Merger_DB['productData'].update({'_id': i['id']}, {'$set': i}, upsert=True)