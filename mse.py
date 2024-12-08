text = input("Enter a number: ")
num = int(text)
for row in range(num):
    for col in range(num):
        if (row + col) % 2 == 0:
            print("**", end="")
        else:
            print("  ", end="")
    print()
