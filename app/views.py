from app import app, db, models
from flask import render_template, request, redirect, url_for, flash, session
from .models import *
import random
from datetime import datetime
from app.sql_statements import remove_item
import json
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
from flask_bcrypt import generate_password_hash, check_password_hash

bcrypt = Bcrypt(app)


csrf = CSRFProtect(app)

@app.route('/vote', methods=['POST'])
@csrf.exempt
def vote():
    data = json.loads(request.data)
    idea_id = int(data.get('idea_id'))
    print("python " + str(idea_id))
    idea = models.Product.query.get(idea_id)

    if data.get('vote_type') == "up":
        idea.likes += 1
    else:
        idea.dislikes += 1

    db.session.commit()
    return json.dumps({'status':'OK','upvotes': idea.likes, 'downvotes': idea.dislikes })

# Homepage
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    products = Product.query.all()
    if not products:
        flash("No products found", "error")
    
    return render_template('homepage.html', products=products)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(UserName=username).first()

        if user:
            if password and check_password_hash(user.Password, password):
                session["user"] = user.UserName
                session['userid'] = user.Userid
                flash("Logged in successfully " + user.UserName + "!", "success")
                return redirect(url_for("homepage"))
            else:
                flash("Incorrect password", "error")
        else:
            flash("User not found", "error")
    return render_template('login.html')


# User signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form['username']
        existing_user = User.query.filter_by(UserName=username).first()

        if not existing_user:
            # Hash the password
            password = generate_password_hash(request.form['password']).decode('utf-8')

            # Creating a new user
            new_user = User(
                FirstName=request.form['firstname'],
                LastName=request.form['lastname'],
                Email=request.form['email'],
                UserName=username,
                Password=password
            )

            # Add the new user to the database
            db.session.add(new_user)
            db.session.commit()

            flash("Signed up successfully!", 'success')
            return redirect(url_for('signup'))
        else:
            flash("An account with this username already exists", 'error')
    else:
        # Handle the case where there are no existing users
        existing_users = User.query.all()
        if not existing_users:
            flash("No existing users found, you can create the first one!", 'info')

    return render_template('signup.html')


# Logout
@app.route('/logout')
def logout():
    session.pop("user", None)
    flash("Successfully logged out", 'success')
    return redirect(url_for("homepage"))

#Cart
@app.route('/cart')
def cart():
    if 'user' in session:
        return render_template('/cart.html')
    else:
        return '<h1>401, access not granted</h1>'

@app.route('/add', methods=['POST'])
def add_product_to_cart():
    if int(request.form['quantity']) > 20:
        flash(f'Quantity should not be more than 20', 'error')
        return redirect(url_for('homepage'))
    if int(request.form['quantity']) < 1:
        flash(f'Quantity must be more than 0', 'error')
        return redirect(url_for('homepage'))
    else:
        _quantity = int(request.form['quantity'])
        _code = request.form['code']

    print(f"_quantity: {_quantity}")
    print(f"_code: {_code}")

    if _quantity and _code and request.method == 'POST':
        product = Product.query.filter_by(Code=_code).first()
        print(f'this is product: {product}')

        if product:
            itemArray = {
                product.Code: {
                    'name': product.ProductName,
                    'code': product.Code,
                    'quantity': _quantity,
                    'price': product.Price,
                    'image': product.Image,
                    'total_price': _quantity * product.Price
                }
            }

            all_total_price = 0
            all_total_quantity = 0

            session.modified = True

            if 'user' in session:
                if 'cart_item' in session:
                    if product.Code in session['cart_item']:
                        key = product.Code
                        old_quantity = session['cart_item'][key]['quantity']
                        total_quantity = old_quantity + _quantity
                        session['cart_item'][key]['quantity'] = total_quantity
                        session['cart_item'][key]['total_price'] = total_quantity * product.Price
                        print(f"Updated existing product in cart: {session['cart_item'][key]}")
                    else:
                        print("Adding new product to cart:")
                        print(itemArray)
                        session['cart_item'].update(itemArray)

                    for key, value in session['cart_item'].items():
                        individual_quantity = int(session['cart_item'][key]['quantity'])
                        individual_price = float(session['cart_item'][key]['total_price'])
                        all_total_quantity += individual_quantity
                        all_total_price += individual_price
                else:
                    print("Setting cart_item for the first time:")
                    print(itemArray)
                    session['cart_item'] = itemArray
                    all_total_quantity = _quantity
                    all_total_price = _quantity * product.Price
            else:
                flash("You need to log in first", "error")
                return redirect('/')

            session['all_total_quantity'] = all_total_quantity
            session['all_total_price'] = all_total_price
            print(f"Final cart_item in session: {session['cart_item']}")
            print(f'Successfully added {product.ProductName} to cart!')
            return redirect('/')
        else:
            flash(f'Product with code {_code} not found', 'error')
            return redirect('/')
    else:
        return 'Error while adding item to cart'

    
@app.route('/accountorders', methods=['GET', 'POST'])
def accountorders():
    if request.method == 'GET':
        userid = session['userid']
        # Fetch information about the user in session using SQLAlchemy
        data = Orders.query.filter_by(UserID=userid).all()

        # Fetch products data using a join query with SQLAlchemy
        productsdata = db.session.query(OrderDetail.ProductCode, OrderDetail.Quantity, OrderDetail.OrderNumber)\
            .join(Orders, Orders.Orderid == OrderDetail.Orderid)\
            .filter(Orders.UserID == userid).all()

        return render_template('accountorders.html', passingdata=data, passingproductsdata=productsdata)

@app.route('/empty')
def empty_cart():
    #clears session containing products.
    session.pop('cart_item', None)
    return redirect('/cart')


@app.route('/delete/<string:code>')
def delete_product(code):
    all_total_price = 0
    all_total_quantity = 0
    session.modified = True

    for item in session['cart_item'].items():
        if item[0] == code:
            session['cart_item'].pop(item[0], None)
            if 'cart_item' in session:
                for key, value in session['cart_item'].items():
                    individual_quantity = int(
                        session['cart_item'][key]['quantity'])
                    individual_price = float(
                        session['cart_item'][key]['total_price'])
                    all_total_quantity = all_total_quantity + individual_quantity
                    all_total_price = all_total_price + individual_price
            break

    if all_total_quantity == 0:
        session.pop('cart_item', None)
        print("cleared cart")
    else:
        session['all_total_quantity'] = all_total_quantity
        session['all_total_price'] = all_total_price

    #return redirect('/')
    return redirect('/cart')

@app.route('/checkout', methods=['GET','POST'])
def checkout():
    user = session.get("user")
    temp = []
    ordernumber = ''
    # creates a unique order number every time a customer places an order.
    random_num = str(random.randint(0, 1000))
    temp.append(random_num)
    if random_num not in temp:
        ordernumber = int(random_num)
    else:
        ordernumber = str(random.randint(0, 1000))

    if request.method == 'POST':
        # fetches UserID for the user in session.
        user_data = User.query.filter_by(UserName=user).first()
        userid = user_data.Userid

        # collects information about the order.
        current_date = datetime.today().strftime('%d-%m-%Y')
        full_price = session['all_total_price']

        # collects user details for the order.
        order = Orders(
            OrderNumber=ordernumber,
            UserID=userid,
            Phone=request.form['phone'],
            Address=request.form['address'],
            OrderDate=current_date,
            Price=full_price
        )
        db.session.add(order)
        db.session.commit()

        # fetches OrderID from the recent order.
        order_data = Orders.query.filter_by(OrderNumber=ordernumber).first()
        orderid = order_data.Orderid

        session['userid'] = userid

        # collects information about the products that have been ordered with their quantity
        for key, value in session['cart_item'].items():
            print(key)
            product_code = session['cart_item'][key]['code']
            quantity = session['cart_item'][key]['quantity']

            product_data = Product.query.filter_by(Code=product_code).first()
            productid = product_data.Productid

            order_detail = OrderDetail(
                Orderid = orderid,
                OrderNumber=ordernumber,
                Userid=userid,
                Productid=productid,
                ProductCode=product_code,
                Quantity=quantity
            )
            db.session.add(order_detail)
            db.session.commit()

            remove_item(product_code, quantity)

        flash("Order Successful!", 'success')
        # clears items in the cart.
        session.pop('cart_item', None)
        return redirect(url_for("homepage"))

# Account info
@app.route('/accountinfo')
def accountinfo():
    if 'user' in session:
        user = User.query.filter_by(UserName=session['user']).first()
        return render_template('accountinfo.html', user=user)
    else:
        return '<h1>401, access not granted</h1>'
