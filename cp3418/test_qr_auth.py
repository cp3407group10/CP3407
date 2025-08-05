from app2 import app
from config import get_db_connection

def test_confirm_qr_auth():
    db_connection = get_db_connection()
    assert db_connection.is_connected()  # 确认连上了数据库

    with db_connection.cursor() as cursor:
        #
        cursor.execute(
            "INSERT INTO auth_logs (token, reasons) VALUES (%s, %s)",
            ("testtoken123", "test reasons")
        )
        db_connection.commit()

    with app.test_client() as client:
        token = "testtoken123"
        data = {"reasons": ["reason1", "reason2"]}
        response = client.post(f'/qr-auth/confirm/{token}', json=data)
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data.get('success') == True

    # 测试结束后清理测试数据
    with db_connection.cursor() as cursor:
        cursor.execute("DELETE FROM auth_logs WHERE token = %s", ("testtoken123",))
        db_connection.commit()
