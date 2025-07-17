import unittest
from flask import Flask, session
from qr_auth import qr_bp, qr_sessions
import uuid


class QRAuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.secret_key = 'test_secret'
        self.app.register_blueprint(qr_bp)

        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

        # 模拟登录后，设置session和qr_sessions数据
        self.qr_token = str(uuid.uuid4())
        with self.client.session_transaction() as sess:
            sess['qr_token'] = self.qr_token
        qr_sessions[self.qr_token] = {'verified': False, 'user_id': 1}

    def tearDown(self):
        qr_sessions.clear()
        self.ctx.pop()

    def test_qr_auth_page(self):
        response = self.client.get('/qr-auth')
        self.assertEqual(response.status_code, 200)
        self.assertIn("扫码验证登录".encode('utf-8'), response.data)

    def test_qr_image_generation(self):
        response = self.client.get('/qr-image')
        # 如果测试失败，打印响应内容以便调试
        if response.status_code != 200:
            print(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'image/png')

    def test_qr_verification(self):
        verify_url = f'/verify_qr/{self.qr_token}'
        response = self.client.get(verify_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("扫码成功".encode('utf-8'), response.data)
        self.assertTrue(qr_sessions[self.qr_token]['verified'])

    def test_check_qr_status(self):
        response = self.client.get('/check_qr')
        self.assertEqual(response.data, b'pending')

        self.client.get(f'/verify_qr/{self.qr_token}')
        response = self.client.get('/check_qr')
        self.assertEqual(response.data, b'verified')


if __name__ == '__main__':
    unittest.main()
