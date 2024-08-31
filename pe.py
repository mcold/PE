# coding: utf-8
import db
from os import path
import os
from sqlite3 import connect
from os import sep
import typer
import use
import sys
from config import *



db.create_db(con=connect(db_file))

app = typer.Typer()


@app.command(help='Export Item')
def exp(item_name: str) -> None:
    item = db.get_item(item_name=item_name)
    with open(file=os.curdir + f'{os.sep}output{os.sep}' + item.name + '.txt', mode='w', encoding='utf-8') as f:
        f.write(item.__str__())

@app.command(help='Show tree structure of items')
def get_tree(item_name: str) -> None:
    for item in db.get_items(item_name=item_name): print(item.__str__tree__() + '\n')

@app.command(help='Import quests from file')
def imp(file_name: str, item_name: str, stream: str = 'rewrite') -> None:
    if stream not in ['rewrite', 'append']:
        print('\nIncorrect stream type\n')
        sys.exit(0)
    item_db = db.get_item(item_name=item_name)
    item_file = use.get_item_file(file_name=file_name, item_name=item_name)
    if item_db.name:
        item = item_db + item_file
    else:
        item = item_file
    item.save()

@app.command(help='Items list')
def ls():
    for item in db.get_items(): print(item)
