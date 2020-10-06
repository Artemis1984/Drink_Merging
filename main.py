from flask import Flask, render_template, request, abort, url_for, redirect, flash
import json
import numpy


app = Flask(__name__)
app.config['SECRET_KEY'] = '12091988BernardoProvencanoToto'


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/cognac_grouping_prove')
def cognac_grouping_prove():
    return render_template('cognac_grouping_prove.html')


@app.route('/vodka_grouping_prove')
def vodka_grouping_prove():
    return render_template('vodka_grouping_prove.html')


@app.route('/whiskey_grouping_prove')
def whiskey_grouping_prove():
    return render_template('whiskey_grouping_prove.html')


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

        show_group = [[i for i in cognac if i['link'][0] in show_group]]
        group_titles = productData_groups[0]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in cognac if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in cognac if k['link'][0] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in cognac if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in cognac if k['link'][0] in show_group]]
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

    return render_template('finished_cognac.html', groups=show_group, titles=group_titles)


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

        show_group = [[i for i in vodka if i['link'][0] in show_group]]
        group_titles = productData_groups[0]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in vodka if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in vodka if k['link'][0] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in vodka if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in vodka if k['link'][0] in show_group]]
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

    return render_template('finished_vodka.html', groups=show_group, titles=group_titles)


@app.route('/finished_whiskey', methods=['GET', 'POST'])
def finished_whiskey():
    show_group = None
    group_titles = None

    whiskey = read_file('whiskey.json')

    merged_whiskey = read_file('productData.json')
    merged_whiskey = [i for i in merged_whiskey if i['section'] == 'Виски']

    productData_links = [i['links'] for i in merged_whiskey]
    productData_groups = [i for i in merged_whiskey]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in whiskey if i['link'][0] in show_group]]
        group_titles = productData_groups[0]

    if 'next' in request.form:

        for i in productData_groups:

            if i['id'] == request.form['next']:
                ind = productData_groups.index(i)
                if ind != len(productData_groups)-1:
                    show_group = productData_links[ind + 1]
                    show_group = [[k for k in whiskey if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind + 1]

                    break
                else:
                    show_group = productData_links[-1]
                    show_group = [[k for k in whiskey if k['link'][0] in show_group]]
                    group_titles = productData_groups[-1]

    if 'previous' in request.form:
        for i in productData_groups:

            if i['id'] == request.form['previous']:
                ind = productData_groups.index(i)
                if ind != 0:
                    show_group = productData_links[ind - 1]
                    show_group = [[k for k in whiskey if k['link'][0] in show_group]]
                    group_titles = productData_groups[ind - 1]
                    break
                else:
                    show_group = productData_links[0]
                    show_group = [[k for k in whiskey if k['link'][0] in show_group]]
                    group_titles = productData_groups[0]

    if 'delete_from_finished' in request.form:
        delete_id = request.form['delete_from_finished']

        productData = read_file('productData.json')

        need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        productData.remove(need_to_delete)

        write_file('productData.json', productData)

        whiskey = read_file('whiskey.json')

        product_with_id = [i for i in whiskey if 'product_id' in i.keys()]
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            ind = whiskey.index(i)
            i.pop('in_productData')
            whiskey[ind] = i

        write_file('whiskey.json', whiskey)

        flash('Группа успешно отправлена на повторную обработку')
        # return redirect('/whiskey_grouping_prove')
        return redirect('/finished_whiskey')

    return render_template('finished_whiskey.html', groups=show_group, titles=group_titles)


@app.route('/naming_cognac', methods=['GET', 'POST'])
def naming_cognac():

    if request.method == 'GET':
        write_file('del_list.json', [])

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

        del_list = read_file('del_list.json')

        for i in del_list:
            del_product = [k for k in cognac if k['link'][0] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                cognac[cognac.index([n for n in cognac if n['link'][0] == i][0])] = del_product[0]

        write_file('cognac.json', cognac)

        write_file('del_list.json', [])

        product_dict = dict()
        exposure = request.form['exposure']
        fortress = request.form['fortress']
        if exposure and fortress:
            product_dict['features'] = {}
            product_dict['features']['Крепость'] = int(fortress)
            product_dict['features']['Выдержка'] = int(exposure)
            product_dict['images'] = {}
            product_dict['description'] = ''
            product_dict['section'] = 'Коньяк'
            product_dict['id'] = request.form['group_id']
            product_dict['name'] = request.form['title']
            product_dict['features']['Страна'] = request.form['country']
            product_dict['features']['Бренд'] = request.form['brand']
            product_dict['features']['Класс'] = request.form['type']

            cognac = read_file('cognac.json')

            products = [i for i in cognac if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'][0] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'][0] for i in cognac if i['link'][0] in product_dict['links']][0]

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

        flash('Операция проведена успешно')
        return redirect('/naming_cognac')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('del_list.json', [])

    return render_template('naming_cognac.html', groups=show_group)


@app.route('/naming_vodka', methods=['GET', 'POST'])
def naming_vodka():

    if request.method == 'GET':
        write_file('del_list.json', [])

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

        del_list = read_file('del_list.json')

        for i in del_list:
            del_product = [k for k in vodka if k['link'][0] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                vodka[vodka.index([n for n in vodka if n['link'][0] == i][0])] = del_product[0]

        write_file('vodka.json', vodka)

        write_file('del_list.json', [])

        product_dict = dict()
        # exposure = request.form['exposure']
        fortress = request.form['fortress']
        if fortress:
            product_dict['features'] = {}
            product_dict['features']['Крепость'] = int(fortress)
            # product_dict['features']['Выдержка'] = int(exposure)
            product_dict['images'] = {}
            product_dict['description'] = ''
            product_dict['section'] = 'Водка'
            product_dict['id'] = request.form['group_id']
            product_dict['name'] = request.form['title']
            product_dict['features']['Страна'] = request.form['country']
            product_dict['features']['Бренд'] = request.form['brand']
            product_dict['features']['Тип'] = request.form['type']

            vodka = read_file('vodka.json')

            products = [i for i in vodka if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'][0] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'][0] for i in vodka if i['link'][0] in product_dict['links']][0]

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

        flash('Операция проведена успешно')
        return redirect('/naming_vodka')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('del_list.json', [])

    return render_template('naming_vodka.html', groups=show_group)


@app.route('/naming_whiskey', methods=['GET', 'POST'])
def naming_whiskey():

    if request.method == 'GET':
        write_file('del_list.json', [])

    show_group = None
    whiskey = read_file('whiskey.json')

    group_id = numpy.unique([i['product_id'] for i in whiskey if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in whiskey if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]

    if 'saving' in request.form:

        whiskey = read_file('whiskey.json')

        del_list = read_file('del_list.json')

        for i in del_list:
            del_product = [k for k in whiskey if k['link'][0] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                whiskey[whiskey.index([n for n in whiskey if n['link'][0] == i][0])] = del_product[0]

        write_file('whiskey.json', whiskey)

        write_file('del_list.json', [])

        product_dict = dict()
        exposure = request.form['exposure']
        fortress = request.form['fortress']
        if exposure and fortress:
            product_dict['features'] = {}
            product_dict['features']['Крепость'] = int(fortress)
            product_dict['features']['Выдержка'] = int(exposure)
            product_dict['images'] = {}
            product_dict['description'] = ''
            product_dict['section'] = 'Виски'
            product_dict['id'] = request.form['group_id']
            product_dict['name'] = request.form['title']
            product_dict['features']['Страна'] = request.form['country']
            product_dict['features']['Бренд'] = request.form['brand']
            product_dict['features']['Тип'] = request.form['type']

            whiskey = read_file('whiskey.json')

            products = [i for i in whiskey if 'product_id' in i.keys()]
            product_dict['links'] = [i['link'][0] for i in products if i['product_id'] == product_dict['id']]
            product_dict['images']['default'] = [i['image'][0] for i in whiskey if i['link'][0] in product_dict['links']][0]

            productData = read_file('productData.json')

            productData.append(product_dict)

            write_file('productData.json', productData)

            whiskey = read_file('whiskey.json')

            for i in whiskey:
                if 'product_id' in i.keys():
                    if i['product_id'] == product_dict['id']:
                        ind = whiskey.index(i)
                        i['in_productData'] = True
                        whiskey[ind] = i

            write_file('whiskey.json', whiskey)

        flash('Операция проведена успешно')
        # return redirect('/whiskey_grouping_prove')
        return redirect('/naming_whiskey')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']

        del_list = read_file('del_list.json')

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        write_file('del_list.json', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        write_file('del_list.json', [])

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        write_file('del_list.json', [])

    return render_template('naming_whiskey.html', groups=show_group)


@app.route('/grouping_cognac/', methods=['GET', 'POST'])
def grouping_cognac():

    if request.method == 'GET':
        write_file('link_list.json', [])

    search = ''
    result_list = []

    cognac = read_file('cognac.json')

    skip_list = read_file('skip_list.json')

    main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('link_list.json', link_list)

    if 'skip' in request.form:

        write_file('link_list.json', [])
        skip_list = read_file('skip_list.json')

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        write_file('skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in cognac if search.lower() in i['name'][0].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('link_list.json', [])

            return redirect('/grouping_cognac')

        elif len(match) == 1:

            link_list = read_file('link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'][0])

            write_file('link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('link_list.json')

            for i in link_list:
                drink = [k for k in cognac if k['link'][0] == i][0]
                ind = cognac.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                cognac[ind] = drink
            if cognac:

                write_file('cognac.json', cognac)

            main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in cognac if
                                    i['identified'] is False and not (i['link'][0] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('skip_list.json', skip_list)

            with open('productData.json') as f:

                link_list = read_file('link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                if item_in_PD:
                    for i in link_list:
                        item_in_PD[0]['links'].append(i)

                    productData[item_in_PD_index] = item_in_PD[0]

            write_file('productData.json', productData)

            cognac = read_file('cognac.json')

            need_change = [i for i in cognac if i['link'][0] in link_list]
            for i in need_change:
                ind = cognac.index(i)
                i['in_productData'] = True
                cognac[ind] = i

            write_file('cognac.json', cognac)

            write_file('link_list.json', [])

            return redirect('/cognac_grouping_prove')
        else:
            if main_drink:

                write_file('link_list.json', [])

                link_list.append(main_drink['link'][0])

                write_file('link_list.json', link_list)

                with open('articles.txt', 'r') as f:
                    doc = f.read()
                    num = doc.split('\n')
                    del num[-1]
                    product_id = num[-1]

                write_file('link_list.json', [])

                for i in link_list:
                    drink = [k for k in cognac if k['link'][0] == i][0]
                    ind = cognac.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    cognac[ind] = drink

                write_file('cognac.json', cognac)

                write_file('link_list.json', [])

                main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in cognac if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('skip_list.json', skip_list)

                with open('articles.txt', 'w') as f:
                    doc = doc.replace(product_id + '\n', '')
                    f.write(doc)
                    f.close()

            return redirect('/cognac_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in cognac if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    return render_template('grouping_cognac.html', main_drink=main_drink, products=result_list, groups=groups)


@app.route('/grouping_vodka/', methods=['GET', 'POST'])
def grouping_vodka():

    if request.method == 'GET':
        write_file('link_list.json', [])

    search = ''
    result_list = []

    vodka = read_file('vodka.json')

    skip_list = read_file('skip_list.json')

    main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('link_list.json', link_list)

    if 'skip' in request.form:

        write_file('link_list.json', [])
        skip_list = read_file('skip_list.json')

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        write_file('skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in vodka if search.lower() in i['name'][0].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('link_list.json', [])

            return redirect('/grouping_whiskey')

        elif len(match) == 1:

            link_list = read_file('link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'][0])

            write_file('link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('link_list.json')

            for i in link_list:
                drink = [k for k in vodka if k['link'][0] == i][0]
                ind = vodka.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                vodka[ind] = drink
            if vodka:

                write_file('vodka.json', vodka)

            main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in vodka if
                                    i['identified'] is False and not (i['link'][0] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('skip_list.json', skip_list)

            with open('productData.json') as f:

                link_list = read_file('link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                if item_in_PD:
                    for i in link_list:
                        item_in_PD[0]['links'].append(i)

                    productData[item_in_PD_index] = item_in_PD[0]

            write_file('productData.json', productData)

            vodka = read_file('vodka.json')

            need_change = [i for i in vodka if i['link'][0] in link_list]
            for i in need_change:
                ind = vodka.index(i)
                i['in_productData'] = True
                vodka[ind] = i

            write_file('vodka.json', vodka)

            write_file('link_list.json', [])

            return redirect('/vodka_grouping_prove')
        else:
            if main_drink:

                write_file('link_list.json', [])

                link_list.append(main_drink['link'][0])

                write_file('link_list.json', link_list)

                with open('articles.txt', 'r') as f:
                    doc = f.read()
                    num = doc.split('\n')
                    del num[-1]
                    product_id = num[-1]

                write_file('link_list.json', [])

                for i in link_list:
                    drink = [k for k in vodka if k['link'][0] == i][0]
                    ind = vodka.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    vodka[ind] = drink

                write_file('vodka.json', vodka)

                write_file('link_list.json', [])

                main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in vodka if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('skip_list.json', skip_list)

                with open('articles.txt', 'w') as f:
                    doc = doc.replace(product_id + '\n', '')
                    f.write(doc)
                    f.close()

            return redirect('/vodka_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in vodka if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    return render_template('grouping_vodka.html', main_drink=main_drink, products=result_list, groups=groups)


@app.route('/grouping_whiskey/', methods=['GET', 'POST'])
def grouping_whiskey():

    if request.method == 'GET':
        write_file('link_list.json', [])

    search = ''
    result_list = []

    whiskey = read_file('whiskey.json')

    skip_list = read_file('skip_list.json')

    main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:

            del skip_list[0]
            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            write_file('skip_list.json', skip_list)

    if "index" in request.form:
        link = request.form['index']

        link_list = read_file('link_list.json')

        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        write_file('link_list.json', link_list)

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']

        link_list = read_file('link_list.json')

        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        write_file('link_list.json', link_list)

    if 'skip' in request.form:

        write_file('link_list.json', [])
        skip_list = read_file('skip_list.json')

        if not (request.form['skip'] in skip_list):
            skip_list.append(request.form['skip'])

        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
        if main_drink:
            main_drink = main_drink[0]
        else:
            if skip_list:
                del skip_list[0]
                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]

        write_file('skip_list.json', skip_list)

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in whiskey if search.lower() in i['name'][0].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        link_list = read_file('link_list.json')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')

            write_file('link_list.json', [])

            return redirect('/grouping_whiskey')

        elif len(match) == 1:

            link_list = read_file('link_list.json')

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'][0])

            write_file('link_list.json', link_list)

            product_id = match[0]

            link_list = read_file('link_list.json')

            for i in link_list:
                drink = [k for k in whiskey if k['link'][0] == i][0]
                ind = whiskey.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                whiskey[ind] = drink
            if whiskey:

                write_file('whiskey.json', whiskey)

            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                skip_list = read_file('skip_list.json')
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in whiskey if
                                    i['identified'] is False and not (i['link'][0] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

                    write_file('skip_list.json', skip_list)

            with open('productData.json') as f:

                link_list = read_file('link_list.json')

            productData = read_file('productData.json')

            item_in_PD = [i for i in productData if i['id'] == product_id]
            if item_in_PD:
                item_in_PD_index = productData.index(item_in_PD[0])
                if item_in_PD:
                    for i in link_list:
                        item_in_PD[0]['links'].append(i)

                    productData[item_in_PD_index] = item_in_PD[0]

            write_file('productData.json', productData)

            whiskey = read_file('whiskey.json')

            need_change = [i for i in whiskey if i['link'][0] in link_list]
            for i in need_change:
                ind = whiskey.index(i)
                i['in_productData'] = True
                whiskey[ind] = i

            write_file('whiskey.json', whiskey)

            write_file('link_list.json', [])

            return redirect('/whiskey_grouping_prove')
        else:
            if main_drink:

                write_file('link_list.json', [])

                link_list.append(main_drink['link'][0])

                write_file('link_list.json', link_list)

                with open('articles.txt', 'r') as f:
                    doc = f.read()
                    num = doc.split('\n')
                    del num[-1]
                    product_id = num[-1]

                write_file('link_list.json', [])

                for i in link_list:
                    drink = [k for k in whiskey if k['link'][0] == i][0]
                    ind = whiskey.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    whiskey[ind] = drink

                write_file('whiskey.json', whiskey)

                write_file('link_list.json', [])

                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    skip_list = read_file('skip_list.json')
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]
                        write_file('skip_list.json', skip_list)

                with open('articles.txt', 'w') as f:
                    doc = doc.replace(product_id + '\n', '')
                    f.write(doc)
                    f.close()

            return redirect('/whiskey_grouping_prove')

    group_id = set([i['product_id'] for i in result_list if 'product_id' in i.keys()])
    groups = list()
    products_with_id = [i for i in whiskey if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
        result_list = [i for i in result_list if not (i in group)]

    return render_template('grouping_whiskey.html', main_drink=main_drink, products=result_list, groups=groups)


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


if __name__ == '__main__':
    app.run(debug=True)

    # from waitress import serve
    # serve(app, host="127.0.0.1", port=8080)
