from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

import datetime
import os

database_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),'data.db')

engine = create_engine('postgresql://postgres:jamsekine618@localhost:5433/postgres')

#declarative_baseのインスタンス生成する
Base = declarative_base()

SessionClass = sessionmaker(engine)
session = SessionClass()

#データベースの初期化
def init_db():
    # modelsをインポート
    import assets.models
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)