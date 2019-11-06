import time

f = open('log.txt',mode='a+')
user = 'Hawkin'
print('---------------------------',file=f)
localtime = time.asctime(time.localtime(time.time()) )
print('Time:', localtime, file=f)
print('User:', user, file=f)
print('', file=f)
print('Logfile: xxx', file=f)
print('Content: xxx', file=f)
print('---------------------------', file=f)
print('', file=f)