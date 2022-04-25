from flask_app import create_app
from config import DevelopmentConfig
from flask_cors import CORS

app = create_app(DevelopmentConfig)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)
