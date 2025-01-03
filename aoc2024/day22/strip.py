from collections import Counter


lines = [
    "23 XOR 17 XOR 12 XOR 6 XOR 17 XOR 11",
    "22 XOR 16 XOR 11 XOR 5 XOR 16 XOR 10",
    "21 XOR 15 XOR 10 XOR 4 XOR 15 XOR 9",
    "20 XOR 14 XOR 9 XOR 3 XOR 14 XOR 8",
    "19 XOR 13 XOR 8 XOR 2 XOR 13 XOR 7",
    "18 XOR 12 XOR 23 XOR 17 XOR 7 XOR 1 XOR 12 XOR 6",
    "17 XOR 11 XOR 22 XOR 16 XOR 6 XOR 0 XOR 11 XOR 5",
    "16 XOR 10 XOR 21 XOR 15 XOR 5 XOR 10 XOR 4",
    "15 XOR 9 XOR 20 XOR 14 XOR 4 XOR 9 XOR 3",
    "14 XOR 8 XOR 19 XOR 13 XOR 3 XOR 8 XOR 2",
    "13 XOR 7 XOR 18 XOR 12 XOR 2 XOR 7 XOR 1",
    "12 XOR 6 XOR 17 XOR 11 XOR 1 XOR 6 XOR 0",
    "11 XOR 5 XOR 16 XOR 10 XOR 0 XOR 5",
    "10 XOR 4 XOR 15 XOR 9",
    "9 XOR 3 XOR 14 XOR 8",
    "8 XOR 2 XOR 13 XOR 7",
    "7 XOR 1 XOR 12 XOR 6",
    "6 XOR 0 XOR 11 XOR 5",
    "5 XOR 10 XOR 4",
    "4 XOR 9 XOR 3",
    "3 XOR 8 XOR 2",
    "2 XOR 7 XOR 1",
    "1 XOR 6 XOR 0",
    "0 XOR 5",
]

for line in lines:
    num_str = line.split(" XOR ")
    num_list = [int(num) for num in num_str]
    odd_occurences = [num for num, count in Counter(num_list).items() if count % 2 == 1]
    unique_nums = list(sorted(odd_occurences))
    print(unique_nums)
