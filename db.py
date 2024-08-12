# coding: utf-8
from sqlite3 import connect
import string

db = 'DB.db'


# TODO: save: если quest уже существует -> заново сохранить ответ и объяснение
# TODO: section saving and getting

"""
Exam [Name]

Set [Name]

Question 1
[Content]

A. [Content]
B. [Content]
C. [Content]

Correct answer: A,B
Section: First section

Explanation:
[Content]

"""

class Typing:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_quest = t[1]
            self.content = t[2]
        else:
            self.id = None
            self.id_quest = None
            self.content = ''

    def __str__(self):
        return self.content

    def drop(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from typing
                             where id = {self.id}""")
            conn.commit()

    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
                
            cur.execute(f"""insert into typing(id_quest, content)
                              values({self.id_quest}, '{self.content}')
                            returning id
                        """)

            self.id = cur.fetchone()[0]

class Ans:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_quest = t[1]
            self.content = t[2]
            self.is_correct = t[3]
        else:
            self.id = None
            self.id_quest = None
            self.content = ''
            self.is_correct = False

    def __str__(self):
        return self.content

    def drop(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from ans
                             where id = {self.id}""")
            conn.commit()

    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
            if self.is_correct:
                val = 1
            else:
                val = 0
                
            cur.execute(f"""insert into ans(id_quest, content, is_correct)
                              values({self.id_quest}, '{self.content}', {val})
                            returning id
                        """)

            self.id = cur.fetchone()[0]

class Exp:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_quest = t[1]
            self.content = t[2]
        else:
            self.id = None
            self.id_quest = None
            self.content = ''

    def __repr__(self) -> str:
        return 'Explanation:\n' + self.content + '\n'
    
    def __str__(self) -> str:
        return 'Explanation:\n' + self.content + '\n'
    
    def drop(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from exp 
                             where id = {self.id}""")
            conn.commit()

    def save(self):
        if len(self.content.strip()) > 0:
            with connect(db) as conn:
                cur = conn.cursor()
                cur.execute(f"""insert into exp(id_quest, content)
                                values({self.id_quest}, '{self.content}')
                                returning id
                            """)
                self.id = cur.fetchone()[0]

class Section:

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.name = t[1]

            # self.l_quests = self.get_quests()
        else:
            self.id = None
            self.name = ''

            self.l_quests = list()

    def __repr__(self) -> str:
        return 'Section: ' + self.name
    
    def __str__(self) -> str:
        return 'Section: ' + self.name
    
    def drop(self) -> None:
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from section
                             where id = {self.id}""")
            conn.commit()
    
    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""insert into section(name)
                              values('{self.name}')
                              on conflict do nothing
                            returning id
                        """)
            l = cur.fetchall()
            if len(l) > 0: 
                self.id = l[0][0]
                return
            
            cur.execute(f"""select id 
                              from section
                             where name = '{self.name}'
                        limit 1
                        """)
            self.id = cur.fetchone()[0]
            return

class Quest:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_set = t[1]
            self.id_section = t[2]
            self.content = t[3].replace("'", '').replace('"', '')

            if self.id_section:
                self.section = self.get_section()
            else:
                self.section = Section(tuple())

            self.l_ans = self.get_ans()
            self.typing = self.get_typing()
            self.exp = self.get_exp()
        else:
            self.id = None
            self.id_set = None
            self.id_section = None
            self.content = ''
            self.section = Section(tuple())
            self.l_ans = list()
            self.typing = Typing(tuple())
            self.exp = Exp(tuple())

    def __repr__(self) -> str:
        res = 'Question ' + self.content + '\n\n'

        n_char = 65
        l_correct_char = list()
        for ans in self.l_ans:
            c_char = chr(n_char)
            res += c_char + '. ' + ans.content + '\n'
            if ans.is_correct: l_correct_char.append(c_char)
            n_char += 1

        # answers
        res +=  self.get_correct_str() + '\n'
        if self.section.id: res += '\n' + self.section.__repr__()
        if self.exp: res += '\n\n' + self.exp.__repr__()

        return res
    
    def __str__(self) -> str:
        res = self.content + '\n\n'
        if len(self.l_ans) > 0:
            for i in range(len(self.l_ans)): res += f'{string.ascii_uppercase[i]}. ' + self.l_ans[i].__str__() + '\n'
            res += '\n'

            res += self.get_correct_str()
        else:
            res += f'Correct answer: {self.typing.content}\n'
        
        if self.section.id: res += '\n' + self.section.__str__()
        if self.exp: res += '\n\n' + self.exp.__str__()
        return res

    def drop(self) -> None:
        for ans in self.l_ans: ans.drop()
        if self.exp: self.exp.drop()
        if self.typing.id: self.typing.drop()
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from quest 
                             where id = {self.id}""")
            conn.commit()

    def get_ans(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_quest,
                                  content,
                                  is_correct
                             from ans
                            where id_quest = {id}
                            order by id""".format(id = self.id))
        return [Ans(result) for result in cur.fetchall()]
    
    def get_correct_str(self):
        n_char = 65
        l_correct_char = list()
        for ans in self.l_ans:
            c_char = chr(n_char)
            if ans.is_correct: l_correct_char.append(c_char)
            n_char += 1

        res = 'Correct answer: ' + ', '.join(l_correct_char) 
        return res
    
    def get_exp(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_quest,
                                  content
                             from exp
                            where id_quest = {id}""".format(id = self.id))
        res = cur.fetchone()
        if res:
            return Exp(res)
        else:
            return None

    def get_section(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  name
                             from section
                            where id = {id}
                            """.format(id = self.id_section))
        res = cur.fetchone()
        if res[0]:
            return Section(res)
        else:
            return Section(tuple())
    
    def get_typing(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_quest,
                                  content
                             from typing
                            where id_quest = {id_quest}
                            """.format(id_quest = self.id))
        res = cur.fetchone()
        if res: return Typing(res)
        else: return Typing(tuple())
    
    def save(self):
        b_no_section = True
        if self.section.name:
            if not self.section.id:
                b_no_section = False
                self.section.save()
                self.id_section = self.section.id
        
                with connect(db) as conn:
                    cur = conn.cursor()
                    cur.execute(f"""insert into quest(id_set, id_section, content)
                                    values({self.id_set}, {self.id_section}, '{self.content}')
                                    on conflict do nothing
                                    returning id
                                """)
                    self.id = cur.fetchone()[0]
            else:
                b_no_section = True
        else:
            b_no_section = True

        if b_no_section:
            with connect(db) as conn:
                cur = conn.cursor()
                cur.execute(f"""insert into quest(id_set, content)
                                values({self.id_set}, '{self.content}')
                                on conflict do nothing
                                returning id
                            """)
                self.id = cur.fetchone()[0]

        for ans in self.l_ans: 
            ans.id_quest = self.id
            ans.save()

        if self.exp:
            self.exp.id_quest = self.id
            self.exp.save()
        
        if self.typing:
            if self.typing.content:
                self.typing.id_quest = self.id
                self.typing.save()
                    

class QSet:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_exam = t[1]
            self.name = t[2]

            self.l_quests = self.get_quests()
        else:
            self.id = None
            self.id_exam = None
            self.name = None
            self.l_quests = list()

    def __repr__(self) -> str:
        res = '\nTestlet ' + self.name + '\n'
        for i in range(len(self.l_quests)): res += 'Question ' + str(i+1) + ' ' + self.l_quests[i].__str__() + '\n\n'
        return  res
    
    def __str__(self) -> str:
        res = '\nTestlet ' + self.name + '\n'
        for i in range(len(self.l_quests)): res += 'Question ' + str(i+1) + ' ' + self.l_quests[i].__str__() + '\n\n'
        return  res

    def __str__tree__(self) -> str:
        return self.name + '\n'

    def drop(self) -> None:
        for quest in self.l_quests: quest.drop()
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from qset 
                             where id = {self.id}""")
            conn.commit()

    def get_quests(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_set,
                                  id_section,
                                  content  
                             from quest
                            where id_set = {id}
                            order by id""".format(id = self.id))
        return [Quest(result) for result in cur.fetchall()]
    
    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""insert into qset(id_exam, name)
                              values({self.id_exam}, '{self.name}')
                            on conflict do nothing
                            returning id
                        """)
            self.id = cur.fetchone()[0]
        for quest in self.l_quests: 
            quest.id_set = self.id
            quest.save()


class Exam:

    def __init__(self, t: tuple):
        if len(t) > 0:
            self.id = t[0]
            self.id_item = t[1]
            self.name = t[2]

            self.l_sets = self.get_qsets()
        else:
            self.id = None
            self.id_item = None
            self.name = None
            self.l_sets = list()

    def __repr__(self) -> str:
        return '\nExam ' + self.name + '\n' + '\n'.join([x.__repr__() for x in self.l_lets])

    def __str__(self) -> str:
        return 'Exam ' + self.name + '\n' + '\n'.join([x.__str__() for x in self.l_sets])

    def __str__tree__(self) -> str:
        return self.name + '\n' + '\n\t\t'.join([qset.__str__tree__() for qset in self.l_sets])

    def drop(self) -> None:
        for tlet in self.l_sets: tlet.drop()
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from exam 
                             where id = {self.id}""")
            conn.commit()

    def get_qsets(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_exam,
                                  name
                             from qset
                            where id_exam = {id}
                            order by id""".format(id = self.id))
        return [QSet(result) for result in cur.fetchall()]

    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""insert into exam(id_item, name)
                              values({self.id_item}, '{self.name}')
                            on conflict do nothing
                            returning id
                        """)
            self.id = cur.fetchone()[0]
        for tlet in self.l_sets: 
            tlet.id_exam = self.id
            tlet.save()

class Item:

    def __init__(self, t: tuple, from_db: bool = False):
        if len(t) > 0:
            self.id = t[0]
            self.name = t[1]

            if from_db:
                self.l_exams = self.get_exams()
            else:
                self.l_exams = list()
        else:
            self.id = None
            self.name = None
            self.l_exams = list()

    def __repr__(self) -> str:
        return '\n'.join(self.l_exams)
    
    def __str__(self) -> str:
        return '\n'.join([x.__str__() for x in self.l_exams])
    
    def __str__tree__(self) -> str:
        return self.name + '\n' + '\n\t'.join([ex.__str__tree__() for ex in self.l_exams])
    
    def drop(self) -> None:
        for ex in self.l_exams: ex.drop()
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""delete 
                              from item 
                             where id = {self.id}""")
            conn.commit()

    def get_exams(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute("""select id,
                                  id_item,
                                  name
                             from exam
                            where id_item = {id}
                            order by id""".format(id = self.id))
        return [Exam(result) for result in cur.fetchall()]
    
    def save(self):
        with connect(db) as conn:
            cur = conn.cursor()
            cur.execute(f"""insert into item(name)
                              values('{self.name}')
                            on conflict do nothing
                            returning id
                        """)
            self.id = cur.fetchone()[0]
        for exam in self.l_exams: 
            exam.id_item = self.id
            exam.save()

def get_exam(id_item: int, exam_name: str) -> Exam:
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""select id,
                              id_item,
                              name
                         from exam
                        where lower(name) = lower('{name}')
                        limit 1
                    """.format(name = exam_name, id_item = id_item))
        l = cur.fetchall()
        if len(l) > 0: return Exam(l[0])
        else: return Exam(tuple())

def get_item(item_name: str = None) -> Item:
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""select id,
                              name
                         from item
                        where lower(name) = lower('{name}')
                        order by lower(name)
                        limit 1
                    """.format(name = item_name))
        l = cur.fetchall()
        if len(l) > 0: return Item(l[0], from_db=True)
        else: return Item(tuple())

def get_items(item_name: str = None) -> list:
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""select id,
                              name
                         from item
                        where lower(name) like lower('{name}')
                        order by name
                    """.format(name = item_name))
        l = cur.fetchall()
        if len(l) > 0: return [Item(x) for x in l]
        else: return []

def get_section(name: str) -> Section:
    with connect(db) as conn:
        cur = conn.cursor()
        cur.execute("""select id,
                              name
                         from section
                        where lower(name) = lower('{name}')
                        limit 1
                    """.format(name = name))
        l = cur.fetchall()
        if len(l) > 0: return Section(l[0])
        else: return Section(tuple())


def create_db(con: connect) -> None:
    cur = con.cursor()
    cur.execute("""
                    create table item (id   integer primary key autoincrement,
                                       name text not null unique);
                """)
    cur.execute("""
                    create table exam (id       integer primary key autoincrement,
                                       id_item  integer references item(id),
                                       name     text not null unique);
                """)
    cur.execute("""
                    create table qset (id        integer primary key autoincrement,
                                       id_exam   integer references exam(id),
                                       name      text not null unique);
                """)
    cur.execute("""
                    create table section (id    integer primary key autoincrement,
                                          name  text not null unique);
                """)
    cur.execute("""
                    create table quest (id          integer primary key autoincrement,
                                        id_set      integer references qset(id),
                                        id_section  integer references section(id),
                                        content     text not null);
                """)
    cur.execute("""
                    create table ans (id            integer primary key autoincrement,
                                      id_quest      integer references quest(id),
                                      content       text not null,
                                      is_correct    integer not null default 0);
                """)
    cur.execute("""
                    create table exp (id        integer primary key autoincrement,
                                      id_quest  integer references quest(id),
                                      content   text not null);
                """)
    cur.execute("""
                    create table typing (id        integer primary key autoincrement,
                                        id_quest   integer references quest(id),
                                        content    text not null);
                """)
