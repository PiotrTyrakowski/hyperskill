import random
def pencils():
    print("""How many pencils would you like to use:""")
    while (True):

        n = input()
        if n == '0':
            print("The number of pencils should be positive")
        else:
            try:
                n = int(n)
                if n < 0:
                    print("The number of pencils should be numeric")
                else:
                    return n
            except:
                print("The number of pencils should be numeric")


def choose_names():
    global names
    names = ['John', 'Jack']

    while (True):
        print(f"Who will be the first ({names[0]}, {names[1]}):")
        name = input()
        if name in names:
            if name == names[1]:
                return 1
            else:
                return 0
        else:
            print(f"Choose between '{names[0]}' and '{names[1]}'")


def game(cnt_, n_):
    while (n_ > 0):
        print(f"{names[cnt_ % 2]}'s turn:")
        if cnt_ % 2 == 0:
            while(True):
                x = input()
                if x not in ['1', '2', '3']:
                    print("Possible values: '1', '2' or '3'")
                elif n_ - int(x) < 0:
                    print("Too many pencils were taken")
                else:
                    break
            n_ = n_ - int(x)
        else:
            if n_%4 >= 2:
                x = n_%4 - 1
            if n_%4 == 1:
                if n_ == 1:
                    x = 1
                else:
                    x = random.randint(1, 3)
            if n_%4 == 0:
                x = 3
            print(x)
            n_ = n_ - x
        
        if n_ == 0:
            print(f"{names[ (cnt_ + 1) % 2]} won!")
            break
        else:
            print(n_ * '|')
            cnt_ = cnt_ + 1





n = pencils()
cnt = choose_names()
print(n * "|")
game(cnt, n)