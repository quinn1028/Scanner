import nmap
import time
import json

try:
    from gpiozero import LED
except:
    print('Unable to import LED')

timeout = 180 #3 minutes

with open('people.json') as f:
     macs_home = json.load(f)

nm = nmap.PortScanner()

# Initialize people's GPIO pins
def init():
    for mac in macs_home.keys():
        macs_home[mac]['led'] = LED(macs_home[mac]['GPIO_pin'])

# Run init
try:
    init()
except:
    print('Unable to initialize GPIO pins; skipping.')

def scan():
    while True:
        hosts = nm.scan(hosts='192.168.86.0/24', arguments='-n -sP -PE')['scan']
    
        for ip in hosts.keys():
            if 'mac' in hosts[ip]['addresses']:
                found_mac = hosts[ip]['addresses']['mac']
                if found_mac in macs_home:
                    macs_home[found_mac]['last_seen'] = time.time()
                    pretty_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(macs_home[found_mac]['last_seen']))
                    print('found %s at %s' % (macs_home[found_mac]['name'], pretty_time))
                    macs_home[found_mac]['connected'] = True

                    try:
                        macs_home[found_mac]['led'].on()
                    except:
                        print('Unable to change LED')

        print('EOF')
        # here
        for ip in macs_home.keys():
            if macs_home[ip]['last_seen'] + timeout < time.time():
                macs_home[ip]['connected'] = False

                try:
                    macs_home[ip]['led'].off()
                except:
                    print('Unable to change LED')
    