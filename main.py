from flask import Flask, render_template, request, abort, url_for, redirect, flash
import json
import numpy
from pprint import pprint


app = Flask(__name__)
app.config['SECRET_KEY'] = '12091988BernardoProvencanoToto'


@app.route('/')
def main_page():
    return render_template('main_page.html')


@app.route('/whiskey_grouping_prove')
def whiskey_grouping_prove():
    return render_template('whiskey_grouping_prove.html')


@app.route('/finished_whiskey', methods=['GET', 'POST'])
def finished_whiskey():
    show_group = None
    group_titles = None
    with open('whiskey.json') as f:
        whiskey = f.read()
        whiskey = json.loads(whiskey)
        f.close()

    with open('productData.json') as f:
        merged_whiskey = f.read()
        merged_whiskey = json.loads(merged_whiskey)
        f.close()

    productData_links = [i['links'] for i in merged_whiskey]
    productData_groups = [i for i in merged_whiskey]

    if productData_links:
        show_group = productData_links[0]

        show_group = [[i for i in whiskey if i['link'][0] in show_group]]
        group_titles = productData_groups[0]

    if 'next' in request.form:

        for i in productData_groups:
            print(i)

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
        # print(request.form['delete_from_finished'])
        delete_id = request.form['delete_from_finished']
        with open('productData.json') as f:
            productData = f.read()
            productData = json.loads(productData)
            f.close()

        need_to_delete = [i for i in productData if i['id'] == delete_id][0]
        productData.remove(need_to_delete)

        with open('productData.json', 'w') as f:
            json.dump(productData, f, ensure_ascii=False, indent=2)
            f.close()

        with open('whiskey.json') as f:
            whiskey = f.read()
            whiskey = json.loads(whiskey)
            f.close()

        product_with_id = [i for i in whiskey if 'product_id' in i.keys()]
        need_to_delete_list = [i for i in product_with_id if i['product_id'] == delete_id]
        for i in need_to_delete_list:
            ind = whiskey.index(i)
            i.pop('in_productData')
            whiskey[ind] = i

        with open('whiskey.json', 'w') as f:
            json.dump(whiskey, f, ensure_ascii=False, indent=2)
            f.close()

        flash('Группа успешно отправлена на повторную обработку')
        return redirect('/whiskey_grouping_prove')

    return render_template('finished_whiskey.html', groups=show_group, titles=group_titles)


# del_list = []


@app.route('/naming_whiskey', methods=['GET', 'POST'])
def naming_whiskey():
    show_group = None

    with open('whiskey.json') as f:
        whiskey = f.read()
        whiskey = json.loads(whiskey)
        f.close()
    # group_id = numpy.unique([i['product_id'] for i in whiskey if 'product_id' in i.keys()])
    group_id = numpy.unique([i['product_id'] for i in whiskey if 'product_id' in i.keys() and not ('in_productData' in i.keys())])
    groups = list()
    products_with_id = [i for i in whiskey if 'product_id' in i.keys()]
    for i in group_id:
        group = [k for k in products_with_id if k['product_id'] == i]
        groups.append(group)
    if groups:
        show_group = [groups[0]]

    if 'saving' in request.form:

        with open('whiskey.json') as f:
            whiskey = f.read()
            whiskey = json.loads(whiskey)
            f.close()
        with open('del_list.json') as f:
            del_list = f.read()
            del_list = json.loads(del_list)
            f.close()
        for i in del_list:
            # print(i)
            del_product = [k for k in whiskey if k['link'][0] == i]
            if del_product:
                del_product[0]['identified'] = False
                del_product[0].pop('product_id')
                whiskey[whiskey.index([n for n in whiskey if n['link'][0] == i][0])] = del_product[0]
                print(whiskey[whiskey.index([n for n in whiskey if n['link'][0] == i][0])])


        with open('whiskey.json', 'w') as f:
            json.dump(whiskey, f, ensure_ascii=False, indent=2)
            f.close()

        # del_list.clear()
        with open('del_list.json', 'w') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
            f.close()

        product_dict = dict()
        product_dict['features'] = {}
        product_dict['images'] = {}
        product_dict['description'] = ''
        product_dict['section'] = 'Виски'
        product_dict['id'] = request.form['group_id']
        product_dict['name'] = request.form['title']
        product_dict['features']['Страна'] = request.form['country']
        product_dict['features']['Бренд'] = request.form['brand']
        product_dict['features']['Тип'] = request.form['type']
        product_dict['features']['Выдержка'] = int(request.form['exposure'])
        product_dict['features']['Крепость'] = int(request.form['fortress'])
        with open('whiskey.json') as f:
            whiskey = f.read()
            whiskey = json.loads(whiskey)
            f.close()
        products = [i for i in whiskey if 'product_id' in i.keys()]
        product_dict['links'] = [i['link'][0] for i in products if i['product_id'] == product_dict['id']]
        product_dict['images']['default'] = [i['image'][0] for i in whiskey if i['link'][0] in product_dict['links']][0]

        with open('productData.json') as f:
            productData = f.read()
            productData = json.loads(productData)
            f.close()

        productData.append(product_dict)

        with open('productData.json', 'w') as f:
            json.dump(productData, f, ensure_ascii=False, indent=2)

        with open('whiskey.json') as f:
            whiskey = f.read()
            whiskey = json.loads(whiskey)
            f.close()

        for i in whiskey:
            if 'product_id' in i.keys():
                if i['product_id'] == product_dict['id']:
                    ind = whiskey.index(i)
                    i['in_productData'] = True
                    whiskey[ind] = i

        with open('whiskey.json', 'w') as f:
            json.dump(whiskey, f, ensure_ascii=False, indent=2)

        flash('Операция проведена успешно')
        return redirect('/whiskey_grouping_prove')

    if 'delete_from_group' in request.form:
        del_link = request.form['delete_from_group']
        with open('del_list.json') as f:
            del_list = f.read()
            del_list = json.loads(del_list)
            f.close()

        if not (del_link in del_list):
            del_list.append(del_link)
        else:
            del_list.remove(del_link)

        with open('del_list.json', 'w') as f:
            json.dump(del_list, f, ensure_ascii=False, indent=2)
            f.close()

        print('delete list', del_list)

    if 'next' in request.form:
        for i in groups:
            if str(i) == str(request.form['next']):
                if groups.index(i) != len(groups)-1:
                    show_group = [groups[groups.index(i)+1]]
                    break
                else:
                    show_group = [groups[-1]]

        with open('del_list.json', 'w') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
            f.close()

        # del_list.clear()

    if 'previous' in request.form:
        for i in groups:
            if str(i) == str(request.form['previous']):
                if groups.index(i) != 0:
                    show_group = [groups[groups.index(i) - 1]]
                    break

        with open('del_list.json', 'w') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
            f.close()
        # del_list.clear()

    return render_template('naming_whiskey.html', groups=show_group)


# link_list = list()
skip_list = []


@app.route('/grouping_whiskey/', methods=['GET', 'POST'])
def grouping_whiskey():
    search = ''
    result_list = []

    with open('whiskey.json') as f:
        whiskey = f.read()
        whiskey = json.loads(whiskey)
        f.close()


    main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
    if main_drink:
        main_drink = main_drink[0]
    else:
        if skip_list:
            print('Количество пропущенных напитков', len(skip_list))

            del skip_list[0]
            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]

    if "index" in request.form:
        link = request.form['index']

        # тестирование
        with open('link_list.json') as f:
            link_list = f.read()
            link_list = json.loads(link_list)
            f.close()
            print(link_list, 'in index')



        if link in link_list:
            link_list.remove(link)
        else:
            link_list.append(link)

        with open('link_list.json', 'w') as f:
            json.dump(link_list, f, ensure_ascii=False, indent=2)
            f.close()

    if 'add_to_group' in request.form:
        article = request.form['add_to_group']
        with open('link_list.json') as f:
            link_list = f.read()
            link_list = json.loads(link_list)
            f.close()
        print(link_list, 'add group')
        if article in link_list:
            link_list.remove(article)
        else:
            link_list.append(article)

        with open('link_list.json', 'w') as f:
            json.dump(link_list, f, ensure_ascii=False, indent=2)
            f.close()
        print(link_list, 'add to group')

    if 'skip' in request.form:

        with open('link_list.json', 'w') as f:
            json.dump([], f, ensure_ascii=False, indent=2)
            f.close()

        # link_list.clear()

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

    if 'search' in request.form:
        search = request.form['search']
        result_list = [i for i in whiskey if search.lower() in i['name'][0].lower() and not (i is main_drink)]

    if 'saving' in request.form:

        with open('link_list.json') as f:
            link_list = f.read()
            link_list = json.loads(link_list)
            f.close()
            print(link_list, 'in saving')

        match = [i for i in link_list if i.isdigit()]

        if len(match) > 1:
            flash('Ошибка: Вы можете добавить напиток только в одну группу')
            with open('link_list.json', 'w') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
                f.close()
            # link_list.clear()
            return redirect('/grouping_whiskey')
            # return redirect('/test')

        elif len(match) == 1:

            with open('link_list.json') as f:
                link_list = f.read()
                link_list = json.loads(link_list)
                f.close()

            link_list.remove(match[0])
            if main_drink:
                link_list.append(main_drink['link'][0])

            with open('link_list.json', 'w') as f:
                json.dump(link_list, f, ensure_ascii=False, indent=2)
                f.close()

            product_id = match[0]

            # with open('whiskey.json', 'w') as f:

            with open('link_list.json') as f:
                link_list = f.read()
                link_list = json.loads(link_list)
                f.close()

            for i in link_list:
                drink = [k for k in whiskey if k['link'][0] == i][0]
                ind = whiskey.index(drink)
                drink['identified'] = True
                drink['product_id'] = product_id
                whiskey[ind] = drink
            if whiskey:
                with open('whiskey.json', 'w') as f:
                    json.dump(whiskey, f, ensure_ascii=False, indent=2)
                    f.close()

            main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
            if main_drink:
                main_drink = main_drink[0]
            else:
                if skip_list:
                    del skip_list[0]
                    main_drink = [i for i in whiskey if
                                    i['identified'] is False and not (i['link'][0] in skip_list)]
                    if main_drink:
                        main_drink = main_drink[0]

            with open('productData.json') as f:

                with open('link_list.json') as f:
                    link_list = f.read()
                    link_list = json.loads(link_list)
                    f.close()
            with open('productData.json') as f:
                productData = f.read()
                productData = json.loads(productData)
                f.close()
                item_in_PD = [i for i in productData if i['id'] == product_id]
                if item_in_PD:
                    item_in_PD_index = productData.index(item_in_PD[0])
                    if item_in_PD:
                        for i in link_list:
                            item_in_PD[0]['links'].append(i)

                        productData[item_in_PD_index] = item_in_PD[0]

                with open('productData.json', 'w') as f:
                    json.dump(productData, f, ensure_ascii=False, indent=2)
                    f.close()

                with open('whiskey.json') as f:
                    whiskey = f.read()
                    whiskey = json.loads(whiskey)
                    f.close()
                need_change = [i for i in whiskey if i['link'][0] in link_list]
                for i in need_change:
                    ind = whiskey.index(i)
                    i['in_productData'] = True
                    whiskey[ind] = i
                with open('whiskey.json', 'w') as f:
                    json.dump(whiskey, f, ensure_ascii=False, indent=2)
                    f.close()

            # link_list.clear()


            with open('link_list.json', 'w') as f:
                json.dump([], f, ensure_ascii=False, indent=2)
                f.close()

            return redirect('/whiskey_grouping_prove')
        else:
            if main_drink:
                with open('link_list.json', 'w') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                    f.close()

                link_list.append(main_drink['link'][0])

                with open('link_list.json', 'w') as f:
                    json.dump(link_list, f, ensure_ascii=False, indent=2)
                    f.close()

                with open('articles.txt', 'r') as f:
                    doc = f.read()
                    num = doc.split('\n')
                    del num[-1]
                    product_id = num[-1]


                with open('link_list.json', 'w') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                    f.close()

                for i in link_list:
                    drink = [k for k in whiskey if k['link'][0] == i][0]
                    ind = whiskey.index(drink)
                    drink['identified'] = True
                    drink['product_id'] = product_id
                    whiskey[ind] = drink


                with open('whiskey.json', 'w') as f:
                    json.dump(whiskey, f, ensure_ascii=False, indent=2)
                    f.close()

                # link_list.clear()

                with open('link_list.json', 'w') as f:
                    json.dump([], f, ensure_ascii=False, indent=2)
                    f.close()

                main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
                if main_drink:
                    main_drink = main_drink[0]
                else:
                    if skip_list:
                        del skip_list[0]
                        main_drink = [i for i in whiskey if i['identified'] is False and not (i['link'][0] in skip_list)]
                        if main_drink:
                            main_drink = main_drink[0]

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


if __name__ == '__main__':
    app.run(debug=True)

    # from waitress import serve
    # serve(app, host="127.0.0.1", port=8080)
