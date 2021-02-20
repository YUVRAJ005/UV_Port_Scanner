#!/usr/bin/python3

'''
#UV Port Scanner Designed and Developed by - Abhishek P. Iche [API]

#UV Port Scanner is a high speed port scanner providing easy to use command line interface (CLI).

#Features :-

O) High Speed Port Scanning
O) Multiple Target Scanning
O) Custom Port Range
O) Displaying Port Protocols, Service Names and Banners assigned
'''

import sys
import threading
import socket
import time
from IPy import IP
from datetime import datetime
from art import *


# Getting IP Address form domain name
def get_ip(target):
    try:
        IP(target)
        return target
    except ValueError:
        try:
            ip = socket.gethostbyname(target)
            return ip
        except socket.gaierror:
            print('[-] Hostname {} Could Not Be Resolved !'.format(target))
            sys.exit()


def port_range(portRange):
    if '-' in portRange:
        return portRange.split('-')
    elif len(portRange) == 0:
        return ['0', '1024']


# Port Scanner
def port_scanner(ip, port, output, banner, service):
    try:
        sock = socket.socket()
        sock.settimeout(5)
        sock.connect((str(ip), port))
        output[port] = 'Listening'
        try:
            service[port] = socket.getservbyport(port, 'tcp')
            service[port] = 'tcp-' + service[port]
            try:
                banner[port] = ' : ' + get_banner(sock)
            except:
                banner[port] = ''
        except:
            service[port] = socket.getservbyport(port, 'udp')
            service[port] = 'udp-' + service[port]
            try:
                banner[port] = ' : ' + get_banner(sock)
            except:
                banner[port] = ''
        finally:
            sock.close()

    except:
        output[port] = ''


# Getting Banners if there
def get_banner(sock):
    return str(sock.recv(1024).decode().strip('\n'))


# Creating and Starting Threads
def start_threads(ip, portRange):
    threads = []  # To run TCP_connect concurrently
    output = {}  # For printing purposes
    banner = {}  # To store Banners
    service = {}  # To store type of service

    # Spawning threads to scan ports
    for port in range(int(portRange[0]), int(portRange[1]) + 1):
        t = threading.Thread(target=port_scanner, args=(ip, port, output, banner, service))
        threads.append(t)

    # Starting threads
    for port in range(int(portRange[0]), int(portRange[1]) + 1):
        threads[port - int(portRange[0])].start()

    # Locking the main thread until all threads complete
    for port in range(int(portRange[0]), int(portRange[1]) + 1):
        threads[port - int(portRange[0])].join()

    # Printing listening ports from small to large
    for port in range(int(portRange[0]), int(portRange[1]) + 1):
        if output[port] == 'Listening':
            print('[+] Discovered open port {}/{}{}'.format(str(port), service[port], banner[port]))

    

# Handling particular number of threads at a time
def threads_handler(ip , portRange):
    startTime = datetime.now()

    print('[+] -> Initiating Scan at {} for Target {}'.format(startTime.strftime("%H:%M:%S"), ip))
    print('[+] -> Scanning Target {} '.format(ip))
    
    start = int(portRange[0])
    end = int(portRange[1])
 
    while  (start+500 < end):
        ports = []
        ports.append(str(start))
        ports.append(str(start + 500))
        start += 301
        start_threads(ip, ports) 
    
    ports = []
    ports.append(str(start))
    ports.append(str(end - start))
    start_threads(ip, ports)

    endTime = datetime.now()
    elapsed = endTime - startTime
    print('[+] -> Scan Completed at {}, {}s elapsed'.format(endTime.strftime("%H:%M:%S"), elapsed.seconds))
    

try:
    tprint('UV Port Scanner', font='cricket')
    time.sleep(1)
    print('UV Port Scanner')
    print('Designed and Developed by --- Abhishek P. Iche [API]')
    time.sleep(1.5)
    print()
    
    target = input('[+] Enter Target/s to scan [xxx.xxx.xxx.xxx, / www.abc.com,] : ')
    if len(target) == 0:
        print('[-] Invalid Target ! Exiting Program...')
        sys.exit()
    portRange = input('[+] Enter range of ports to scan [start-end] : ')

    if ',' in target:
        portRange = port_range(portRange)
        for address in target.split(','):
            ip = get_ip(address.strip(' '))
            threads_handler(ip, portRange)
            print()
    else:
        ip = get_ip(target)
        portRange = port_range(portRange)
        threads_handler(ip, portRange)
        print()
    time.sleep(10)
    print('\n[-]Exiting Program...')
    time.sleep(5)

except KeyboardInterrupt:
    print('\n[-]Exiting Program...')
    sys.exit()
except TypeError:
    print('\n[-] Invalid Port Range! Exiting Program...')
    sys.exit()

#Designed and Developed by - Abhishek P.Iche [API]