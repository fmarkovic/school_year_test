from flask_app import create_app
from config import DevelopmentConfig
from flask_cors import CORS
from flask import redirect, url_for

app = create_app(DevelopmentConfig)
CORS(app)

@app.route('/')
def root():
    return redirect(url_for('auth.login'))


if __name__ == '__main__':
    app.run(debug=True)
