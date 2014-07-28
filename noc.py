#!/usr/bin/env python
import paramiko
import telnetlib
import cmd
import sys
import time
import os




def connect():

        #--------------------------------
        #| Collect login info from user. |
        #--------------------------------
        ip = raw_input("IP Address:")
        user = raw_input("Username:")
        passw = _raw_input("Password:")

        #-------------------------------------------------------
        #| Begin SSH connection using Paramiko - Only available |
        #| in Python version 2.6+                               |
        #-------------------------------------------------------
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, username=user, password=passw, allow_agent=False, look_for_keys=False)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        chan = ssh.invoke_shell()

        #----------------------------------------------------------
        #| 'terminal length 0' disables screen breaks when output  |
        #|  from device is longer than the row count in terminal.  |
        #|  Example: show log and having to press Space to scroll  |
        #----------------------------------------------------------
        chan.send('terminal length 0'+'\n')
        print showClock(chan)
        print '\n'
        print showVer(chan)
        print '\n'
        print showLog(chan)
        print '\n'
        print intDesc(chan)
        print '\n'
        print intSumm(chan)
        print '\n'

        #----------------------------------------------------------------
        #| If device is a router - execute Routing summary show commands.|
        #----------------------------------------------------------------
        reply = raw_input("Is this device a Router? Y/N ... ").lower()
        if reply == 'y':
            print '\n'
            print showBGP(chan)
            print '\n'
            print showOSPF(chan)
            print '\n'
            print showEIGRP(chan)
            print '\n'
            print 'Finished!'
            chan.send('exit'+'\n')
        else:
            print '\n'
            print 'Finished!'
            chan.send('exit'+'\n')
        chan.close()




def telConnect():
        host = raw_input("IP Address: ")
        username = raw_input("Username: ")
        password = _raw_input("Password: ")
        tn = telnetlib.Telnet(host)
        tn.read_until("Username:")
        tn.write(username+"\n")
        tn.read_until("Password:")
        tn.write(password+"\n")
        tn.write("terminal length 0"+"\n")
        tn.write("sh clock"+"\n")
        tn.write("sh version"+"\n")
        tn.write("sh log"+"\n")
        tn.write("sh int desc"+"\n")
        tn.write("sh int summ"+"\n")
        reply = raw_input("Is this device a Router? Y/N ... ").lower()
        if reply == 'y':
                tn.write("show ip bgp summ"+"\n")
                tn.write("show ip bgp summ"+"\n")
                tn.write("show ip bgp summ"+"\n")
                tn.write("exit"+"\n")
        else:
                tn.write("exit"+"\n")
        output = tn.read_all()
        tn.close()
        return output




def _raw_input(prompt="", stream=None, input=None):
    # A raw_input() replacement that doesn't save the string in the History
    if not stream:
        stream = sys.stderr
    if not input:
        input = sys.stdin
    prompt = str(prompt)
    if prompt:
        stream.write(prompt)
        stream.flush()
    # NOTE: The Python C API calls flockfile() (and unlock) during readline.
    line = input.readline()
    if not line:
        raise EOFError
    if line[-1] == '\n':
        line = line[:-1]
    return line





def showClock(chan):
        chan.send('show clock')
        chan.send('\n')
        time.sleep(1)
        clock = chan.recv(1000)
        return clock




def showVer(chan):
        chan.send('show ver | i uptime'+'\n')
        time.sleep(1)
        version = chan.recv(1000)
        return version




def showLog(chan):
        chan.send('show log'+'\n')
        time.sleep(3)
        log = chan.recv(9999)
        return log




def intDesc(chan):
        chan.send('show int desc'+'\n')
        time.sleep(1)
        results = str(chan.recv(9999))
        return results




def intSumm(chan):
        chan.send('show int summ'+'\n')
        time.sleep(1)
        summ = str(chan.recv(9999))
        return summ




def showBGP(chan):
        chan.send('show ip bgp summ'+'\n')
        time.sleep(1)
        summ = str(chan.recv(9999))
        return summ




def showEIGRP(chan):
        chan.send('show ip eigrp neigh detail'+'\n')
        time.sleep(1)
        summ = str(chan.recv(9999))
        return summ




def showOSPF(chan):
        chan.send('show ip ospf neighbor detail'+'\n')
        time.sleep(1)
        summ = str(chan.recv(9999))
        return summ




print ("############################################")
print ("#                NOC - SPEED               #")
print ("#                Written By                #")
print ("#                  Travis                  #")
print ("############################################\n")



def main():
        userInput = raw_input("[  SSH / TELNET ... (SSH)  ]  ").lower()
        if userInput == '':
                connect()
        elif userInput.find("s") == 1:
                connect()
        else:
                print telConnect()



if __name__ == "__main__":
        main()