"""
zip加密文件破解
"""

import zipfile

def extractFile(zfile, passwd):
    try:
        zfile.extractall(pwd=passwd)
        return passwd
    except :
        return


# 单线程执行
def main0():
    zfile = zipfile.ZipFile('test.zip')
    passFile = open('dictionary.txt')
    for line in passFile.readlines():
        passwd = line.strip('\n')
        guess = extractFile(zfile, passwd)
        if guess:
            print('[+] Password = %s \n' % guess)
            exit(0)


from threading import Thread
# 多线程执行
def main1():
    zfile = zipfile.ZipFile('test.zip')
    passFile = open('dictionary.txt')
    for line in passFile.readlines():
        passwd = line.strip('\n')
        t = Thread(target=extractFile, args=(zfile, passwd))
        t.start()


import optparse
def main2():
    """
    用户指定输入要破解的zip文件和字典文件
    :return:
    """
    parser = optparse.OptionParser("usage%prog -f <zipfile> -d <dictionory>")
    parser.add_option('-f', dest='zname', type='string', help='specify zip file')
    parser.add_option('-d', dest='dname', type='string', help='specify dictionary file')
    (options, args) = parser.parse_args()
    if (options.zname == None) | (options.dname == None):
        print(parser.usage)
        exit(0)
    else:
        zname = options.zname
        dname = options.dname
    zfile = zipfile.ZipFile(zname)
    passFile = open(dname)
    for line in passFile.readlines():
        passwd = line.strip('\n')
        t = Thread(target=extractFile, args=(zfile, passwd))
        t.start()


if __name__ == "__main__":
    main0()