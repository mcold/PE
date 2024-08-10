# coding: utf-8
import db
from os import path
from sqlite3 import connect
import typer
import use


db_file = 'DB.db'


if not path.exists(db_file): db.create_db(con=connect(db_file))

app = typer.Typer()


@app.command(help='Generate Item collection test by item name')
def gen_item(item_name: str) -> None:
    for item in db.get_item(item_name=item_name):
        with open(file=item.name + '.txt', mode='w', encoding='utf-8') as f:
            f.write(item.__repr__())

@app.command(help='Import quests from file')
def get_tree(item_name: str) -> None:
    for item in db.get_items(item_name=item_name): print(item.__str__tree__() + '\n')

@app.command(help='Import quests from file')
def imp_data(file_name: str, item_name: str) -> None:
    item_file = use.get_item_file(file_name=file_name, item_name=item_name)
    

@app.command(help='Items list')
def ls():
    for item in db.get_items(): print(item)
