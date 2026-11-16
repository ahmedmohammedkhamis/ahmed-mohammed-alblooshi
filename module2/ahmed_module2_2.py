
def encrypt(text):
    result = ""

    for letter in text:
        result += chr(ord(letter) + 2)

    return result


message = input("enter your message: ")
encrypted = encrypt(message)

print("Encrypted message:", encrypted)
