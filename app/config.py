class Config:
    @staticmethod
    def init_app():
        pass

class DevelopmentConfig(Config):
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= "sqlite:///project.sqlite"

class ProductionConfig(Config):
    DEBUG=False
    SQLALCHEMY_DATABASE_URI= "postgresql://iti:8561@localhost:5432/flaskdb"


projectConfig={
    "dev": DevelopmentConfig,
    'prd': ProductionConfig
}