from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Connect Database Helper Method
def get_db(db_user, db_password, db_host, db_port, db_name):
    db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_uri)
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = Session()
    return session
