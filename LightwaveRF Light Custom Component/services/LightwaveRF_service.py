#!/usr/bin/env python

#LightwaveRF Service for Raspberry PI
#SCCMOG - Richie Schuster - 0/05/2018
#www.sccmog.com
#This script can also be run stand alone for trouble shooting in a terminal.

import pika
import sys
import time
import subprocess
import socket


credentials = pika.PlainCredentials('[yourusername]','[yourpassword]')
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',
                                        5672,
                                        '/',
                                        credentials))
channel = connection.channel()

def callback(ch, method, properties, body):
        i = body.split('|', 1)
        lrflink = i[0]
        cmd = i[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(cmd.encode('UTF-8'), (lrflink, 9760))
        sock.close
        time.sleep(0.8)
        info = ' [x] Sent: %sto LightwaveRF Link: %s ' % (cmd, lrflink)
        print(info)

channel.basic_consume(callback,
                        queue='LightwaveRF',
                        no_ack=True)
              

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()

