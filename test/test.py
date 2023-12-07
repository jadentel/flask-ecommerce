"""
import unittest
from app import app, db, models

class TestModels(unittest.TestCase):

    def setUp(self):
        app.config.from_object('config')
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        with app.app_context():
            self.app = app.test_client()
            db.create_all()


    def test_user_creation(self):
        with app.app_context():
            user = models.User(FirstName='John', LastName='Doe', Email='john@example.com', UserName='john_doe', Password='hashed_password')
            db.session.add(user)
            db.session.commit()

            retrieved_user = models.User.query.filter_by(UserName='john_doe').first()
            self.assertIsNotNone(retrieved_user)
            self.assertEqual(retrieved_user.FirstName, 'John')

    def test_product_creation(self):
        with app.app_context():
            user = models.Product(ProductName='Test', Code='TST123', Image='/static/images/black_tshirt.jpg', Price=6.98, Description='Size: Large', Stock = 12, likes = 0, dislikes = 0)
            db.session.add(user)
            db.session.commit()

            retrieved_product = models.Product.query.filter_by(ProductName='Test').first()
            self.assertIsNotNone(retrieved_product)
            self.assertEqual(retrieved_product.ProductName, 'Test')

    def test_order_creation(self):
        with app.app_context():
            order = models.Orders(OrderNumber='12345', UserID='user123', Phone='555-1234', Address='123 Main St', OrderDate='2023-12-07', Price=50.0)
            db.session.add(order)
            db.session.commit()

            retrieved_order = models.Orders.query.filter_by(OrderNumber='12345').first()
            self.assertIsNotNone(retrieved_order)
            self.assertEqual(retrieved_order.OrderNumber, '12345')

    def test_order_detail_creation(self):
        with app.app_context():
            order_detail = models.OrderDetail(Orderid=1, OrderNumber='12345', Userid=1, Productid=1, ProductCode='ABC123', Quantity=2)
            db.session.add(order_detail)
            db.session.commit()

            retrieved_order_detail = models.OrderDetail.query.filter_by(OrderNumber='12345').first()
            self.assertIsNotNone(retrieved_order_detail)
            self.assertEqual(retrieved_order_detail.ProductCode, 'ABC123')

    

if __name__ == '__main__':
    unittest.main()
"""