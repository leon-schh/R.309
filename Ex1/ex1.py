def divEntier(x: int, y: int) -> int:
    if x < y:
        return 0
    else:
        x = x - y
        return divEntier(x, y) + 1

if __name__ == '__main__':
    while True:
        try:
            x = int(input("Quelle est la veleur de x ? : "))
            y = int(input("Quelle est la veleur de y ? : "))
            print (divEntier(x,y))
        except ValueError :
            print(f"please enter a float ")
        except RecursionError:
            print(f"y should not be 0 ")
        else: 
            break
        