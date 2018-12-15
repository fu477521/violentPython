"""
UNIX口令破解机
使用UNIX计算口令hash的 crypt()算法。
"""

import crypt


def testPass(cryptPass):
	salt = cryptPass[0:2]

	dictFile = open("dictionary.txt","r")
	for word in dictFile.readlines():
		word = word.strip('\n')
        # 将口令和salt作为参数传递进去
		cryptWord = crypt.crypt(word,salt)
        # 将计算出来 的结果与我们传入的参数比较，找出符合结果的口令值，
        # 如果没有找到，打印找不到的信息提示。
		if (cryptWord == cryptPass):
			print("[+] Found PassWord: "+word+"\n")
			return
		print("[-] Password Not Found.\n")
		return

def main():
    """
    逐行搜索破解口令
    :return:
    """
	passfFile = open('passwords.txt')
	for line in passfFile.readlines():
		if ":" in line:
			user = line.split(':')[0]
			cryptPass = line.split(':')[1].strip(' ')
			print("[*] Cracking Password For : "+user)
			result = testPass(cryptPass)



if __name__ == '__main__':
	main()
