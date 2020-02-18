import nose.tools as nt
from webtest import TestApp

from url_shortner import generate_short_url, SQLiteBackend, create_app


"""
Run tests with:

>> python3 -m "nose" tests

where "tests" is the target directory where test cases are.
"""


class TestBase62(object):

    def test_base62_returns_short_url_from_number(self):
        actual = generate_short_url(1)
        nt.assert_equal("1", actual)


class TestServer(object):

    def setup(self):
        db_url = 'sqlite:///test.db'
        db = SQLiteBackend(db_url)
        db.bootstrap()
        app = create_app(db)
        self.app = TestApp(app)

    def test_get_short_url_api_is_success(self):
        test_data = {"original_url": "http://test-u-r-l"}
        resp = self.app.post('/short-url', test_data)
        nt.assert_equals(resp.status_int, 200)