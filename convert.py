# Trabalho realizado por: 66088 - Emanuel Fernandes - MEAer
#                         78450 - Joao Louro - MEAer
#
# Inteligencia Artifical e Sistemas de Decisao, 1.o Semestre 2017/2018

import sys

# open file handling
def file_open():
        file = sys.stdin
        file_lines = file.readlines()
        return file_lines

# file read handling
def read_stdin():
    file_lines = file_open()
    file_list = []
    for line in file_lines:
           file_list.append(line)
    return file_list

# file handling (cleaning)
def clean_element(string):
    clean = string.replace("[", "")
    clean = clean.replace("]", "")
    clean = clean.replace(",", "")
    clean = clean.replace(" ", "")
    return clean

# file handling (cleaning)
def clean_element_rd(string):
    clean = string.replace("(", "")
    clean = clean.replace(")", "")
    clean = clean.replace(",", "")
    clean = clean.replace(" ", "")
    return clean

# file handling (cleaning)
def clean_file(file_list):
    file_formated = []
    for line in file_list:
        size = len(line)-1
        k = 0
        while k < size:
            if line[k] == ',' and line[k+1] != ' ':
                #print(line)
                line = line[:k+1] + ' ' + line[k+1:]
                k += 1
                size += 1
            k += 1
        file_formated.append(line)
    file_formated = [line.replace('(', '[') for line in file_formated]
    file_formated = [line.replace(')', ']') for line in file_formated]
    file_formated = [line.replace("'", "") for line in file_formated]
    return file_formated

# recursive list creation - conjunction of disjunctions
def correctly_into_lists(line):
    operator = clean_element(line[0])
    correct_output = []
    if isdoubleoperator(operator):
        temp1,line = correctly_into_lists(line[1:])
        temp2,line = correctly_into_lists(line)
        correct_output = [operator,temp1,temp2]

    elif operator == 'not':
        temp,line = correctly_into_lists(line[1:])
        correct_output = [operator,temp];

    else:
        correct_output = clean_element(line[0])
        line = line[1:]

    correct_output = [correct_output, line]
    return correct_output

# returns operator in the beginning of line
def oper(line):
    operator = line[0]
    return operator

# check for operator with 1 argument
def isoperator(string):
    if string == 'and':
        return True
    elif string == '<=>':
        return True
    elif string == 'or':
        return True
    elif string == '=>':
        return True
    elif string == 'not':
        return True
    else:
        return False

# check for operators with 2 arguments
def isdoubleoperator(string):
    if string == 'and':
        return True
    elif string == '<=>':
        return True
    elif string == 'or':
        return True
    elif string == '=>':
        return True
    else:
        return False

# recursively, converts a line to cnf
def to_cnf(line):
    # literal handling
    if isoperator(oper(line)) == False:
        return line

    # equivalence handling
    elif oper(line) == "<=>":
        return to_cnf(["and",to_cnf(["=>", line[1], line[2]]),to_cnf(["=>",\
            line[2], line[1]])])

    # implies handling
    elif oper(line) == "=>":
        return to_cnf(["or", to_cnf(["not",line[1]]), to_cnf(line[2])])

    # 'not' handling
    elif oper(line) == 'not':
        # single not
        if len(line[1]) == 1:
            return line
        # not not
        elif oper(line[1]) == "not" and isoperator(line[1][1]) == False:
            return to_cnf(line[1][1])
        # equivalence inside not
        elif oper(line[1]) == "<=>":
            return to_cnf(["or", to_cnf(["not", ["=>", line[1][1],\
                line[1][2]]]), to_cnf(["not", ["=>", line[1][2], line[1][1]]])])
        # '=>' inside line_not
        elif oper(line[1]) == "=>":
            return to_cnf(["not", ["or", to_cnf(["not", to_cnf(line[1][1])]),\
                to_cnf(line[1][2])]])
        # 'or' inside not
        elif oper(line[1]) == "or":
            return to_cnf(["and", to_cnf(["not", line[1][1]]),\
                to_cnf(["not",line[1][2]])])
        # 'and' inside not
        elif oper(line[1]) == "and":
            return to_cnf(["or", to_cnf(["not", line[1][1]]),\
                to_cnf(["not",line[1][2]])])

    # 'or' handling
    elif oper(line) == "or":
        # distributive
        if (not oper(line[2]) == "and") and (oper(line[1]) == "and"):
            return to_cnf(['and', to_cnf(['or', line[1][1], line[2]]),\
                to_cnf(['or', line[1][2], line[2]])])
        # distributive
        if (not oper(line[1]) == "and") and (oper(line[2]) == "and"):
            return to_cnf(['and', to_cnf(['or', line[1], line[2][1]]),\
                to_cnf(['or', line[1], line[2][2]])])
        # distributive
        if oper(line[1]) == "and" and oper(line[2]) == "and":
            return to_cnf(['and', to_cnf(['or', line[1][1], line[2][1]]),\
                to_cnf(['and', ['or', line[1][1], line[2][2]], ['and', ['or',\
                line[1][2], line[2][1]], ['or', line[1][2], line[2][2]]]])])

        clause_aux = ['or', to_cnf(line[1]), to_cnf(line[2])]
        if(line == clause_aux):
            return(line)
        else:
            line = to_cnf(clause_aux)

    # 'and' handling
    elif oper(line) == "and":
        final_line = []
        for counter, logic_op in enumerate(line):
            if counter > 0:
                final_line.append(to_cnf(logic_op))
        final_line.insert(0, "and")
        return final_line

# convert prefix notation (beginning) to infix notation (center)
def centerer(line):
    if oper(line) == "and" or oper(line) == "or":
        return [centerer(line[1]), oper(line), centerer(line[2])]
    else:
        return line

# create output -> to print
def create_output(line):
    line_str = clean_element(str(line))
    #divides the conjunction of disjunctions
    final_output = []

    split = line_str.split("'and'")
    for part in split:
        option = []

        div_or = part.split("'or'")
        for lit in div_or:
            lit = clean_element(lit)
            lit = clean_element_rd(lit)

            if "'not'" in lit:
                option.append("('not'," + lit[-3:] + ")")
            else:
                option.append(lit)
        final_output.append(option)

        for item in final_output:
            checker = False
            for counter1, subitem1 in enumerate(item):
                for counter2, subitem2 in enumerate(item):
                    if len(item[counter2]) < 4:#
                        if ((item[counter2] in item[counter1]) and
                            len(item[counter1]) > 3):
                            checker = True
                            final_output.remove(item)
                            break
                if checker:
                    break
    return final_output

# prints the output
def out_print(output):
    for line in output:
        if len(line)>1:
            print("[", end="")
        if len(line)==1 and len(line[0])==1:
            print("'", end="")
        for counter, element in enumerate(line):
            if counter+1==len(line):
                print(element, end="")
            else:
                print(element+", ", end="")

        if len(line)>1:
            print("]", end="")
        if len(line)==1 and len(line[0])==1:
            print("'", end="")
        print(" ")


# main function

file_list = read_stdin()
file_formated = clean_file(file_list)

file_cut = []
for line in file_formated:
    file_cut.append(line.split())

knowledge_base = []
for line_cut in file_cut:
    knowledge_base.append(correctly_into_lists(line_cut)[0])

output = []
for line in knowledge_base:
    line_l = to_cnf(line)
    line_l = centerer(line_l)
    line_l = create_output(line_l)
    output.extend(line_l)

out_print(output)
