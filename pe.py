# coding: utf-8
import db
import os
from sqlite3 import connect
import typer
import use
from config import *
import re


db.create_db(con=connect(db_file))

app = typer.Typer()


def imp_file(file_name: str, item_name: str) -> None:
    item_db = db.get_item(item_name=item_name)
    item_file = use.get_item_file(file_name=file_name, item_name=item_name)
    if item_db.name:
        item = item_db + item_file
    else:
        item = item_file
    item.save()

@app.command(help='Export Item')
def exp(item_name: str) -> None:
    item_content = db.get_item(item_name=item_name).__str__().replace('👆', '"').replace("👇", "'")
    l_res = list()
    for line in item_content.split('\n'):
        l_res.append(re.sub(r'\.{3,}', '🔥🔥🔥🔥', line))
    with open(file = os.curdir + f'{os.sep}{dir_export}{os.sep}' + item_name + '.txt', mode='w', encoding='utf-8') as f:
        f.write('\n'.join(l_res))


@app.command(help='Show tree structure of items')
def get_tree(item_name: str) -> None:
    for item in db.get_items(item_name=item_name): print(item.__str__tree__() + '\n')

@app.command(help='Import quests from file')
def imp(item_name: str) -> None:
    input_dir = os.curdir + f'{os.sep}{dir_input}'
    output_dir = os.curdir + f'{os.sep}{dir_output}' 
    for f in os.listdir(input_dir):
        imp_file(file_name=f'{input_dir}{os.sep}{f}', item_name=item_name)
        os.replace(f'{input_dir}{os.sep}{f}', f'{output_dir}{os.sep}{f}') 

@app.command(help='Items list')
def ls():
    for item in db.get_items(): print(item)
