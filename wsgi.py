from app.word import create_app
from app.settings import ProdConfig

app = create_app(ProdConfig)

if __name__ == '__main__':
    app.run()
