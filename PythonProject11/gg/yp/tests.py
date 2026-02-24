import unittest


#ТЕСТ 1: Расчёт итоговой цены с учётом скидки

def calculate_final_price(price, discount_percent):
    if price < 0 or discount_percent < 0 or discount_percent > 100:
        raise ValueError('Некорректные входные данные')
    return round(price * (1 - discount_percent / 100), 2)

class TestCalculateFinalPrice(unittest.TestCase):

    def test_standard_discount(self):
        result = calculate_final_price(1000.0, 20)
        self.assertEqual(result, 800.0)

    def test_zero_discount(self):
        result = calculate_final_price(500.0, 0)
        self.assertEqual(result, 500.0)

    def test_negative_price(self):
        with self.assertRaises(ValueError):
            calculate_final_price(-100.0, 10)


#ТЕСТ 2: Авторизация пользователя

MOCK_USERS = {
    'admin':    {'password': 'admin123', 'role': 'administrator'},
    'manager1': {'password': 'pass1',    'role': 'manager'},
}

def authenticate_user(login, password, users_db):
    user = users_db.get(login)
    if user and user['password'] == password:
        return user['role']
    return None

class TestAuthenticateUser(unittest.TestCase):

    def test_success(self):
        role = authenticate_user('admin', 'admin123', MOCK_USERS)
        self.assertEqual(role, 'administrator')

    def test_wrong_password(self):
        role = authenticate_user('admin', 'wrongpass', MOCK_USERS)
        self.assertIsNone(role)

    def test_unknown_login(self):
        role = authenticate_user('unknown', '123', MOCK_USERS)
        self.assertIsNone(role)


#ТЕСТ 3: Проверка права на удаление товара

MOCK_ORDERS = [
    {'order_id': 1, 'product_ids': [10, 20, 30]},
    {'order_id': 2, 'product_ids': [20, 40]},
]

def can_delete_product(product_id, orders_list):
    for order in orders_list:
        if product_id in order['product_ids']:
            return False
    return True

class TestCanDeleteProduct(unittest.TestCase):

    def test_blocked(self):
        result = can_delete_product(20, MOCK_ORDERS)
        self.assertFalse(result)

    def test_allowed(self):
        result = can_delete_product(99, MOCK_ORDERS)
        self.assertTrue(result)

    def test_empty_orders(self):
        result = can_delete_product(10, [])
        self.assertTrue(result)


#ТЕСТ 4: Генерация нового ID товара

def get_next_product_id(existing_ids):
    if not existing_ids:
        return 1
    return max(existing_ids) + 1

class TestGetNextProductId(unittest.TestCase):

    def test_standard(self):
        result = get_next_product_id([1, 2, 5, 10])
        self.assertEqual(result, 11)

    def test_empty(self):
        result = get_next_product_id([])
        self.assertEqual(result, 1)

