from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def get_db(db_user, db_password, db_host, db_port, db_name):
    db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_uri)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    return session

def disconnect_db(session):
  session.close()
