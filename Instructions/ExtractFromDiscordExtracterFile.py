import os
import requests
import re


def saveFile(name, content):
    with open(name, "wb+") as file:
        file.write(content)
    return


with open("channelbackup.txt", "r") as channelfile:
    channelcontent = channelfile.readlines()

Attachment = False
AttachmentCounter = 0
channelcontent2 = []
AttachmentList = []

for line in channelcontent:
    line = line.rstrip()
    if Attachment:
        AttachmentCounter += 1
        Attachment = False
        url = line
        r = requests.get(url, allow_redirects=True)
        if r.status_code != 200:
            print(r.status_code, url)
        try:
            d = r.headers['content-disposition']
            fname = re.findall("filename=(.+)", d)[0]
        except KeyError:
            fname = url.split("/")[-1]
        if os.path.exists(f"SandboxWorlds/{fname}"):
            n = 2
            while os.path.exists(f"SandboxWorlds/({n}) {fname}"):
                n += 1
            saveFile(f"SandboxWorlds/({n}) " + fname, r.content)
            line = f"SandboxWorlds/({n}) {fname}"
        else:
            saveFile("SandboxWorlds/" + fname, r.content)
            line = f"SandboxWorlds/{fname}"
        AttachmentList.append({"a": url, "r": line})
        # print(AttachmentCounter, fname, "saved")
        channelcontent2.append(line + "\n")
        continue
    if line == "{Attachments}":
        channelcontent2.append(line + "\n")
        Attachment = True
        continue
    channelcontent2.append(line + "\n")

print(AttachmentCounter)
print(AttachmentList)
with open("channelbackup2.txt", "w+") as file:
    file.write("".join(channelcontent2))
