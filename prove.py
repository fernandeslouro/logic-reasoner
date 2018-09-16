# Trabalho realizado por: 66088 - Emanuel Fernandes - MEAer
#                         78450 - Joao Louro - MEAer
#
# Inteligencia Artifical e Sistemas de Decisao, 1.o Semestre 2017/2018

import sys
from copy import copy

# open file handling
def file_open():
    file = sys.stdin
    file_lines = file.readlines()

    return file_lines

# file handling (cleaning)
def clean_lines(file_lines):
    for n in reversed(range(file_lines.__len__())):
        file_lines[n] = file_lines[n].replace(" ","")
        file_lines[n] = file_lines[n].replace('\r','')
        file_lines[n] = file_lines[n].replace('\n','')
        file_lines[n] = file_lines[n].replace('\t','')
        if file_lines[n]:
            if (file_lines[n][0] == "'" or
                file_lines[n][0] == "(" or
                file_lines[n][0] == "["):

                file_lines[n] = file_lines[n].replace("'","")
                file_lines[n] = file_lines[n].replace("’","")
                continue
        #remove empty spaces
        del file_lines[n]

# append a literal to knowledge base
def append_literal(KB, line):
    if line[0] == '(':
        #negation
        line = line.replace("(","")
        line = line.replace(")","")
        line = line.replace("not,","!")
        KB.append([line])
    else:
        #atom
        KB.append([line])

# append a clause to knowledge base
def append_clause(KB, line):
    line = line.replace("[","")
    line = line.replace("]","")

    split_raw = line.split(",")
    new_clause = []
    for n in range(split_raw.__len__()):
        if split_raw[n][0] == "(" and split_raw[n+1][-1] == ")":
            new_clause.append("!" + split_raw[n+1].replace(")",""))
        else:
            if split_raw[n][-1] == ")":
                continue
            else:
                new_clause.append(split_raw[n])

    KB.append(new_clause)

#returns the complementary literal: if positive, adds '!' prefix, and vice-versa
def return_complementary(literal):
    if literal[0] == "!":
        return literal[1:]
    else:
        return "!"+literal

#check if C2 contains at least one complement of one of the literals of C1
def check4compl(C1, C2):
    foundit = False
    for literal_1 in C1:
        literal_compl = return_complementary(literal_1)
        if literal_compl in C2:
            foundit = True
            break
    return foundit

#check for tautology
def is_tautology(clause):
    return check4compl(clause, clause)

#simplification 4 - remove repeated literals in clause
def rem_rep(clause):
    out_clause = []
    for literal in clause:
        if literal not in out_clause:
            out_clause.append(literal)
    return out_clause
    
def resolution(C1, C2):
    if C1.__len__() < C2.__len__():
        Ci = C1
        Cj = C2
    else:
        Ci = C2
        Cj = C1
    
    resolvent = Ci + Cj

    done = False
    j = resolvent.__len__()-1# = len(Ci)+len(Cj)-1
    Ci_len = Ci.__len__()
    while j > Ci_len-1:
        i = Ci_len-1
        while i >= 0:
            if resolvent:
                if resolvent[i] == return_complementary(resolvent[j]):
                    if resolvent.__len__() > 2:
                        del resolvent[j]
                        del resolvent[i]
                        Ci_len -= 1
                        j -= 2
                        i += 1
                    else:
                        #if not tautology by single clause:
                        if Ci_len == 1 and Cj.__len__() == 1:
                            del resolvent[j]
                            del resolvent[i]
                            Ci_len -= 1
                            j -= 2
                            i += 1
            else:
                #empty, conclusion reached!
                done = True
                break
            i -= 1
        if done:
            break
        j -= 1

    #simplification 4 (factoring): remove repeated literals in clause
    resolvent = rem_rep(resolvent)

    return resolvent

def is_subset(new_C ,C):
    found_dif = False
    for new_clause in new_C:
        found_dif = True
        for clause in C:
            if sorted(clause) == sorted(new_clause):
                found_dif = False
                break
        if found_dif:
            break
    return not found_dif

def is_present(clause, set_clauses):
    for c in set_clauses:
        if sorted(c) == sorted(clause):
            return True
    return False

def extend_C(C, new_C):
    out_C = []
    out_C.extend(C)
    for clause in new_C:
        if not is_present(clause, C):
            out_C.append(clause)
    return out_C



# main function

#file open and read
file_lines = file_open()

# clean the lines read
clean_lines(file_lines)

# dividir, verificar e adicionar à KB
KB = []
for line in file_lines:
    if line[0] == '[':
        #clause
        append_clause(KB, line)
    else:
        #literal
        append_literal(KB, line)

C = copy(KB)

C2 = []
for clause in C:    
    clause = rem_rep(clause)
    C2.append(clause)
C = C2

new_C = []

#num_iter = 0

C_len = C.__len__()
end = False
while True:
    C.sort(key = len, reverse = True)
    
    #for i in reversed(range(0, C_len)):#theorem is the last, should be faster
    i = C_len-1
    while i >= 0:
        C1 = C[i]
        if is_tautology(C1):
            del C[i]
            C_len = C.__len__()
            i -= 1
            continue

        #for j in reversed(range(0, i)):
        j = i-1
        while j >= 0:
            C2 = C[j]

            if is_tautology(C2):
                del C[j]
                C_len = C.__len__()
                i -= 1
                j -= 1
                continue

            if check4compl(C1, C2):
                resolvent = resolution(C1, C2)
                if not resolvent:
                    #oh yeah, descobrimos o vazio, return True!
                    print("True")
                    end = True
                    break
                if not is_tautology(resolvent):#do not append single tautologies
                    if not is_present(resolvent, new_C):
                        #only append unique new clauses
                        new_C.append(resolvent)
            j -= 1
        if end:
            break
        i -= 1

    #num_iter += 1

    if end:
        break

    if is_subset(new_C, C):
        print("False")
        break

    C = extend_C(C, new_C)
    C_len = C.__len__()

#print("num_iter =", num_iter)
#print("sum_b =", new_C.__len__())
#print("avg_b =", float(new_C.__len__())/num_iter)
