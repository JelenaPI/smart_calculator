from _collections import deque

import string

priority = { '+': 1, '-':1, '*':2,'/':2,'^':3,'(':4,')':4}

def commands(command):
    if command.lower() == "/exit":
        print("Bye!")
        exit(0)
    elif command.lower() == "/help":
        return "The program calculates the sum of number and also difference of number"
    else:
        print('Unknown command')

def convert_to_postfix(data):
    final = []
    operations = deque()
    for x in data:
        if x not in '+-*/^()': # if it is number
            final.append(x)
        elif len(operations) == 0 or x == "(" or (len(operations) > 0 and operations[-1] =='('):
            operations.append(x)
        elif x ==')':
            x = operations.pop()
            while x != '(':
                final.append(x)
                x = operations.pop()
        else:
            while len(operations) > 0 and priority[x] <= priority[operations[-1]] and operations[-1] != '(':
                final.append(operations.pop())
            operations.append(x)
    while len(operations) > 0:
        final.append(operations.pop())
    return final

def correct_input(data):  #  insert space around +-*/(),replace --- with - and -- with +,take value for variables
    if data.startswith('-'):
        data = "0 "+data
    while "---" in data:
        data = data.replace("---", '-')
    while '--' in data:
        data = data.replace('--', '+')
    while '++' in data:
        data = data.replace('++', '+')
    for x in '+-*/()':
        if x in data:
            data = data.replace(x, ' ' + x + " ")
    data = data.split()
    for num in range(len(data)):  # if we have variable stored, we take its valu
        if data[num] in identifier:
            data[num] = identifier[data[num]]
    return data

def calculate(data):
    stack = deque()
    for x in data:
        if x not in '+-*/^':
            stack.append(int(x))
        else:
            if x == '+':
                tmp1 = stack.pop()
                tmp2 = stack.pop()
                tmp = tmp1+tmp2
                stack.append(tmp)
            elif x == '-':
                tmp1 = stack.pop()
                tmp2 = stack.pop()
                stack.append(tmp2-tmp1)
            elif x == '*':
                tmp1 = stack.pop()
                tmp2 = stack.pop()
                tmp = tmp1*tmp2
                stack.append(tmp)
            elif x == '/':
                tmp1 = stack.pop()
                tmp2 = stack.pop()
                if tmp2 != 0:
                    tmp = tmp2/tmp1
                    stack.append(int(tmp))
                else:
                    print('Division by 0')
    return print(stack.pop())

def valid_identifier(word):
    for letter in word:
        if letter in string.ascii_letters:
            continue
        else:
            return False
    return True

def valid_assignment(word):
    if word in identifier:
        return True
    elif word.isnumeric():
        return True
    else:
        return False

def assignment(data):
    data = [x.strip() for x in data.split('=')]
    if valid_identifier(data[0]):
        if len(data) == 2:
            assign = data[1]
            if assign.isnumeric():
                identifier[data[0]] = assign
            elif assign in identifier:
                identifier[data[0]] = identifier[assign]
            elif valid_identifier(assign):
                print('Unknown variable')
            else:
                print("Invalid assignment")
        else:
            print("Invalid assignment")
    else:
        print('Invalid identifier')
    return identifier

def check_parenthesis(data):
    steck = deque()
    tmp = True
    for x in data:
        if x == '(':
            steck.append(x)
        elif x == ')':
            if len(steck) > 0:
                steck.pop()
            else:
                tmp = False
    if len(steck)>0:
        tmp = False
    return tmp

identifier = {}

while True:
    data = input().strip()
    if data == '':
        continue
    if data.startswith('/'):
        commands(data)
    elif "=" in data:
        assignment(data)
    elif valid_identifier(data):
        if data in identifier:
            print(identifier[data])
        else:
            print('Unknown variable')
    else:
        data = correct_input(data)
        if check_parenthesis(data):
            data = convert_to_postfix(data)
            try:
                calculate(data)
            except:
                print('Invalid expression')
        else:
            print('Invalid expression')


