# coding: utf-8
import db
from os import path
from sqlite3 import connect
import typer

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
def imp_data(file_name: str, item_name: str, exam_name: str = None) -> None:
    # TODO
     with open(file=file_name, mode='r', encoding='utf-8') as f:
        l_lines = f.readlines()
        for line in l_lines:
            if line.lower().startswith('exam'):
                ex = db.Exam(tuple())
                ex.name = line[5:].lstrip(':').strip()
                continue
            if line.lower().startswith('set'):
                qset = db.QSet(tuple())
                qset.name = line[4:].lstrip(':').strip()
                ex.l_sets.append(qset)
                continue
            if line.lower().startswith('question'):
                quest = db.Quest(tuple())
                quest.name = line[9:].lstrip(':').strip()
            if quest:
                # TODO
                pass
    

@app.command(help='Items list')
def ls():
    for item in db.get_items(): print(item)
