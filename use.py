# coding: utf-8
import db
import string


def set_correct_ans(quest: db.Quest, l: list) -> db.Quest:
    l_ans = list()
    for i in range(len(quest.l_ans)):
        ans = quest.l_ans[i]
        if string.ascii_uppercase[i] in l:
            ans.is_correct = True
            l_ans.append(ans)
        else:
            ans.is_correct = False
            l_ans.append(ans)

    quest.l_ans = l_ans
    return quest

def get_item_file(file_name: str, item_name: str) -> db.Item:
    """
        Get Item from file
    """
    with open(file=file_name, mode='r', encoding='utf-8') as f:
        l_lines = f.readlines()
        b_exam = False
        b_testlet = False
        b_quest = False
        b_ans = False
        b_exp = False
        item = db.Item(tuple())
        ex = db.Exam(tuple())
        qset = db.QSet(tuple())
        quest = db.Quest(tuple())
        ans = db.Ans(tuple())
        exp = db.Exp(tuple())

        item.name = item_name
        for line in l_lines:
            if len(line.strip()) > 0:
                line = line.replace("'", '').replace('"', '')

                if line.lower().startswith('exam'):
                    if b_exam:
                        if b_testlet:
                            if b_quest:
                                if b_ans: 
                                    quest.l_ans.append(ans)
                                    ans = db.Ans(tuple())
                                if b_exp: 
                                    quest.exp = exp
                                    exp = db.Exp(tuple())
                                qset.l_quests.append(quest)
                        b_testlet = False
                        b_quest = False
                        b_ans = False
                        b_exp = False
                        
                        ex.l_sets.append(qset)
                        item.l_exams.append(ex)
                        qset = db.QSet(tuple())
                            
                    b_exam = True
                    ex = db.Exam(tuple())
                    ex.name = line[5:].lstrip(':').strip()
                    continue

                if line.lower().startswith('testlet'):
                    if b_testlet:
                        if b_quest:
                            if b_ans: 
                                quest.l_ans.append(ans)
                                ans = db.Ans(tuple())
                            if b_exp: 
                                quest.exp = exp
                                exp = db.Exp(tuple())
                            qset.l_quests.append(quest)
                        b_quest = False
                        b_ans = False
                        b_exp = False
                        ex.l_sets.append(qset)
                    else:
                        b_testlet = True
                    qset = db.QSet(tuple())
                    qset.name = line[8:].lstrip(':').strip()
                    continue

                if line.lower().startswith('question'):
                    if b_quest:
                        if b_ans:
                            quest.l_ans.append(ans)
                            ans = db.Ans(tuple())
                        if b_exp: 
                            quest.exp = exp
                            exp = db.Exp(tuple())
                        b_ans = False
                        b_exp = False
                        
                        qset.l_quests.append(quest)

                    b_quest = True
                    b_ans = False
                    b_exp = False
                    quest = db.Quest(tuple())
                    quest.content = line[11:].strip().lstrip(':').strip()
                    continue

                if line.split('.')[0] in list(string.ascii_uppercase) and len(line.split('.')[0]) == 1:
                    if b_ans: quest.l_ans.append(ans)
                    b_ans = True
                    ans = db.Ans(tuple())
                    ans.content = '.'.join(line.split('.')[1:]).strip()
                    continue

                if line.lower().startswith('correct answer'):
                    quest.l_ans.append(ans)
                    l_correct_ans = [x.strip() for x in line.split(':')[-1].split(',')]
                    quest = set_correct_ans(quest=quest, l=l_correct_ans)
                    b_ans = False
                    b_exp = False
                    continue

                if line.lower().startswith('explanation'):
                    b_ans = False
                    b_exp = True
                    exp = db.Exp(tuple())
                    if len(line.strip()) > 14: 
                        exp.content = line[13:].strip()
                    
                    continue

                ### BOOLS ###
                if b_exam:
                    if b_testlet:
                        if b_quest:
                            if b_ans:
                                if len(ans.content) > 0:
                                    ans.content += '\n' + line
                                else:
                                    ans.content = line.strip()
                                continue
                            if b_exp:
                                if len(exp.content) > 0:
                                    exp.content += '\n' + line.strip()
                                else:
                                    exp.content = line.strip()
                                continue
                            
                            continue
        if b_exam:
            if b_testlet:
                if b_quest:
                    if b_ans:
                        if len(ans.content) > 0:
                            ans.content += '\n' + line
                        else:
                            ans.content = line.strip()
                    if b_exp:
                        if len(exp.content) > 0:
                            exp.content += '\n' + line.strip()
                        else:
                            exp.content = line.strip()
                    qset.l_quests.append(quest)
                ex.l_sets.append(qset)
            item.l_exams.append(ex)
    return item
