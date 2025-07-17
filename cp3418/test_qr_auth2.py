import uuid, time
import qrcode
from io import BytesIO
import socket
from flask import Blueprint, session, send_file, render_template, request, redirect
import redis

qr_bp = Blueprint('qr_auth', __name__)
r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

TOKEN_EXPIRY = 300  # 5分钟有效

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip

@qr_bp.route('/qr-auth')
def qr_auth():
    qr_token = str(uuid.uuid4())
    session['qr_token'] = qr_token
    # 存储到 Redis，5分钟有效期
    r.hmset(f"qr:{qr_token}", {
        'verified': 0,
        'created': int(time.time())
    })
    r.expire(f"qr:{qr_token}", TOKEN_EXPIRY)
    return render_template('qr_auth.html', qr_token=qr_token)

@qr_bp.route('/qr-image')
def qr_image():
    qr_token = session.get('qr_token')
    if not qr_token:
        return "No token in session", 400
    local_ip = get_local_ip()
    qr_data = f"http://{local_ip}:5000/confirm?token={qr_token}"
    img = qrcode.make(qr_data)
    buf = BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@qr_bp.route('/confirm')
def confirm_page():
    token = request.args.get("token")
    if not r.exists(f"qr:{token}"):
        return "二维码已过期或无效", 404
    return render_template("confirm.html", token=token)

@qr_bp.route('/verify_qr/<token>', methods=['POST'])
def verify_qr(token):
    if r.exists(f"qr:{token}"):
        r.hset(f"qr:{token}", "verified", 1)
        return "扫码成功，登录已确认！"
    return "二维码无效或已过期", 404

@qr_bp.route('/check_qr')
def check_qr():
    qr_token = session.get('qr_token')
    if not qr_token or not r.exists(f"qr:{qr_token}"):
        return "invalid"
    verified = r.hget(f"qr:{qr_token}", "verified")
    return "verified" if verified == '1' else "pending"
