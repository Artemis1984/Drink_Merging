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
    show_group = None
    group_titles = None

    champagne = read_file('champagne.json')

    merged_champagne = read_file('productData.json')
    merged_champagne = [i for i in merged_champagne if i['section'] == 'Шампанское и игристое вино']

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

        productData = read_file('productData.json')

        need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        productData.remove(need_to_delete)

        write_file('productData.json', productData)

        champagne = read_file('champagne.json')

        product_with_id = [i for i in champagne if 'product_id' in i.keys()]
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            ind = champagne.index(i)
            i.pop('in_productData')
            champagne[ind] = i

        write_file('champagne.json', champagne)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_champagne')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = len([i for i in read_file('productData.json') if i['section'] == 'Шампанское и игристое вино'])

    return render_template('finished_champagne.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/finished_cognac', methods=['GET', 'POST'])
def finished_cognac():
    show_group = None
    group_titles = None

    cognac = read_file('cognac.json')

    merged_cognac = read_file('productData.json')
    merged_cognac = [i for i in merged_cognac if i['section'] == 'Коньяк']

    productData_links = [i['links'] for i in merged_cognac]
    productData_groups = [i for i in merged_cognac]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in cognac if i['link'] in show_group]]
        group_titles = productData_groups[0]
    
    if 'search' in request.form:
        group_ind = int(request.form['search']) - 1
        if group_ind > len(merged_cognac):
            flash('У вас нет столько групп')
            return redirect('/finished_cognac')
        show_group = productData_links[group_ind]
        show_group = [[i for i in cognac if i['link'] in show_group]]
        group_titles = productData_groups[group_ind]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
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

        productData = read_file('productData.json')

        need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        productData.remove(need_to_delete)

        write_file('productData.json', productData)

        cognac = read_file('cognac.json')

        product_with_id = [i for i in cognac if 'product_id' in i.keys()]
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            ind = cognac.index(i)
            i.pop('in_productData')
            cognac[ind] = i

        write_file('cognac.json', cognac)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_cognac')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = len([i for i in read_file('productData.json') if i['section'] == 'Коньяк'])

    return render_template('finished_cognac.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/finished_vodka', methods=['GET', 'POST'])
def finished_vodka():
    show_group = None
    group_titles = None

    vodka = read_file('vodka.json')

    merged_vodka = read_file('productData.json')
    merged_vodka = [i for i in merged_vodka if i['section'] == 'Водка']

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

        productData = read_file('productData.json')

        need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        productData.remove(need_to_delete)

        write_file('productData.json', productData)

        vodka = read_file('vodka.json')

        product_with_id = [i for i in vodka if 'product_id' in i.keys()]
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            ind = vodka.index(i)
            i.pop('in_productData')
            vodka[ind] = i

        write_file('vodka.json', vodka)

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/finished_vodka')
    
    # Номер группы
    group_num = productData_groups.index(group_titles) + 1
    # число готовых групп
    done = len([i for i in read_file('productData.json') if i['section'] == 'Водка'])

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

    # whiskey = read_file('whiskey.json')
    whiskey = list(Merger_DB['Виски'].find())

    # merged_whiskey = read_file('productData.json')
    # merged_whiskey = [i for i in merged_whiskey if i['section'] == 'Виски']
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

        # productData = read_file('productData.json')

        # need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        # productData.remove(need_to_delete)

        # write_file('productData.json', productData)
        
        need_to_delete = list(Merger_DB['productData'].find({'id': delete_id}))
        if need_to_delete:
            need_to_delete = need_to_delete[0]
        Merger_DB['productData'].delete_one({'_id': need_to_delete['_id']})

        # whiskey = read_file('whiskey.json')

        # product_with_id = [i for i in whiskey if 'product_id' in i.keys()]
        product_with_id = Merger_DB['Виски'].find({'product_id': {'$exists': True}})
        
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
        #     ind = whiskey.index(i)
        #     i.pop('in_productData')
        #     whiskey[ind] = i
            Merger_DB['Виски'].update({'_id': i['_id']}, {'$unset': {'in_productData': 1}}, upsert=True)

        # write_file('whiskey.json', whiskey)
        
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
    # done = len([i for i in read_file('productData.json') if i['section'] == 'Виски'])
    done = Merger_DB['productData'].count_documents({'section': 'Виски'})

    return render_template('finished_whiskey.html', groups=show_group, titles=group_titles, done=done, group_num=group_num)


@app.route('/naming_champagne', methods=['GET', 'POST'])
def naming_champagne():
    if request.method == 'GET':
        write_file('champagne_del_list.json', [])

    show_group = None
    champagne = read_file('champagne.json')

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

        champagne = read_file('champagne.json')
    
        del_list = read_file('champagne_del_list.json')
    
        for i in del_list:
            del_product = [k for k in champagne if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                champagne[champagne.index([n for n in champagne if n['link'] == i][0])] = del_product[0]
    
        write_file('champagne.json', champagne)
    
        write_file('champagne_del_list.json', [])
    
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
            champagne = read_file('champagne.json')
    
            products = [i for i in champagne if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in champagne if i['link'] in product_dict['links']][0]
    
            productData = read_file('productData.json')
    
            productData.append(product_dict)
    
            write_file('productData.json', productData)
    
            champagne = read_file('champagne.json')
    
            for i in champagne:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        ind = champagne.index(i)
                        i['in_productData'] = True
                        champagne[ind] = i
    
            write_file('champagne.json', champagne)
    
            flash('Операция проведена успешно', 'success')
            return redirect('/naming_champagne')
        else:
            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_champagne')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('champagne_del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('champagne_del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups) - 1:
                    show_group = [groups[groups.index(i) + 1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('champagne_del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('champagne_del_list.json', [])

    # число неготовых групп
    undone = len(groups)

    return render_template('naming_champagne.html', groups=show_group, undone=undone)


@app.route('/naming_cognac', methods=['GET', 'POST'])
def naming_cognac():

    if request.method == 'GET':
        write_file('cognac_del_list.json', [])

    show_group = None
    cognac = read_file('cognac.json')

    group_id = numpy.unique([i['product_id'] for i in cognac if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in cognac if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]
    
    if 'saving' in request.form:
        
        cognac = read_file('cognac.json')
    
        del_list = read_file('cognac_del_list.json')
    
        for i in del_list:
            del_product = [k for k in cognac if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                cognac[cognac.index([n for n in cognac if n['link'] == i][0])] = del_product[0]
    
        write_file('cognac.json', cognac)
    
        write_file('cognac_del_list.json', [])
    
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
            cognac = read_file('cognac.json')
    
            products = [i for i in cognac if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in cognac if i['link'] in product_dict['links']][0]
    
            productData = read_file('productData.json')
    
            productData.append(product_dict)
    
            write_file('productData.json', productData)
    
            cognac = read_file('cognac.json')
    
            for i in cognac:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        ind = cognac.index(i)
                        i['in_productData'] = True
                        cognac[ind] = i
    
            write_file('cognac.json', cognac)
    
            flash('Операция проведена успешно', category='success')
            return redirect('/naming_cognac')
        else:
            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_cognac')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('cognac_del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('cognac_del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('cognac_del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('cognac_del_list.json', [])
        
    # число неготовых групп
    undone = len(groups)

    return render_template('naming_cognac.html', groups=show_group, undone=undone)


@app.route('/naming_vodka', methods=['GET', 'POST'])
def naming_vodka():

    if request.method == 'GET':
        write_file('vodka_del_list.json', [])

    show_group = None
    vodka = read_file('vodka.json')

    group_id = numpy.unique([i['product_id'] for i in vodka if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in vodka if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]
    
    if 'saving' in request.form:

        vodka = read_file('vodka.json')

        del_list = read_file('vodka_del_list.json')

        for i in del_list:
            del_product = [k for k in vodka if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                vodka[vodka.index([n for n in vodka if n['link'] == i][0])] = del_product[0]

        write_file('vodka.json', vodka)

        write_file('vodka_del_list.json', [])

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
            vodka = read_file('vodka.json')
    
            products = [i for i in vodka if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in vodka if i['link'] in product_dict['links']][0]
    
            productData = read_file('productData.json')
    
            productData.append(product_dict)
    
            write_file('productData.json', productData)
    
            vodka = read_file('vodka.json')
    
            for i in vodka:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        ind = vodka.index(i)
                        i['in_productData'] = True
                        vodka[ind] = i
    
            write_file('vodka.json', vodka)
    
            flash('Операция проведена успешно', category='success')
            return redirect('/naming_vodka')
        else:
            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_vodka')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('vodka_del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('vodka_del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('vodka_del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('vodka_del_list.json', [])
    
    # число неготовых групп
    undone = len(groups)

    return render_template('naming_vodka.html', groups=show_group, undone=undone)


@app.route('/naming_whiskey', methods=['GET', 'POST'])
def naming_whiskey():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        # write_file('whiskey_del_list.json', [])
        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    show_group = None
    # whiskey = read_file('whiskey.json')
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

        # whiskey = read_file('whiskey.json')
        whiskey = list(Merger_DB['Виски'].find())

        # del_list = read_file('whiskey_del_list.json')
        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'whiskey_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]
        # print(del_list)
        for i in del_list:
            del_product = [k for k in whiskey if k['link'] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                Merger_DB['Виски'].update({'_id': del_product[0]['_id']}, {'$set': del_product[0]})
                Merger_DB['Виски'].update({'_id': del_product[0]['_id']}, {'$unset': {'product_id': 1}})
                # whiskey[whiskey.index([n for n in whiskey if n['link'] == i][0])] = del_product[0]
                # print(list(Merger_DB['Виски'].find({'_id': del_product[0]['_id']})))
        # write_file('whiskey.json', whiskey)

        # write_file('whiskey_del_list.json', [])
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
            # whiskey = read_file('whiskey.json')
            whiskey = list(Merger_DB['Виски'].find())

            products = [i for i in whiskey if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'] for i in whiskey if i['link'] in product_dict['links'] and 'image' in i.keys()][0]
    
            # productData = read_file('productData.json')
    
            # productData.append(product_dict)
    
            # write_file('productData.json', productData)

            Merger_DB['productData'].update({'_id': product_dict['id']}, {'$set': product_dict}, upsert=True)
    
            # whiskey = read_file('whiskey.json')
    
            for i in whiskey:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        # ind = whiskey.index(i)
                        i['in_productData'] = True
                        # whiskey[ind] = i
                        Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            # write_file('whiskey.json', whiskey)

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
            # productData = list(Merger_DB['productData'].find())
            # write_file('productData.json', productData)

            flash('Нужно заполнить все поля', category='error')
            return redirect('/naming_whiskey')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        # del_list = read_file('whiskey_del_list.json')
        del_list = list(Merger_DB['del_list'].find({'$and': [{'_id': 'whiskey_del_list'}, {ip_address: {'$exists': True}}]}))
        if del_list:
            del_list = del_list[0][ip_address]

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        # write_file('whiskey_del_list.json', del_list)
        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$set': {ip_address: del_list}}, upsert=True)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        # write_file('whiskey_del_list.json', [])
        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        # write_file('whiskey_del_list.json', [])
        Merger_DB['del_list'].update({'_id': 'whiskey_del_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        
    # число неготовых групп
    undone = len(groups)

    return render_template('naming_whiskey.html', groups=show_group, undone=undone)


@app.route('/grouping_champagne/', methods=['GET', 'POST'])
def grouping_champagne():
    if request.method == 'GET':
        write_file('champagne_link_list.json', [])

    search = ''
    result_list = []

    champagne = read_file('champagne.json')

    skip_list = read_file('champagne_skip_list.json')

    main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('champagne_skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('champagne_link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('champagne_link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('champagne_link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('champagne_link_list.json', link_list)

    if 'skip' in request.form:

        write_file('champagne_link_list.json', [])
        skip_list = read_file('champagne_skip_list.json')

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

        write_file('champagne_skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in champagne if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('champagne_link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('champagne_link_list.json', [])

            return redirect('/grouping_champagne')

        elif len(match) == 1:

            link_list = read_file('champagne_link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            write_file('champagne_link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('champagne_link_list.json')

            for i in link_list:
                drink = [k for k in champagne if k['link'] == i][0]
                ind = champagne.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in champagne[ind].keys()):
                    drink['id'] = take_article()
                champagne[ind] = drink
            if champagne:
                write_file('champagne.json', champagne)

            main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('champagne_skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in champagne if
                                  i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('champagne_skip_list.json', skip_list)

            link_list = read_file('champagne_link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                    productData[item_in_PD_index] = item_in_PD[0]

                write_file('productData.json', productData)

                champagne = read_file('champagne.json')

                need_change = [i for i in champagne if i['link'] in link_list]
                for i in need_change:
                    ind = champagne.index(i)
                    i['in_productData'] = True
                    champagne[ind] = i

            write_file('champagne.json', champagne)

            write_file('champagne_link_list.json', [])

            return redirect('/champagne_grouping_prove')
        else:
            if main_drink:

                write_file('champagne_link_list.json', [])

                link_list.append(main_drink['link'])

                write_file('champagne_link_list.json', link_list)

                product_id = take_article()

                write_file('champagne_link_list.json', [])

                for i in link_list:
                    drink = [k for k in champagne if k['link'] == i][0]
                    ind = champagne.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not ('id' in champagne[ind].keys()):
                        drink['id'] = take_article()
                    champagne[ind] = drink

                write_file('champagne.json', champagne)

                write_file('champagne_link_list.json', [])

                main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('champagne_skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in champagne if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('champagne_skip_list.json', skip_list)

            return redirect('/champagne_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in champagne if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    # число несгруппированных напитков
    undone = len([i for i in read_file('champagne.json') if not i['identified']])

    return render_template('grouping_champagne.html', main_drink=main_drink, products=result_list, groups=groups,
                           undone=undone)


@app.route('/grouping_cognac/', methods=['GET', 'POST'])
def grouping_cognac():

    if request.method == 'GET':
        write_file('cognac_link_list.json', [])

    search = ''
    result_list = []

    cognac = read_file('cognac.json')

    skip_list = read_file('cognac_skip_list.json')

    main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('cognac_skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('cognac_link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('cognac_link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('cognac_link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('cognac_link_list.json', link_list)

    if 'skip' in request.form:

        write_file('cognac_link_list.json', [])
        skip_list = read_file('cognac_skip_list.json')

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

        write_file('cognac_skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in cognac if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('cognac_link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('cognac_link_list.json', [])

            return redirect('/grouping_cognac')

        elif len(match) == 1:

            link_list = read_file('cognac_link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            write_file('cognac_link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('cognac_link_list.json')

            for i in link_list:
                drink = [k for k in cognac if k['link'] == i][0]
                ind = cognac.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in cognac[ind].keys()):
                    drink['id'] = take_article()
                cognac[ind] = drink
            if cognac:

                write_file('cognac.json', cognac)

            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('cognac_skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in cognac if
                                    i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('cognac_skip_list.json', skip_list)

            link_list = read_file('cognac_link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                    productData[item_in_PD_index] = item_in_PD[0]

                write_file('productData.json', productData)

                cognac = read_file('cognac.json')

                need_change = [i for i in cognac if i['link'] in link_list]
                for i in need_change:
                    ind = cognac.index(i)
                    i['in_productData'] = True
                    cognac[ind] = i

            write_file('cognac.json', cognac)

            write_file('cognac_link_list.json', [])

            return redirect('/cognac_grouping_prove')
        else:
            if main_drink:

                write_file('cognac_link_list.json', [])

                link_list.append(main_drink['link'])

                write_file('cognac_link_list.json', link_list)

                product_id = take_article()

                write_file('cognac_link_list.json', [])

                for i in link_list:
                    drink = [k for k in cognac if k['link'] == i][0]
                    ind = cognac.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not('id' in cognac[ind].keys()):
                        drink['id'] = take_article()
                    cognac[ind] = drink

                write_file('cognac.json', cognac)

                write_file('cognac_link_list.json', [])

                main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('cognac_skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in cognac if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('cognac_skip_list.json', skip_list)

            return redirect('/cognac_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in cognac if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]
    
    # число несгруппированных напитков 
    undone = len([i for i in read_file('cognac.json') if not i['identified']])

    return render_template('grouping_cognac.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


@app.route('/grouping_vodka/', methods=['GET', 'POST'])
def grouping_vodka():

    if request.method == 'GET':
        write_file('vodka_link_list.json', [])

    search = ''
    result_list = []

    vodka = read_file('vodka.json')

    skip_list = read_file('vodka_skip_list.json')

    main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('vodka_skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('vodka_link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('vodka_link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('vodka_link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('vodka_link_list.json', link_list)

    if 'skip' in request.form:

        write_file('vodka_link_list.json', [])
        skip_list = read_file('vodka_skip_list.json')

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

        write_file('vodka_skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in vodka if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('vodka_link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('vodka_link_list.json', [])

            return redirect('/grouping_vodka')

        elif len(match) == 1:

            link_list = read_file('vodka_link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            write_file('vodka_link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('vodka_link_list.json')

            for i in link_list:
                drink = [k for k in vodka if k['link'] == i][0]
                ind = vodka.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                if not ('id' in vodka[ind].keys()):
                    drink['id'] = take_article()
                vodka[ind] = drink
            if vodka:

                write_file('vodka.json', vodka)

            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('vodka_skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('vodka_skip_list.json', skip_list)

            link_list = read_file('vodka_link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                productData[item_in_PD_index] = item_in_PD[0]

                write_file('productData.json', productData)

                vodka = read_file('vodka.json')

                need_change = [i for i in vodka if i['link'] in link_list]
                for i in need_change:
                    ind = vodka.index(i)
                    i['in_productData'] = True
                    vodka[ind] = i

            write_file('vodka.json', vodka)

            write_file('vodka_link_list.json', [])

            return redirect('/vodka_grouping_prove')
        else:
            if main_drink:

                write_file('vodka_link_list.json', [])

                link_list.append(main_drink['link'])

                write_file('vodka_link_list.json', link_list)

                product_id = take_article()

                write_file('vodka_link_list.json', [])

                for i in link_list:
                    drink = [k for k in vodka if k['link'] == i][0]
                    ind = vodka.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not('id' in vodka[ind].keys()):
                        drink['id'] = take_article()
                    vodka[ind] = drink

                write_file('vodka.json', vodka)

                write_file('vodka_link_list.json', [])

                main_drink = [i for i in vodka if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('vodka_skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('vodka_skip_list.json', skip_list)

            return redirect('/vodka_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in vodka if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]
        
    # число несгруппированных напитков 
    undone = len([i for i in read_file('vodka.json') if not i['identified']])

    return render_template('grouping_vodka.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


@app.route('/grouping_whiskey/', methods=['GET', 'POST'])
def grouping_whiskey():

    ip_address = request.remote_addr.replace('.', '')

    if request.method == 'GET':
        # write_file('whiskey_link_list.json', [])
        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

    search = ''
    result_list = []

    # whiskey = read_file('whiskey.json')
    whiskey = list(Merger_DB['Виски'].find())

    # skip_list = read_file('whiskey_skip_list.json')
    # skip_list = list(Merger_DB['skip_list'].find({ip_address: {'$exists': True}}))
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
            # write_file('whiskey_skip_list.json', skip_list)
            Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if "index" in request.form:
        link = request.form['index']

        # link_list = read_file('whiskey_link_list.json')
        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        # write_file('whiskey_link_list.json', link_list)
        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)


    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        # link_list = read_file('whiskey_link_list.json')
        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        # write_file('whiskey_link_list.json', link_list)
        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

    if 'skip' in request.form:

        # write_file('whiskey_link_list.json', [])
        Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)
        # skip_list = read_file('whiskey_skip_list.json')
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

        # write_file('whiskey_skip_list.json', skip_list)
        Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in whiskey if search.lower() in i['name'].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        # link_list = read_file('whiskey_link_list.json')
        link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
        if link_list:
            link_list = link_list[0][ip_address]

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            # write_file('whiskey_link_list.json', [])
            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            return redirect('/grouping_whiskey')

        elif len(match) == 1:

            # link_list = read_file('whiskey_link_list.json')
            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'])

            # write_file('whiskey_link_list.json', link_list)
            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$set': {ip_address: link_list}}, upsert=True)

            product_id = match[0]

            # link_list = read_file('whiskey_link_list.json')
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
            #     whiskey[ind] = drink
            # if whiskey:
            #
            #     write_file('whiskey.json', whiskey)
            whiskey = list(Merger_DB['Виски'].find())
            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                # skip_list = read_file('whiskey_skip_list.json')
                skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
                if skip_list:
                    skip_list = skip_list[0]['skip_list']

                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    # write_file('whiskey_skip_list.json', skip_list)
                    Merger_DB['skip_list'].update({'_id': 'whiskey_skip_list'}, {'$set': {'skip_list': skip_list}}, upsert=True)

            # link_list = read_file('whiskey_link_list.json')
            link_list = list(Merger_DB['link_list'].find({'$and': [{'_id': 'whiskey_link_list'}, {ip_address: {'$exists': True}}]}))
            if link_list:
                link_list = link_list[0][ip_address]

            # productData = read_file('productData.json')
            productData = list(Merger_DB['productData'].find({'section': 'Виски'}))

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                for i in link_list:
                    item_in_PD[0]['links'].append(i)

                # productData[item_in_PD_index] = item_in_PD[0]
                Merger_DB['productData'].update({'_id': item_in_PD[0]['id']}, {'$set': item_in_PD[0]}, upsert=True)

                # whiskey = read_file('whiskey.json')
                whiskey = list(Merger_DB['Виски'].find())
                # write_file('productData.json', productData)

                need_change = [i for i in whiskey if i['link'] in link_list]
                for i in need_change:
                    # ind = whiskey.index(i)
                    i['in_productData'] = True
                    # whiskey[ind] = i
                    Merger_DB['Виски'].update({'_id': i['_id']}, {'$set': i}, upsert=True)

            # write_file('whiskey.json', whiskey)

            # write_file('whiskey_link_list.json', [])
            Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

            # saving data to files
            whiskey = list(Merger_DB['Виски'].find())
            write_file('whiskey.json', whiskey)
            productData = list(Merger_DB['productData'].find())
            write_file('productData.json', productData)

            return redirect('/whiskey_grouping_prove')
        else:
            if main_drink:

                # write_file('whiskey_link_list.json', [])
                # Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': ip_address}, upsert=True)

                link_list.append(main_drink['link'])

                # write_file('whiskey_link_list.json', link_list)

                product_id = take_article()

                # write_file('whiskey_link_list.json', [])

                for i in link_list:
                    drink = [k for k in whiskey if k['link'] == i][0]
                    ind = whiskey.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    if not('id' in whiskey[ind].keys()):
                        drink['id'] = take_article()
                    # whiskey[ind] = drink
                    Merger_DB['Виски'].update({'_id': drink['_id']}, {'$set': drink}, upsert=True)

                # write_file('whiskey.json', whiskey)

                # write_file('whiskey_link_list.json', [])
                Merger_DB['link_list'].update({'_id': 'whiskey_link_list'}, {'$unset': {ip_address: 1}}, upsert=True)

                whiskey = list(Merger_DB['Виски'].find())

                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    # skip_list = read_file('whiskey_skip_list.json')
                    skip_list = list(Merger_DB['skip_list'].find({'_id': 'whiskey_skip_list'}))
                    if skip_list:
                        skip_list = skip_list[0]['skip_list']

                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        # write_file('whiskey_skip_list.json', skip_list)
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
    # undone = len([i for i in whiskey if not i['identified']])
    undone = Merger_DB['Виски'].count_documents({'identified': False})

    return render_template('grouping_whiskey.html', main_drink=main_drink, products=result_list, groups=groups, undone=undone)


# def read_file(file_name):
#     with open(file_name) as f:
#         file = f.read()
#         file = json.loads(file)
#         f.close()
#     return file


def read_file(file_name):
    new_name = file_name[:file_name.index('.json')] + '_dont_touch.json'
    start_time = time.time()
    while True:
        if time.time() - start_time > 5:
            os.rename(new_name, file_name)
        try:
            os.rename(file_name, new_name)
            with open(new_name) as f:
                file = f.read()
                file = json.loads(file)
                f.close()
            os.rename(new_name, file_name)
            return file
        except:
            time.sleep(0.5)


# def write_file(file_name, data):
#     with open(file_name, 'w') as f:
#         json.dump(data, f, ensure_ascii=False, indent=2)
#         f.close()
#     return


def write_file(file_name, data):
    new_name = file_name[:file_name.index('.json')] + '_dont_touch.json'
    os.rename(file_name, new_name)
    with open(new_name, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.close()
    while True:
        try:
            with open(new_name) as f:
                file = f.read()
                file = json.loads(file)
                f.close()
            while True:
                if len(file) == len(data):
                    break
                else:
                    continue
            break
        except:
            time.sleep(0.5)
    os.rename(new_name, file_name)
    return


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