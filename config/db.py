from sqlalchemy import create_engine, MetaData

DATABASE_URL = "postgresql://postgres:admin@localhost/fastApi"

engine = create_engine(DATABASE_URL)

#conn = engine.connect()

meta_data = MetaData()

