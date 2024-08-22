def main():
    email = input("Please enter the email: ")
    passw = input("Please enter the password: ")
    f = open("configEmail", "w")
    f.write(email + "\n")
    f.write(passw)


if __name__ == '__main__':
    main()