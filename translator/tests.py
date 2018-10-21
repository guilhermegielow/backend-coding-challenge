import unittest
import app


class TestTranslatorUnbabel(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def testIndex(self):
        print('Testing testIndex')

        text = 'My test is OK'
        response = self.app.get('/', data=dict(text_to_translate=text), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(text, response.data)

    def testPrepareTranslation(self):
        print('Testing testPrepareTranslation')
        self.assertEqual(type(app.prepare_translation(app.request_translation('This is my test two'))),
                         type({}))

    def testRequestTranslation(self):
        print('Testing testRequestTranslation')
        self.assertTrue(app.request_translation('This is my test three').uid)

    def testRequestUpdate(self):
        print('Testing testRequestUpdate')
        self.assertTrue(app.request_update('bc07ca0ffd').status)

    def testUpdateStatus(self):
        print('Testing testUpdateStatus')
        self.assertEqual(app.update_status('new'), 'requested')
        self.assertEqual(app.update_status('translating'), 'pending')
        self.assertEqual(app.update_status('completed'), 'translated')
        self.assertEqual(app.update_status('text'), 'text')


if __name__ == "__main__":
    unittest.main()
