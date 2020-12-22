from flask import Flask, render_template, request, abort, url_for, redirect, flash
import json
import numpy
import os
import time
from pymongo import MongoClient


client = MongoClient('localhost', 27017)
Merger_DB = client.Merger_DB

app = Flask(__name__)
app.config['SECRET_KEY'] = '12091988BernardoProvencanoToto'


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('main_page.html')


@app.route('/champagne_grouping_prove')
def champagne_grouping_prove():
    return render_template('champagne_grouping_prove.html')


@app.route('/cognac_grouping_prove')
def cognac_grouping_prove():
    return render_template('cognac_grouping_prove.html')


@app.route('/vodka_grouping_prove')
def vodka_grouping_prove():
    return render_template('vodka_grouping_prove.html')


@app.route('/whiskey_grouping_prove')
def whiskey_grouping_prove():
    return render_template('whiskey_grouping_prove.html')


@app.route('/finished_champagne', methods=['GET', 'POST'])
def finished_champagne():

    # for i in read_file('champagne.json'):
    #     Merger_DB['Шампанское и игристое вино'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    #
    # for i in read_file('productData.json'):
    #     Merger_DB['productData'].update({'_id': i['id']}, {'$set': i}, upsert=True)

    show_group = None
    group_titles = None

    champagne = list(Merger_DB['Шампанское и игристое вино'].find())

    merged_champagne = list(Merger_DB['productData'].find({'section': 'Шампанское и игристое вино'}))

    productData_links = [i['links'] for i in merged_champagne]
    productData_groups = [i for i in merged_champagne]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in champagne if i['link'] in show_group]]
        group_titles = productData_groups[0]
    
    if 'search' in request.form:
        group_ind = int(request.form['search']) - 1
        if group_ind > len(merged_champagne):
            flash('У вас нет столько групп')
            return redirect('/finished_champagne')
        show_group = productData_links[group_ind]
        show_group = [[i for i in champagne if i['link'] in show_group]]
        group_titles = productData_groups[group_ind]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups) - 1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in champagne if k['link'] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in champagne if k['link'] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in champagne if k['link'] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in champagne if k['link'] in show_group]]
                    group_titles = productData_groups[0]

    if 'delete_from_finished' in request.form:
        delete_id = request.form['delete_from_finished']

        Merger_DB['productData'].delete_one({'_id': delete_id})

        product_with_id = list(Merger_DB['Шампанское и игристое вино'].find({'product_id': {'$exists': True}}))

        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            i.pop('in_productData')
            Merger_DB['Шампанское и игристое вино'].update({'_id': i['_id']}, {'$unset': {'in_productData': 1}}, upsert=True)

        # Saving data to files
        champagne = list(Merger_DB['Шампанское и игристое вино'].find())
        productData_file = list(Merger_DB['productData'].find())
        write_file('productData.json', productData_file)
        write_file('champagne.json', champagne)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_champagne')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = Merger_DB['productData'].count_documents({'section': 'Шампанское и игристое вино'})

    return render_template('finished_champagne.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/finished_cognac', methods=['GET', 'POST'])
def finished_cognac():

    # for i in read_file('cognac.json'):
    #     Merger_DB['Коньяк'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    #
    # for i in read_file('productData.json'):
    #     Merger_DB['productData'].update({'_id': i['id']}, {'$set': i}, upsert=True)

    show_group = None
    group_titles = None

    cognac = list(Merger_DB['Коньяк'].find())

    merged_cognac = list(Merger_DB['productData'].find({'section': 'Коньяк'}))

    productData_links = [i['links'] for i in merged_cognac]
    productData_groups = [i for i in merged_cognac]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in cognac if i['link'] in show_group]]
        group_titles = productData_groups[0]

    if 'search' in request.form:
        group_ind = int(request.form['search']) - 1
        if group_ind > len(merged_cognac) - 1:
            flash('У вас нет столько групп')
            return redirect('/finished_cognac')
        show_group = productData_links[group_ind]
        show_group = [[i for i in cognac if i['link'] in show_group]]
        group_titles = productData_groups[group_ind]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups) - 1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in cognac if k['link'] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in cognac if k['link'] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in cognac if k['link'] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in cognac if k['link'] in show_group]]
                    group_titles = productData_groups[0]

    if 'delete_from_finished' in request.form:
        delete_id = request.form['delete_from_finished']

        Merger_DB['productData'].delete_one({'_id': delete_id})

        product_with_id = list(Merger_DB['Коньяк'].find({'product_id': {'$exists': True}}))

        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            Merger_DB['Коньяк'].update({'_id': i['_id']}, {'$unset': {'in_productData': 1}}, upsert=True)

        # Saving data to files
        cognac_file = list(Merger_DB['Коньяк'].find())
        productData_file = list(Merger_DB['productData'].find())
        write_file('productData.json', productData_file)
        write_file('whiskey.json', cognac_file)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_cognac')

    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # Число готовых
    done = Merger_DB['productData'].count_documents({'section': 'Коньяк'})

    return render_template('finished_cognac.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/finished_vodka', methods=['GET', 'POST'])
def finished_vodka():

    # for i in read_file('vodka.json'):
    #     Merger_DB['Водка'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    #
    # for i in read_file('productData.json'):
    #     Merger_DB['productData'].update({'_id': i['id']}, {'$set': i}, upsert=True)

    show_group = None
    group_titles = None

    vodka = list(Merger_DB['Водка'].find())

    merged_vodka = list(Merger_DB['productData'].find({'section': 'Водка'}))

    productData_links = [i['links'] for i in merged_vodka]
    productData_groups = [i for i in merged_vodka]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in vodka if i['link'] in show_group]]
        group_titles = productData_groups[0]
        
    if 'search' in request.form:
        group_ind = int(request.form['search']) - 1
        if group_ind > len(merged_vodka):
            flash('У вас нет столько групп')
            return redirect('/finished_vodka')
        show_group = productData_links[group_ind]
        show_group = [[i for i in vodka if i['link'] in show_group]]
        group_titles = productData_groups[group_ind]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in vodka if k['link'] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in vodka if k['link'] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in vodka if k['link'] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in vodka if k['link'] in show_group]]
                    group_titles = productData_groups[0]

    if 'delete_from_finished' in request.form:
        delete_id = request.form['delete_from_finished']

        Merger_DB['productData'].delete_one({'_id': delete_id})

        product_with_id = list(Merger_DB['Водка'].find({'product_id': {'$exists': True}}))

        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            Merger_DB['Водка'].update({'_id': i['_id']}, {'$unset': {'in_productData': 1}}, upsert=True)

        # Saving data to files
        vodka_file = list(Merger_DB['Водка'].find())
        productData_file = list(Merger_DB['productData'].find())
        write_file('productData.json', productData_file)
        write_file('vodka.json', vodka_file)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_vodka')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = Merger_DB['productData'].count_documents({'section': 'Водка'})

    return render_template('finished_vodka.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/finished_whiskey', methods=['GET', 'POST'])
def finished_whiskey():
    
    # for i in read_file('whiskey.json'):
    #     Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    #
    # for i in read_file('productData.json'):
    #     Merger_DB['productData'].update({'_id': i['id']}, {'$set': i}, upsert=True)
    
    show_group = None
    group_titles = None

    whiskey = list(Merger_DB['Виски'].find())

    merged_whiskey = list(Merger_DB['productData'].find({'section': 'Виски'}))

    productData_links = [i['links'] for i in merged_whiskey]
    productData_groups = [i for i in merged_whiskey]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in whiskey if i['link'] in show_group]]
        group_titles = productData_groups[0]
    
    if 'search' in request.form:
        group_ind = int(request.form['search']) - 1
        if group_ind > len(merged_whiskey) - 1:
            flash('У вас нет столько групп')
            return redirect('/finished_whiskey')
        show_group = productData_links[group_ind]
        show_group = [[i for i in whiskey if i['link'] in show_group]]
        group_titles = productData_groups[group_ind]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in whiskey if k['link'] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in whiskey if k['link'] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in whiskey if k['link'] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in whiskey if k['link'] in show_group]]
                    group_titles = productData_groups[0]

    if 'delete_from_finished' in request.form:
        delete_id = request.form['delete_from_finished']

        Merger_DB['productData'].delete_one({'_id': delete_id})

        product_with_id = list(Merger_DB['Виски'].find({'product_id': {'$exists': True}}))
        
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            Merger_DB['Виски'].update({'_id': i['_id']}, {'$unset': {'in_productData': 1}}, upsert=True)

        # Saving data to files
        whiskey_file = list(Merger_DB['Виски'].find())
        productData_file = list(Merger_DB['productData'].find())
        write_file('productData.json', productData_file)
        write_file('whiskey.json', whiskey_file)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_whiskey')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = Merger_DB['productData'].count_documents({'section': 'Виски'})

    return render_template('finished_whiskey.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/naming_champagne', methods=['GET', 'POST'])
def naming_champagne():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['del_list'].update({'_id': 'champagne_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    show_group = None
    champagne = list(Merger_DB['Шампанское и игристое вино'].find())

    group_id = numpy.unique(
        [i['product_id'] for i in champagne if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in champagne if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]
    
    if 'saving' in request.form:

        champagne = list(Merger_DB['Шампанское и игристое вино'].find())

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'champagne_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        for i in del_list:
            del_product = [k for k in champagne if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                Merger_DB['Шампанское и игристое вино'].update({'_id': del_product[0]['_id']}, {'$set': del_product[0]})
                Merger_DB['Шампанское и игристое вино'].update({'_id': del_product[0]['_id']}, {'$unset': {'product_id': 1}})

        Merger_DB['del_list'].update({'_id': 'champagne_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)
    
        product_dict = dict()
        fortress = request.form['fortress']
        product_dict['features'] = {}
        product_dict['features']['Крепость'] = None
        product_dict['images'] = {}
        product_dict['description'] = ''
        product_dict['section'] = 'Шампанское и игристое вино'
        product_dict['id'] = request.form['group_id']
        product_dict['name'] = request.form['title']
        if fortress:
            product_dict['features']['Крепость'] = float(fortress) if '.' in fortress else int(fortress)
        product_dict['features']['Страна'] = request.form['country']
        product_dict['features']['Бренд'] = request.form['brand']
        product_dict['features']['Тип'] = request.form['type']
        product_dict['features']['Цвет'] = request.form['color']
        product_dict['features']['Сахар'] = request.form['sugar']
    
        if product_dict['name'] and product_dict['features']['Крепость'] and product_dict['features']['Страна'] and product_dict['features']['Бренд'] and product_dict['features']['Тип'] and product_dict['features']['Цвет'] and product_dict['features']['Сахар']:
            champagne = list(Merger_DB['Шампанское и игристое вино'].find())

            products = [i for i in champagne if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in champagne if i['link'] in product_dict['links']][0]

            Merger_DB['productData'].update({'_id': product_dict['id']}, {'$set': product_dict}, upsert=True)

            for i in champagne:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        i['in_productData'] = True
                        Merger_DB['Шампанское и игристое вино'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    
            # saving data to files
            champagne = list(Merger_DB['Шампанское и игристое вино'].find())
            write_file('champagne.json', champagne)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            flash('Операция проведена успешно', 'success')
            return redirect('/naming_champagne')
        else:
            # saving data to files
            champagne = list(Merger_DB['Шампанское и игристое вино'].find())
            write_file('champagne.json', champagne)

            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_champagne')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'champagne_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        Merger_DB['del_list'].update({'_id': 'champagne_del_list'}, {'$set': {ip_address: del_list}}, upsert=True)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups) - 1:
                    show_group = [groups[groups.index(i) + 1]]
                    break
                else:
                    show_group = [groups[-1]]

        Merger_DB['del_list'].update({'_id': 'champagne_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        Merger_DB['del_list'].update({'_id': 'champagne_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    # число неготовых групп
    undone = len(groups)

    return render_template('naming_champagne.html', groups=show_group, undone=undone)


@app.route('/naming_cognac', methods=['GET', 'POST'])
def naming_cognac():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['del_list'].update({'_id': 'cognac_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    show_group = None
    cognac = list(Merger_DB['Коньяк'].find())

    group_id = numpy.unique([i['product_id'] for i in cognac if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in cognac if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]

    if 'saving' in request.form:

        cognac = list(Merger_DB['Коньяк'].find())

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'cognac_del_list'}, {ip_address: {'$exists': True}}]}))

        if del_list:
            del_list = del_list[0][ip_address]
        for i in del_list:
            del_product = [k for k in cognac if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                Merger_DB['Коньяк'].update({'_id': del_product[0]['_id']}, {'$set': del_product[0]})
                Merger_DB['Коньяк'].update({'_id': del_product[0]['_id']}, {'$unset': {'product_id': 1}})

        Merger_DB['del_list'].update({'_id': 'cognac_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

        product_dict = dict()
        exposure = request.form['exposure']
        fortress = request.form['fortress']
        product_dict['features'] = {}
        product_dict['features']['Крепость'] = None
        product_dict['features']['Выдержка'] = None
        if exposure and fortress:
            product_dict['features']['Крепость'] = float(fortress) if '.' in fortress else int(fortress)
            product_dict['features']['Выдержка'] = float(exposure) if '.' in exposure else int(exposure)
        product_dict['images'] = {}
        product_dict['description'] = ''
        product_dict['section'] = 'Коньяк'
        product_dict['id'] = request.form['group_id']
        product_dict['name'] = request.form['title']
        product_dict['features']['Страна'] = request.form['country']
        product_dict['features']['Бренд'] = request.form['brand']
        product_dict['features']['Класс'] = request.form['type']
        if product_dict['name'] and product_dict['features']['Страна'] and product_dict['features']['Бренд'] and product_dict['features']['Класс'] and product_dict['features']['Крепость'] and product_dict['features']['Выдержка']:
            cognac = list(Merger_DB['Коньяк'].find())

            products = [i for i in cognac if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in cognac if i['link'] in product_dict['links']][0]

            Merger_DB['productData'].update({'_id': product_dict['id']}, {'$set': product_dict}, upsert=True)

            for i in cognac:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        i['in_productData'] = True
                        Merger_DB['Коньяк'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            # saving data to files
            cognac = list(Merger_DB['Коньяк'].find())
            write_file('cognac.json', cognac)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            flash('Операция проведена успешно', category='success')
            return redirect('/naming_cognac')
        else:
            # saving data to files
            cognac = list(Merger_DB['Коньяк'].find())
            write_file('cognac.json', cognac)

            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_cognac')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'cognac_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        Merger_DB['del_list'].update({'_id': 'cognac_del_list'}, {'$set': {ip_address: del_list}}, upsert=True)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups) - 1:
                    show_group = [groups[groups.index(i) + 1]]
                    break
                else:
                    show_group = [groups[-1]]

        Merger_DB['del_list'].update({'_id': 'cognac_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        Merger_DB['del_list'].update({'_id': 'cognac_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    # число неготовых групп
    undone = len(groups)

    return render_template('naming_cognac.html', groups=show_group, undone=undone)


@app.route('/naming_vodka', methods=['GET', 'POST'])
def naming_vodka():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['del_list'].update({'_id': 'vodka_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    show_group = None
    vodka = list(Merger_DB['Водка'].find())

    group_id = numpy.unique([i['product_id'] for i in vodka if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in vodka if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]
    
    if 'saving' in request.form:

        vodka = list(Merger_DB['Водка'].find())

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'vodka_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        for i in del_list:
            del_product = [k for k in vodka if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                # vodka[vodka.index([n for n in vodka if n['link'] == i][0])] = del_product[0]
                Merger_DB['Водка'].update({'_id': del_product[0]['_id']}, {'$set': del_product[0]})
                Merger_DB['Водка'].update({'_id': del_product[0]['_id']}, {'$unset': {'product_id': 1}})

        Merger_DB['del_list'].update({'_id': 'vodka_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

        product_dict = dict()
        fortress = request.form['fortress']
        product_dict['features'] = {}
        product_dict['features']['Крепость'] = None
        if fortress:
            product_dict['features']['Крепость'] = float(fortress) if '.' in fortress else int(fortress)
        product_dict['images'] = {}
        product_dict['description'] = ''
        product_dict['section'] = 'Водка'
        product_dict['id'] = request.form['group_id']
        product_dict['name'] = request.form['title']
        product_dict['features']['Страна'] = request.form['country']
        product_dict['features']['Бренд'] = request.form['brand']
        product_dict['features']['Тип'] = request.form['type']
        if product_dict['name'] and product_dict['features']['Страна'] and product_dict['features']['Бренд'] and product_dict['features']['Тип'] and product_dict['features']['Крепость']:
            vodka = list(Merger_DB['Водка'].find())

            products = [i for i in vodka if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in vodka if i['link'] in product_dict['links']][0]

            Merger_DB['productData'].update({'_id': product_dict['id']}, {'$set': product_dict}, upsert=True)

            for i in vodka:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        i['in_productData'] = True
                        Merger_DB['Водка'].update({'_id': i['_id']}, {'$set': i}, upsert=True)
    
            # saving data to files
            vodka = list(Merger_DB['Водка'].find())
            write_file('vodka.json', vodka)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)
    
            flash('Операция проведена успешно', category='success')
            return redirect('/naming_vodka')
        else:

            # saving data to files
            vodka = list(Merger_DB['Водка'].find())
            write_file('vodka.json', vodka)

            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_vodka')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'vodka_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        Merger_DB['del_list'].update({'_id': 'vodka_del_list'}, {'$set': {ip_address: del_list}}, upsert=True)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        Merger_DB['del_list'].update({'_id': 'vodka_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        Merger_DB['del_list'].update({'_id': 'vodka_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    # число неготовых групп
    undone = len(groups)

    return render_template('naming_vodka.html', groups=show_group, undone=undone)


@app.route('/naming_whiskey', methods=['GET', 'POST'])
def naming_whiskey():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    show_group = None
    whiskey = list(Merger_DB['Виски'].find())

    group_id = numpy.unique([i['product_id'] for i in whiskey if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in whiskey if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]
    
    if 'saving' in request.form:

        whiskey = list(Merger_DB['Виски'].find())

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'whiskey_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        for i in del_list:
            del_product = [k for k in whiskey if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                Merger_DB['Виски'].update({'_id': del_product[0]['_id']}, {'$set': del_product[0]})
                Merger_DB['Виски'].update({'_id': del_product[0]['_id']}, {'$unset': {'product_id': 1}})

        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

        product_dict = dict()
        exposure = request.form['exposure']
        fortress = request.form['fortress']
        product_dict['features'] = {}
        product_dict['features']['Крепость'] = None
        product_dict['features']['Выдержка'] = None
        if exposure and fortress:
            product_dict['features']['Крепость'] = float(fortress) if '.' in fortress else int(fortress)
            product_dict['features']['Выдержка'] = float(exposure) if '.' in exposure else int(exposure)
        product_dict['images'] = {}
        product_dict['description'] = ''
        product_dict['section'] = 'Виски'
        product_dict['id'] = request.form['group_id']
        product_dict['name'] = request.form['title']
        product_dict['features']['Страна'] = request.form['country']
        product_dict['features']['Бренд'] = request.form['brand']
        product_dict['features']['Тип'] = request.form['type']
        if product_dict['name'] and product_dict['features']['Страна'] and product_dict['features']['Бренд'] and product_dict['features']['Тип'] and product_dict['features']['Выдержка'] and product_dict['features']['Крепость']:
            whiskey = list(Merger_DB['Виски'].find())

            products = [i for i in whiskey if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in whiskey if i['link'] in product_dict['links'] and 'image' in i.keys()][0]

            Merger_DB['productData'].update({'_id': product_dict['id']}, {'$set': product_dict}, upsert=True)
    
            for i in whiskey:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        # ind = whiskey.index(i)
                        i['in_productData'] = True
                        # whiskey[ind] = i
                        Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            # saving data to files
            whiskey = list(Merger_DB['Виски'].find())
            write_file('whiskey.json', whiskey)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)
    
            flash('Операция проведена успешно', category='success')
            return redirect('/naming_whiskey')
        else:
            # saving data to files
            whiskey = list(Merger_DB['Виски'].find())
            write_file('whiskey.json', whiskey)

            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_whiskey')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'whiskey_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$set': {ip_address: del_list}}, upsert=True)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        
    # число неготовых групп
    undone = len(groups)

    return render_template('naming_whiskey.html', groups=show_group, undone=undone)


@app.route('/grouping_champagne/', methods=['GET', 'POST'])
def grouping_champagne():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    search = ''
    result_list = []

    champagne = list(Merger_DB['Шампанское и игристое вино'].find())

    skip_list = list(Merger_DB['skip_list'].find({'_id': 'champagne_skip_list'}))
    if skip_list:
        skip_list = skip_list[0]['skip_list']

    main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            Merger_DB['skip_list'].update({'_id': 'champagne_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if "index" in request.form:
        link = request.form['index']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'skip' in request.form:

        Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        skip_list = list(Merger_DB['skip_list'].find({'_id': 'champagne_skip_list'}))
        if skip_list:
            skip_list = skip_list[0]['skip_list']

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        Merger_DB['skip_list'].update({'_id': 'champagne_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in champagne if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            return redirect('/grouping_champagne')

        elif len(match) == 1:

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

            product_id = match[0]

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            for i in link_list:
                drink = [k for k in champagne if k['link'] == i][0]
                ind = champagne.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in champagne[ind].keys()):
                    drink['id'] = take_article()
                Merger_DB['Шампанское и игристое вино'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

            champagne = list(Merger_DB['Шампанское и игристое вино'].find())
            main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = list(Merger_DB['skip_list'].find({'_id': 'champagne_skip_list'}))
                if skip_list:
                    skip_list = skip_list[0]['skip_list']

                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in champagne if
                                  i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    Merger_DB['skip_list'].update({'_id': 'champagne_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'champagne_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            productData = list(Merger_DB['productData'].find({'section': 'Шампанское и игристое вино'}))

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                Merger_DB['productData'].update({'_id': item_in_PD[0]['id']}, {'$set': item_in_PD[0]}, upsert=True)

                champagne = list(Merger_DB['Шампанское и игристое вино'].find())

                need_change = [i for i in champagne if i['link'] in link_list]
                for i in need_change:
                    i['in_productData'] = True
                    Merger_DB['Шампанское и игристое вино'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            champagne = list(Merger_DB['Шампанское и игристое вино'].find())
            write_file('champagne.json', champagne)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            return redirect('/champagne_grouping_prove')
        else:
            if main_drink:

                link_list.append(main_drink['link'])

                product_id = take_article()

                for i in link_list:
                    drink = [k for k in champagne if k['link'] == i][0]
                    ind = champagne.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not ('id' in champagne[ind].keys()):
                        drink['id'] = take_article()
                    Merger_DB['Шампанское и игристое вино'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

                Merger_DB['link_list'].update({'_id': 'champagne_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

                champagne = list(Merger_DB['Шампанское и игристое вино'].find())

                main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = list(Merger_DB['skip_list'].find({'_id': 'champagne_skip_list'}))
                    if skip_list:
                        skip_list = skip_list[0]['skip_list']

                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        Merger_DB['skip_list'].update({'_id': 'champagne_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            # saving data to files
            champagne = list(Merger_DB['Шампанское и игристое вино'].find())
            write_file('champagne.json', champagne)

            return redirect('/champagne_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in champagne if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    # число несгруппированных напитков
    undone = Merger_DB['Шампанское и игристое вино'].count_documents({'identified': False})

    return render_template('grouping_champagne.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


@app.route('/grouping_cognac/', methods=['GET', 'POST'])
def grouping_cognac():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    search = ''
    result_list = []

    cognac = list(Merger_DB['Коньяк'].find())

    skip_list = list(Merger_DB['skip_list'].find({'_id': 'cognac_skip_list'}))
    if skip_list:
        skip_list = skip_list[0]['skip_list']

    main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            Merger_DB['skip_list'].update({'_id': 'cognac_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if "index" in request.form:
        link = request.form['index']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'skip' in request.form:

        Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        skip_list = list(Merger_DB['skip_list'].find({'_id': 'cognac_skip_list'}))
        if skip_list:
            skip_list = skip_list[0]['skip_list']

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        Merger_DB['skip_list'].update({'_id': 'cognac_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in cognac if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            return redirect('/grouping_cognac')

        elif len(match) == 1:

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

            product_id = match[0]

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            for i in link_list:
                drink = [k for k in cognac if k['link'] == i][0]
                ind = cognac.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in cognac[ind].keys()):
                    drink['id'] = take_article()
                Merger_DB['Коньяк'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

            cognac = list(Merger_DB['Коньяк'].find())
            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = list(Merger_DB['skip_list'].find({'_id': 'cognac_skip_list'}))
                if skip_list:
                    skip_list = skip_list[0]['skip_list']

                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    Merger_DB['skip_list'].update({'_id': 'cognac_skip_list'}, {'$set': {'skip_list': skip_list}},
                                                  upsert=True)

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'cognac_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            productData = list(Merger_DB['productData'].find({'section': 'Коньяк'}))

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                Merger_DB['productData'].update({'_id': item_in_PD[0]['id']}, {'$set': item_in_PD[0]}, upsert=True)

                cognac = list(Merger_DB['Коньяк'].find())

                need_change = [i for i in cognac if i['link'] in link_list]
                for i in need_change:
                    i['in_productData'] = True
                    Merger_DB['Коньяк'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            # saving data to files
            cognac = list(Merger_DB['Коньяк'].find())
            write_file('cognac.json', cognac)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            return redirect('/cognac_grouping_prove')
        else:
            if main_drink:

                link_list.append(main_drink['link'])

                product_id = take_article()

                for i in link_list:
                    drink = [k for k in cognac if k['link'] == i][0]
                    ind = cognac.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not ('id' in cognac[ind].keys()):
                        drink['id'] = take_article()
                    Merger_DB['Коньяк'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

                Merger_DB['link_list'].update({'_id': 'cognac_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

                cognac = list(Merger_DB['Коньяк'].find())

                main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = list(Merger_DB['skip_list'].find({'_id': 'cognac_skip_list'}))
                    if skip_list:
                        skip_list = skip_list[0]['skip_list']

                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        Merger_DB['skip_list'].update({'_id': 'cognac_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            # saving data to files
            cognac = list(Merger_DB['Коньяк'].find())
            write_file('cognac.json', cognac)

            return redirect('/cognac_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in cognac if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    # число несгруппированных напитков
    undone = Merger_DB['Коньяк'].count_documents({'identified': False})

    return render_template('grouping_cognac.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


@app.route('/grouping_vodka/', methods=['GET', 'POST'])
def grouping_vodka():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    search = ''
    result_list = []

    vodka = list(Merger_DB['Водка'].find())

    skip_list = list(Merger_DB['skip_list'].find({'_id': 'vodka_skip_list'}))
    if skip_list:
        skip_list = skip_list[0]['skip_list']

    main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            Merger_DB['skip_list'].update({'_id': 'vodka_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if "index" in request.form:
        link = request.form['index']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'skip' in request.form:

        Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

        skip_list = list(Merger_DB['skip_list'].find({'_id': 'vodka_skip_list'}))
        if skip_list:
            skip_list = skip_list[0]['skip_list']

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        Merger_DB['skip_list'].update({'_id': 'vodka_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in vodka if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            return redirect('/grouping_vodka')

        elif len(match) == 1:

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

            product_id = match[0]

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            for i in link_list:
                drink = [k for k in vodka if k['link'] == i][0]
                ind = vodka.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in vodka[ind].keys()):
                    drink['id'] = take_article()
                Merger_DB['Водка'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

            vodka = list(Merger_DB['Водка'].find())

            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = list(Merger_DB['skip_list'].find({'_id': 'vodka_skip_list'}))
                if skip_list:
                    skip_list = skip_list[0]['skip_list']
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    Merger_DB['skip_list'].update({'_id': 'vodka_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'vodka_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            productData = list(Merger_DB['productData'].find({'section': 'Водка'}))

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                Merger_DB['productData'].update({'_id': item_in_PD[0]['id']}, {'$set': item_in_PD[0]}, upsert=True)

                vodka = list(Merger_DB['Водка'].find())

                need_change = [i for i in vodka if i['link'] in link_list]
                for i in need_change:
                    i['in_productData'] = True
                    Merger_DB['Водка'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            # saving data to files
            vodka = list(Merger_DB['Водка'].find())
            write_file('vodka.json', vodka)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            return redirect('/vodka_grouping_prove')
        else:
            if main_drink:

                link_list.append(main_drink['link'])

                product_id = take_article()

                write_file('vodka_link_list.json', [])

                for i in link_list:
                    drink = [k for k in vodka if k['link'] == i][0]
                    ind = vodka.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not('id' in vodka[ind].keys()):
                        drink['id'] = take_article()
                    Merger_DB['Водка'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

                Merger_DB['link_list'].update({'_id': 'vodka_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

                vodka = list(Merger_DB['Водка'].find())

                main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = list(Merger_DB['skip_list'].find({'_id': 'vodka_skip_list'}))
                    if skip_list:
                        skip_list = skip_list[0]['skip_list']
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        Merger_DB['skip_list'].update({'_id': 'vodka_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            # saving data to files
            vodka = list(Merger_DB['Водка'].find())
            write_file('vodka.json', vodka)

            return redirect('/vodka_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in vodka if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]
        
    # число несгруппированных напитков 
    undone = Merger_DB['Водка'].count_documents({'identified': False})

    return render_template('grouping_vodka.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


@app.route('/grouping_whiskey/', methods=['GET', 'POST'])
def grouping_whiskey():

    # update_data = read_file('whiskey_update.json')
    # if update_data:
    #     for i in update_data:
    #         Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    search = ''
    result_list = []

    whiskey = list(Merger_DB['Виски'].find())

    skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
    if skip_list:
        skip_list = skip_list[0]['skip_list']

    main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if "index" in request.form:
        link = request.form['index']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'skip' in request.form:

        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
        if skip_list:
            skip_list = skip_list[0]['skip_list']

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in whiskey if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            return redirect('/grouping_whiskey')

        elif len(match) == 1:

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

            product_id = match[0]

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            for i in link_list:
                drink = [k for k in whiskey if k['link'] == i][0]
                ind = whiskey.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in whiskey[ind].keys()):
                    drink['id'] = take_article()
                Merger_DB['Виски'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

            whiskey = list(Merger_DB['Виски'].find())
            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
                if skip_list:
                    skip_list = skip_list[0]['skip_list']

                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            productData = list(Merger_DB['productData'].find({'section': 'Виски'}))

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                Merger_DB['productData'].update({'_id': item_in_PD[0]['id']}, {'$set': item_in_PD[0]}, upsert=True)

                whiskey = list(Merger_DB['Виски'].find())

                need_change = [i for i in whiskey if i['link'] in link_list]
                for i in need_change:
                    i['in_productData'] = True
                    Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            # saving data to files
            whiskey = list(Merger_DB['Виски'].find())
            write_file('whiskey.json', whiskey)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            return redirect('/whiskey_grouping_prove')
        else:
            if main_drink:

                link_list.append(main_drink['link'])

                product_id = take_article()

                for i in link_list:
                    drink = [k for k in whiskey if k['link'] == i][0]
                    ind = whiskey.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not('id' in whiskey[ind].keys()):
                        drink['id'] = take_article()
                    Merger_DB['Виски'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

                Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

                whiskey = list(Merger_DB['Виски'].find())

                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
                    if skip_list:
                        skip_list = skip_list[0]['skip_list']

                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            # saving data to files
            whiskey = list(Merger_DB['Виски'].find())
            write_file('whiskey.json', whiskey)

            return redirect('/whiskey_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in whiskey if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]
        
    # число несгруппированных напитков
    undone = Merger_DB['Виски'].count_documents({'identified': False})

    return render_template('grouping_whiskey.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


def read_file(file_name):
    with open(file_name) as f:
        file = f.read()
        file = json.loads(file)
        f.close()
    return file


# def read_file(file_name):
#     new_name = file_name[:file_name.index('.json')] + '_dont_touch.json'
#     start_time = time.time()
#     while True:
#         if time.time() - start_time > 5:
#             os.rename(new_name, file_name)
#         try:
#             os.rename(file_name, new_name)
#             with open(new_name) as f:
#                 file = f.read()
#                 file = json.loads(file)
#                 f.close()
#             os.rename(new_name, file_name)
#             return file
#         except:
#             time.sleep(0.5)


def write_file(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()
    return


# def write_file(file_name, data):
#     new_name = file_name[:file_name.index('.json')] + '_dont_touch.json'
#     os.rename(file_name, new_name)
#     with open(new_name, 'w') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#         f.close()
#     while True:
#         try:
#             with open(new_name) as f:
#                 file = f.read()
#                 file = json.loads(file)
#                 f.close()
#             while True:
#                 if len(file) == len(data):
#                     break
#                 else:
#                     continue
#             break
#         except:
#             time.sleep(0.5)
#     os.rename(new_name, file_name)
#     return


# def take_article():
#     with open('articles.txt', 'r') as f:
#         doc = f.read()
#         num = doc.split('\n')
#         del num[-1]
#         article = num[-1]

#     with open('articles.txt', 'w') as f:
#         doc = doc.replace(article + '\n', '')
#         f.write(doc)
#         f.close()

#     return article


def take_article():
    
    while True:
        try:
            os.rename('articles.txt', 'articles_dont_touch.txt')
            with open('articles_dont_touch.txt', 'r') as f:
                doc = f.read()
                num = doc.split('\n')
                del num[-1]
                article = num[-1]
                f.close()

            with open('articles_dont_touch.txt', 'w') as f:
                doc = doc.replace(article + '\n', '')
                f.write(doc)
                f.close()

            os.rename('articles_dont_touch.txt', 'articles.txt')
            return article
        except:
            time.sleep(0.5)


if __name__ == '__main__':
    app.run(debug=True)

    # from waitress import serve
    # serve(app, host="127.0.0.1", port=8080)