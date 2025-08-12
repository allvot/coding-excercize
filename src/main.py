from sort import sort

while True:
    print("--------------------------------")
    width = int(input("Input width: "))
    height = int(input("Input height: "))
    length = int(input("Input length: "))
    mass = int(input("Input mass: "))

    print(sort(width, height, length, mass))
    if input("Continue? (y/n) ").lower() == "n":
        break