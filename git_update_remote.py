#!/usr/bin/python
# -*- coding: utf-8 -*-

import pexpect
import paramiko

try:
    f = open('.update_remote')
except:
    print('No .update_remote info. user@host password directory')

user, host, password, directory = f.read().split(' ')

#git push origin master
child = pexpect.spawn('git push origin master')

print('Entering password...')
child.expect(".*: ")
child.sendline(password)

i = child.expect(["Permission denied.*", '.*'])
if(i == 0):
  print 'Wrong password, please check your .update_remote file and try again'
else:
  print 'Password ok, sending data to remote...'

child.expect(".*")
child.kill(0)

#ssh
ssh = paramiko.SSHClient()
print('Connecting...')
ssh.set_missing_host_key_policy(paramiko.WarningPolicy())
print host, user, password
ssh.connect(host, username=user, password=password)

print('SSH Command: cd '+directory+' && git pull origin master')
ch = ssh.get_transport().open_session()

print ch.exec_command('cd '+directory+' && git pull origin master')
print ch.recv_exit_status()
ssh.close()
