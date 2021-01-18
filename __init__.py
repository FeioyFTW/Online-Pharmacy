import Item
import Cart
import shelve

from flask import Flask, render_template, request, redirect, url_for, flash

from Forms import CreateItemForm, BuyItemForm, CheckoutForm, SearchBar

app = Flask(__name__, static_url_path='/static')

app.secret_key = b'o5Dg987*&G^@(E&FW)}'


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/pharmacy', methods=['GET', 'POST'])
def show_items():
    search = SearchBar(request.form)
    if request.method == 'POST':
        item_dict = {}
        db = shelve.open('storage.db', 'r')
        item_dict = db['Items']
        db.close()

        item_list = []
        start_item_list = []
        contain_item_list = []
        for key in item_dict:
            item = item_dict.get(key)
            if item.get_item_name().lower().startswith(search.search.data.lower()):
                start_item_list.append(item)
            elif search.search.data.lower() in item.get_item_name().lower():
                contain_item_list.append(item)

            item_list = start_item_list + contain_item_list

        return render_template('pharmacy.html', items_list=item_list, form=search)

    item_dict = {}
    db = shelve.open('storage.db', 'r')
    item_dict = db['Items']
    db.close()

    item_list = []
    for key in item_dict:
        item = item_dict.get(key)
        item_list.append(item)

    return render_template('pharmacy.html', items_list=item_list, form=search)


@app.route('/pharmacy/hot', methods=['GET', 'POST'])
def show_hot():
    search = SearchBar(request.form)
    if request.method == 'POST':
        item_dict = {}
        db = shelve.open('storage.db', 'r')
        item_dict = db['Items']
        db.close()

        item_list = []
        start_item_list = []
        contain_item_list = []
        for key in item_dict:
            item = item_dict.get(key)
            if "hot" in item.get_item_tag():
                if item.get_item_name().lower().startswith(search.search.data.lower()):
                    start_item_list.append(item)
                elif search.search.data.lower() in item.get_item_name().lower():
                    contain_item_list.append(item)

                item_list = start_item_list + contain_item_list

        return render_template('pharmacy.html', items_list=item_list, form=search)

    item_dict = {}
    db = shelve.open('storage.db', 'r')
    item_dict = db['Items']
    db.close()

    item_list = []
    for key in item_dict:
        item = item_dict.get(key)
        if "hot" in item.get_item_tag():
            item_list.append(item)

    return render_template('pharmacy.html', items_list=item_list, form=search)


@app.route('/createItem', methods=['GET', 'POST'])
def create_item():
    create_item_form = CreateItemForm(request.form)
    if request.method == 'POST' and create_item_form.validate():
        item_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            item_dict = db['Items']
        except:
            print("Error in retrieving Items from storage.db.")

        item = Item.Item(create_item_form.name.data, round(create_item_form.price.data, 2), create_item_form.have.data,
                         create_item_form.bio.data, create_item_form.picture.data)
        item_dict[item.get_item_id()] = item
        db['Items'] = item_dict

        db.close()

        return redirect(url_for('inventory'))
    return render_template('createItem.html', form=create_item_form)


@app.route('/inventory')
def inventory():
    item_dict = {}
    db = shelve.open('storage.db', 'r')
    item_dict = db['Items']
    db.close()

    item_list = []
    for key in item_dict:
        item = item_dict.get(key)
        item_list.append(item)

    return render_template('inventory.html', items_list=item_list)


@app.route('/purchaseItem/<int:id>/', methods=['GET', 'POST'])
def buy_item(id):
    buy_item_form = BuyItemForm(request.form)

    if request.method == 'POST' and buy_item_form.validate():
        db = shelve.open('storage.db', 'w')
        item_dict = db['Items']
        cart = db['Cart']

        item = item_dict.get(id)
        item.set_item_want(buy_item_form.want.data)

        if item.get_item_want() > item.get_item_have():
            item.set_item_want(0)
            flash("Not enough stock at the moment, try again later")
        elif not cart.check(item):
            cart.add(item)
            db['Items'] = item_dict
            db['Cart'] = cart

        db.close()
        return redirect(url_for('show_items'))

    else:
        item_dict = {}
        db = shelve.open('storage.db', 'r')
        item_dict = db['Items']
        db.close()

        item = item_dict.get(id)
        buy_item_form.want.data = item.get_item_want()

        return render_template('buyItem.html', form=buy_item_form, name=item.get_item_name(),
                               bio=item.get_item_bio(), price=item.get_item_price(), picture=item.get_item_picture(),
                               have=item.get_item_have())


@app.route('/updateItem/<int:id>/', methods=['GET', 'POST'])
def update_item(id):
    update_item_form = CreateItemForm(request.form)

    if request.method == 'POST' and update_item_form.validate():
        db = shelve.open('storage.db', 'w')
        item_dict = db['Items']

        item = item_dict.get(id)
        item.set_item_name(update_item_form.name.data)
        item.set_item_price(update_item_form.price.data)
        item.set_item_have(update_item_form.have.data)
        item.set_item_bio(update_item_form.bio.data)
        item.set_item_picture(update_item_form.picture.data)

        db['Items'] = item_dict
        db.close()

        return redirect(url_for('inventory'))
    else:
        item_dict = {}
        db = shelve.open('storage.db', 'r')
        item_dict = db['Items']
        db.close()

        item = item_dict.get(id)
        update_item_form.name.data = item.get_item_name()
        update_item_form.price.data = item.get_item_price()
        update_item_form.have.data = item.get_item_have()
        update_item_form.bio.data = item.get_item_bio()
        update_item_form.picture.data = item.get_item_picture()

        return render_template('updateItem.html', form=update_item_form)


@app.route('/deleteItem/<int:id>', methods=['POST'])
def delete_item(id):
    item_dict = {}
    db = shelve.open('storage.db', 'w')
    item_dict = db['Items']

    item_dict.pop(id)

    db['Items'] = item_dict
    db.close()

    return redirect(url_for('inventory'))


@app.route('/removeItem/<int:id>', methods=['POST'])
def remove_item(id):
    item_dict = {}
    db = shelve.open('storage.db', 'w')
    item_dict = db['Items']
    cart = db['Cart']

    item = item_dict.get(id)
    item.set_item_want(0)
    cart.remove(item)

    db['Items'] = item_dict
    db['Cart'] = cart
    db.close()

    return redirect(url_for('shopping_cart'))


@app.route('/clearCart', methods=['POST'])
def clear_cart():
    db = shelve.open('storage.db', 'w')
    cart = db['Cart']

    cart.clear_cart()

    db['Cart'] = cart
    db.close()

    return redirect(url_for('shopping_cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    checkout_form = CheckoutForm(request.form)

    if request.method == 'POST' and checkout_form.validate():
        item_dict = {}
        db = shelve.open('storage.db', 'w')
        cart = db['Cart']
        item_dict = db['Items']

        cart.checkout()
        for key in item_dict:
            item = item_dict.get(key)
            item.set_item_have(item.get_item_have() - item.get_item_want())
            item.set_item_want(0)

        db['Items'] = item_dict
        db['Cart'] = cart
        db.close()
        return redirect(url_for('paid'))

    else:
        db = shelve.open('storage.db', 'r')
        cart = db['Cart']
        db.close()

        item_list = []
        for item in cart.get_cart():
            item_list.append(item)

    return render_template('checkout.html', form=checkout_form)


@app.route('/shoppingCart', methods=['GET', 'POST'])
def shopping_cart():
    search = SearchBar(request.form)
    if request.method == 'POST':
        db = shelve.open('storage.db', 'r')
        item_dict = db['Items']
        cart = db['Cart']
        db.close()

        item_list = cart.get_cart()
        total = cart.total()
        count = cart.get_count()

        start_item_list = []
        contain_item_list = []
        for item in cart.get_cart():
            if item.get_item_name().lower().startswith(search.search.data.lower()):
                start_item_list.append(item)
            elif search.search.data.lower() in item.get_item_name().lower():
                contain_item_list.append(item)

            item_list = start_item_list + contain_item_list

        return render_template('shoppingCart.html', items_list=item_list, form=search, total=total, count=count)
    item_dict = {}
    db = shelve.open('storage.db', 'r')
    item_dict = db['Items']
    cart = db['Cart']
    db.close()

    item_list = cart.get_cart()
    total = cart.total()
    count = cart.get_count()

    return render_template('shoppingCart.html', items_list=item_list, form=search, total=total, count=count)


@app.route('/complete')
def paid():
    return render_template('complete.html')


if __name__ == '__main__':
    app.run()
