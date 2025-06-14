from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL='postgresql://postgres:0527480034i@localhost/fastapi'

engine=create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn=psycopg2.connect(host='localhost',database='fastapi',user='postgres',
#         password='0527480034i',cursor_factory=RealDictCursor)
#         cursor=conn.cursor()
#         print("Connecting to database was Successful! ")
#         break
        
        
#     except Exception as error:
#         print("Connecting to database was failed")
#         print("Error:",error) 
#         time.sleep(2) #If the connection is unstable.
