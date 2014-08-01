#!/usr/bin/env python
import paramiko
import telnetlib
import subprocess
import re
import sys
import time
import optparse
import os
import cmd


#Eventual Command-line option parser to be implemented with multiple modules--------
#parser = optparse.OptionParser()
#parser.add_option('-p', '--ping', dest = 'ping_option', action='store_true', default=True)
#parser.add_option('-d', '--diagnostic', dest = 'diag_option', action = 'store_true', default = False)


def massPing():

        #--------------------------------
        #| Asks user for a block of text |
        #| Filters out valid IP's using  |
        #| a regex, appends them to a    |
        #| Tuple, and outputs UP or DOWN |
        #| result for each valid address |
        #--------------------------------

        pattern = r"((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)([ (\[]?(\.|dot)[ )\]]?(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3})"
        print('Paste block of Text Containing IP addresses to be pinged: (Press Ctrl+D when Finished) \n\n')
        block = sys.stdin.read()
        ips = [each[0] for each in re.findall(pattern, block)]
        upCount = 0
        downCount = 0
        print ("\n\n############################################")
        print ("#                                          #")
        print ("#        Performing Mass-Ping Test         #")
        print ("#                                          #")
        print ("############################################\n")
        for ip in ips:
            FNULL = open(os.devnull, 'w')
            output = subprocess.call(['ping', '-c 2', ip], stdout=FNULL, stderr=subprocess.STDOUT)
            if output == 1:
                print('Failure: ' + ip + ' is Unreachable.')
                downCount += 1
            else:
                print('Success: ' + ip + ' is Up and Reachable.')
                upCount += 1
        print('\nFinished pinging all IP Addresses')
        print('Results: ' + str(upCount) + ' Hosts Up / ' + str(downCount) + ' Hosts Down.\n')
        exit()


def connect():

        #--------------------------------
        #| Collect login info from user. |
        #--------------------------------
        ip = raw_input("IP Address:")
        user = raw_input("Username:")
        passw = _raw_input("Password:")

        print ("\n\n############################################")
        print ("#                                          #")
        print ("#        Pulling Device Statistics         #")
        print ("#                                          #")
        print ("############################################\n")

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
        print ('\n-------------------------------------\n')
        print showClock(chan)
        print ('\n-------------------------------------\n')
        print showVer(chan)
        print ('\n-------------------------------------\n')
        print showLog(chan)
        print ('\n-------------------------------------\n')
        print intDesc(chan)
        print ('\n-------------------------------------\n')
        print intSumm(chan)
        print ('\n-------------------------------------\n')

        #----------------------------------------------------------------
        #| If device is a router - execute Routing summary show commands.|
        #----------------------------------------------------------------
        reply = raw_input("Is this device a Router? Y/N ... ").lower()
        if reply == 'y':
            print ('\n-------------------------------------\n')
            print showBGP(chan)
            print ('\n-------------------------------------\n')
            print showOSPF(chan)
            print ('\n-------------------------------------\n')
            print showEIGRP(chan)
            print ('\n-------------------------------------\n')
            print 'Finished!'
            chan.send('exit'+'\n')
        else:
            print ('\n-------------------------------------\n')
            print 'Finished!'
            chan.send('exit'+'\n')
        chan.close()




def telConnect():
        host = raw_input("IP Address: ")
        username = raw_input("Username: ")
        password = _raw_input("Password: ")

        print ("\n\n############################################")
        print ("#                                          #")
        print ("#        Pulling Device Statistics         #")
        print ("#                                          #")
        print ("############################################\n")

        tn = telnetlib.Telnet(host)
        tn.read_until("Username:")
        tn.write(username+"\n")
        tn.read_until("Password:")
        tn.write(password+"\n")

        tn.write("terminal length 0"+"\n")
        print ('\n-------------------------------------\n')
        tn.write("sh clock"+"\n")
        print ('\n-------------------------------------\n')
        tn.write("sh version | i uptime"+"\n")
        print ('\n-------------------------------------\n')
        tn.write("sh log"+"\n")
        print ('\n-------------------------------------\n')
        tn.write("sh int desc"+"\n")
        print ('\n-------------------------------------\n')
        tn.write("sh int summ"+"\n")
        print ('\n-------------------------------------\n')
        reply = raw_input("Is this device a Router? Y/N ... ").lower()
        if reply == 'y':
                print ('\n-------------------------------------\n')
                tn.write("show ip bgp summ"+"\n")
                print ('\n-------------------------------------\n')
                tn.write("show ip bgp summ"+"\n")
                print ('\n-------------------------------------\n')
                tn.write("show ip bgp summ"+"\n")
                print ('\n-------------------------------------\n')
                print ('Finished!')
                tn.write("exit"+"\n")
        else:
                print ('Finished!')
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
        summ = chan.recv(1000)
        return summ




def showVer(chan):
        chan.send('show ver | i uptime'+'\n')
        time.sleep(1)
        summ = chan.recv(1000)
        return summ




def showLog(chan):
        chan.send('show log'+'\n')
        time.sleep(3)
        summ = chan.recv(9999)
        return summ




def intDesc(chan):
        chan.send('show int desc'+'\n')
        time.sleep(1)
        summ = str(chan.recv(9999))
        return summ




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



print ("\n")
print ("############################################")
print ("#           Welcome to NOC Magic           #")
print ("#                ++++++++++                #")
print ("#             Written by Travis            #")
print ("#            root{at}info5ec.com           #")
print ("############################################\n")



def main():
        answer = raw_input("Press 1 for MassPing -OR- Press Enter for Diagnostics ... ")
        if answer == 1:
            massPing()
        else:
            userInput = raw_input("[  SSH / TELNET ... (SSH)  ]  ").lower()
            if userInput == '':
                connect()
            elif userInput.find("s") == 's':
                connect()
            else:
                print telConnect()



if __name__ == "__main__":
        main()