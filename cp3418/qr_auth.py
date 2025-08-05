import uuid
from flask import Blueprint, session, url_for, render_template, send_file, request, jsonify
import qrcode
from io import BytesIO
import datetime
import requests
from flask import redirect, render_template_string

qr_bp = Blueprint('qr_auth', __name__, url_prefix='/qr-auth')


# { qr_token: { 'confirmed': bool, 'user': {id, email, fullname} or None } }
qr_sessions = {}

@qr_bp.route('/')
def qr_auth():
    qr_token = str(uuid.uuid4())
    session['qr_token'] = qr_token
    qr_sessions[qr_token] = {'confirmed': False, 'user': None}
    return render_template('qr.html', qr_token=qr_token)

@qr_bp.route('/qr-code')
def qr_code():
    qr_token = session.get('qr_token')
    if not qr_token:
        return "Missing token", 400

    qr_url = request.host_url.rstrip('/') + url_for('qr_auth.qr_login', token=qr_token)
    img = qrcode.make(qr_url)
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    return send_file(buffer, mimetype='image/png')

def get_geo_location(ip):
    if ip.startswith('127.') or ip == '::1':
        return "Localhost - Development"
    try:
        response = requests.get(f'https://ipapi.co/{ip}/json/')
        data = response.json()
        print(data)
        city = data.get('city', '')
        region = data.get('region', '')
        country = data.get('country_name', '')
        location = ', '.join(part for part in [city, region, country] if part)
        return location if location else "Unknown"
    except:
        return "Unknown"



@qr_bp.route('/login/<token>')
def qr_login(token):
    if token not in qr_sessions:
        return "Invalid QR code link", 404

    user_ip = request.remote_addr
    login_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    location = get_geo_location(user_ip)

    return render_template(
        'qr_auth.html',
        token=token,
        ip_address=user_ip,
        login_time=login_time,
        location=location
    )


@qr_bp.route('/confirm/<token>', methods=['POST'])
def confirm(token):
    if token not in qr_sessions:
        return jsonify({'success': False, 'message': 'invalid token'})

    data = request.get_json()
    reasons = data.get('reasons', [])

    # Backend validation logic: "It’s a map app" must be selected and can only be selected.
    if reasons != ["It’s a map app"]:
        return jsonify({'success': False, 'message': 'Invalid authorization reason'}), 403

    user = {
        'id': 1,
        'email': 'test@example.com',
        'fullname': 'Test User'
    }
    qr_sessions[token]['confirmed'] = True
    qr_sessions[token]['user'] = user
    return jsonify({'success': True})

@qr_bp.route('/check-login')
def check_login():
    token = session.get('qr_token')
    if not token or token not in qr_sessions:
        return jsonify({'logged_in': False})

    info = qr_sessions[token]
    if info.get('confirmed'):
        session['user'] = info['user']
        qr_sessions.pop(token)
        session.pop('qr_token', None)
        return jsonify({'logged_in': True})

    return jsonify({'logged_in': False})
