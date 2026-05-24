from peewee import *
import os

db_dir = "/app/db_folder"
if not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

# Point Peewee directly inside the shared volume path
db = SqliteDatabase(os.path.join(db_dir, "app.db"))
#db = SqliteDatabase('translations.db')

class User(Model):
    username = CharField(unique=True) 
    hashed_password = CharField()

    class Meta:
        database = db

class TranslationalModel(Model):
    user = ForeignKeyField(User, backref='translations', null=True) 
    text = TextField()
    base_lang = CharField()
    final_lang = CharField()
    translation = TextField(null=True)

    class Meta:
        database = db

def create_db():
    db.connect()
    db.create_tables([User, TranslationalModel])
    db.close()

create_db()