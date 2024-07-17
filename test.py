from flask import Flask

app = Flask(__name__)

# 根路径
@app.route('/')
def index():
    return 'Welcome to the main page!'

@app.route('/about')
def about():
    return 'About page'

@app.route('/contact')
def contact():
    return 'Contact page'

if __name__ == '__main__':
    app.run(port=5000)  # 设置端口号为5000，可以根据需要修改


