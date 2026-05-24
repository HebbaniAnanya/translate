from peewee import *

db = SqliteDatabase('translations.db')

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

create_db()