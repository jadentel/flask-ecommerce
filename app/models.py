from app import db
from flask_bcrypt import generate_password_hash

class User(db.Model):
    Userid = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(500))
    LastName = db.Column(db.String(500))
    Email = db.Column(db.String(500))
    UserName = db.Column(db.String(500))
    Password = db.Column(db.String(500))



    def __init__(self, FirstName, LastName, Email, UserName, Password):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Email = Email
        self.UserName = UserName
        self.Password = Password

def initialise_user():
    password = generate_password_hash('passing').decode('utf-8')
    
    user_data = [{'FirstName': 'test_first', 'LastName': 'test_last', 'Email': 'test@email.com', 'UserName': 'test', 'Password': password}]
    if not User.query.first():
        for data in user_data:
            user = User(**data)
            db.session.add(user)
        db.session.commit()


class Product(db.Model):
    Productid = db.Column(db.Integer, primary_key=True)
    ProductName = db.Column(db.String(500))
    Code = db.Column(db.String(500))
    Image = db.Column(db.String(500))
    Price = db.Column(db.Float)
    Description = db.Column(db.String(500))
    Stock = db.Column(db.Integer)
    likes = db.Column(db.Integer)
    dislikes = db.Column(db.Integer)



    def __init__(self, ProductName, Code, Image, Price, Description, Stock, likes, dislikes):
        self.ProductName = ProductName
        self.Code = Code
        self.Image = Image
        self.Price = Price
        self.Description = Description
        self.Stock = Stock
        self.likes = likes
        self.dislikes = dislikes
        



def initialize_data():
    products_data = [
        {'ProductName': 'Black T-shirt', 'Code': 'BLKTS01', 'Image': '/static/images/black_tshirt.jpg', 'Price': 5.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Red T-shirt', 'Code': 'REDTS02', 'Image': '/static/images/red_tshirt.jpg', 'Price': 3.99, 'Description': 'Size: Large', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Black Hoodie', 'Code': 'BLKHD03', 'Image': '/static/images/black_hoodie.png', 'Price': 10.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Black Jeans', 'Code': 'BLKJN04', 'Image': '/static/images/black_jeans.jpg', 'Price': 15.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Blue Jeans', 'Code': 'BLUJN05', 'Image': '/static/images/blue_jeans.jpg', 'Price': 15.99, 'Description': 'Size: Small', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'White Hoodie', 'Code': 'WHIHD06', 'Image': '/static/images/white_hoodie.png', 'Price': 13.99, 'Description': 'Size: Large', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Yellow Flannel', 'Code': 'YLWFL07', 'Image': '/static/images/yellow_flannel.jfif', 'Price': 7.99, 'Description': 'Size: Large', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Red Flannel', 'Code': 'REDFL08', 'Image': '/static/images/red_flannel.jpg', 'Price': 7.99, 'Description': 'Size: Small', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Yellow T-shirt', 'Code': 'YLWTS09', 'Image': '/static/images/yellow_tshirt.jpg', 'Price': 5.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Blue Hoodie', 'Code': 'BLUHDS10', 'Image': '/static/images/blue_hoodie.jpg', 'Price': 12.99, 'Description': 'Size: Large', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Black Joggers', 'Code': 'BLKJG11', 'Image': '/static/images/black_joggers.jpg', 'Price': 5.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
        {'ProductName': 'Black Jacket', 'Code': 'BLKJT12', 'Image': '/static/images/black_jacket.png', 'Price': 29.99, 'Description': 'Size: Medium', 'Stock': 12, 'likes': 0, 'dislikes': 0},
    ]

    if not Product.query.first():
        for data in products_data:
            product = Product(**data)
            db.session.add(product)
        db.session.commit()


class Orders(db.Model):
    Orderid = db.Column(db.Integer, primary_key=True)
    OrderNumber = db.Column(db.String(500))
    UserID = db.Column(db.String(500))
    Phone = db.Column(db.String(500))
    Address = db.Column(db.String(500))
    OrderDate = db.Column(db.String(500))
    Price = db.Column(db.Float)


    def __init__(self, OrderNumber, UserID, Phone, Address, OrderDate, Price):
        self.OrderNumber = OrderNumber
        self.UserID = UserID
        self.Phone = Phone
        self.Address = Address
        self.OrderDate = OrderDate
        self.Price = Price

class OrderDetail(db.Model):
    OrderDetailID = db.Column(db.Integer, primary_key=True)
    Orderid = db.Column(db.Integer, db.ForeignKey('orders.Orderid'))
    OrderNumber = db.Column(db.Integer)
    Userid = db.Column(db.Integer, db.ForeignKey('user.Userid'))
    Productid = db.Column(db.Integer, db.ForeignKey('product.Productid'))
    ProductCode = db.Column(db.String(500))
    Quantity = db.Column(db.Integer)

    order = db.relationship('Orders', backref='order_detail')
    product = db.relationship('Product', backref='order_detail')
    user = db.relationship('User', backref='order_detail')

    def __init__(self, Orderid, OrderNumber, Userid, Productid, ProductCode, Quantity):
        self.Orderid = Orderid
        self.OrderNumber = OrderNumber
        self.Userid = Userid
        self.Productid = Productid
        self.ProductCode = ProductCode
        self.Quantity = Quantity
