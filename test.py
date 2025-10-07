name = input("Enter the name\n")
print(f"{name}, Enter the password")
password = input()

def check(password):
    for i in password:
        if not (ord(i) >= 65 and ord(i) <= 90 or ord(i) >= 97 and ord(i) <= 122):
            return (f"Registration is unsuccessful. {password} is an invalid password")
            
    return (f"{password} is a valid password.")
        
print(check(password))
        