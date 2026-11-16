
def unique(numbers):
    result = []

    for number in numbers:
        if number not in result:
            result.append(number)

    return result


numbers = [1, 2, 2, 3, 4, 4, 5, 6, 6, 7,]

print(unique(numbers))
print(type("numbers"))