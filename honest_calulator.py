msg_0 = "Enter an equation"

msg_1 = "Do you even know what numbers are? Stay focused!"

msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"

msg_3 = "Yeah... division by zero. Smart move..."

msg_4 = "Do you want to store the result? (y / n):" 

msg_5 = "Do you want to continue calculations? (y / n):"

msg_6 = " ... lazy"

msg_7 = " ... very lazy"

msg_8 = " ... very, very lazy"

msg_9 = "You are"

msg_10 = "Are you sure? It is only one digit! (y / n)"

msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"

msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

memory = 0

def is_one_digit(v):
    
    if v > -10 and v < 10 and v- int(v) == 0:
        return True
    return False
def check(v1,v2,v3):
    msg = ""
    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6
    if (v1 == 1 or v2 == 1) and v3 == "*":
        msg = msg + msg_7
    if (v1 == 0 or v2 == 0) and (v3 == "*" or v3 == '-' or v3 == '+' ):
        msg = msg + msg_8
    if msg !="":
        msg = msg_9 + msg
        print(msg)

def printer(n):
    if n == 10:
        print(msg_10)
    if n == 11:
        print(msg_11)
    if n == 12:
        print(msg_12)
    

def trzecia():
    global memory
    global result
    if is_one_digit(result) == True:
        msg_index = 10
        while(True):
            printer(msg_index)
            ans_3 = input()
            if ans_3 == "y":
                if msg_index < 12:
                    msg_index = msg_index + 1
                else:
                    memory = result
                    break
            else:
                if ans_3 == "n":
                    break
                
        

        

def pierwsza():
    global memory
    global result
    while (True):
        
        print(msg_0)
        calc = input()
        x, oper, y = calc.split(" ")
        if x == "M":
            x = memory
        if y == "M":
            y = memory
        try:
            x = float(x)
            y = float(y)
        except Exception:
            print(msg_1)
        else:
            if oper in ["+", "-", "*", "/"]:
                check(x,y,oper)
                if oper == '+':
                    print(x+y)
                    result = x+y
                    break
                if oper == '-':
                    print(x-y)
                    result = x-y
                    break
                if(oper == '*'):
                    print(x*y)
                    result = x*y
                    break
                if(oper == '/'):
                    try:
                        print(x/y)
                        result = x/y
                        break
                    except ZeroDivisionError:
                        print(msg_3)
                    
                    
            else:
                print(msg_2)
def druga():
    global memory
    global result
    while(True):
        print(msg_4)
        ans_1 = input()
        if ans_1 == "y":
            
            trzecia()
            break
        else:
            if ans_1 == "n":
                break
    while(True):
        print(msg_5)
        ans_2 = input()
        if ans_2 == 'y':
            return 1
        else:
            if ans_2 == 'n':
                return 0
            else:
                break


while(True):
    pierwsza()
    x = druga()
    if x == 0:
        break
        