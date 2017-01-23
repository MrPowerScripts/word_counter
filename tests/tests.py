from app.app import create_app
from app.extensions import db
from app.settings import TestConfig


class TestMixin():
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        # creates a test client

        test = create_app(TestConfig)

        self.app = test.test_client()
        # propagate the exceptions to the test client
        self.app.testing = True

        db.init_app(test)

        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.close()
        db.drop_all()
