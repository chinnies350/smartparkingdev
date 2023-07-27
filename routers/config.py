from time import monotonic
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient


# client = MongoClient("103.155.12.18", 38762)
client = MongoClient("mongodb://admin:Prematix%40123@172.17.0.3:27017/?authMechanism=DEFAULT")
# client = MongoClient("192.168.1.19",27017)
db = client['smart_parking']

Base_Url = "http://prematix.tech/smart_parking/"
# Base_Url = "http://192.168.1.19:5020/"
SMS_URL = "http://smsstreet.in/websms/sendsms.aspx"
SMS_API_SAFETY_KEY = "smart-parking"

DQL_DATABASE = (
        r'Driver={ODBC Driver 17 for SQL Server};' 
        r'Server=192.168.1.221;'
        r'Database=smart_parking_main;'
        r'UID=sqldeveloper;'
        r'PWD=SqlDeveloper$;'
        r'MARS_Connection=yes;'
        r'APP=yourapp'
)


engine = create_engine("mssql+pyodbc://sqldeveloper:SqlDeveloper$@192.168.1.221/smart_parking_main?driver=ODBC+Driver+17+for+SQL+Server&Mars_Connection=Yes")
def cursorCommit():
    conn = engine.raw_connection()
    cur = conn.cursor()
    return conn,cur

SessionLocal = sessionmaker(bind=engine, autocommit=True, autoflush=False)


Base = declarative_base()


def get_db():
    db = ()
    try:
        yield db
    finally:
        db.close()
