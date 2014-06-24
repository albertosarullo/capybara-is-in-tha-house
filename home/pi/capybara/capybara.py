#!/usr/bin/env python
import RPi.GPIO as GPIO
import time 
import subprocess
import PiFm

gpioPin = 5 

GPIO.cleanup()
GPIO.setmode(GPIO.BOARD) 
GPIO.setup(gpioPin, GPIO.OUT) 

def checkNetwork(network):
    GPIO.output(gpioPin, False); 
    pifmProc = "" 
    while True:
        try:
            output = "" 
            output = subprocess.check_output('iwlist wlan0 scan | grep ingulfnet',shell=True,stderr=subprocess.STDOUT);
        except:
            print("Execution failed") 
        print "output = " + output

        if output:
            print "RETE TROVATA"
            GPIO.output(gpioPin, False)
            time.sleep(0.05) 
            GPIO.output(gpioPin, True)
            try:
                if pifmProc:
                    print "fm already started"
                    if pifmProc.poll() is None: 
                        print "fm in execution.." 
                    else:
                        print "exiting"
                        pifmProc = "" 
                else:
                    print "pi fm start..."
                    pifmProc = subprocess.Popen(["/home/pi/capybara/pifm","/home/pi/capybara/fear.wav","89,00"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print "pi fm post start" 
            except:
                print "pifm except"  
                pifmProc = "" 
        else: 
            print "rete non trovata"
            GPIO.output(gpioPin, True)
            time.sleep(0.05)
            GPIO.output(gpioPin, False)
            if pifmProc:
                print "pifm kill"
                pifmProc.kill()
                pifmProc = "" 

        time.sleep(5) 
        
    print "Done" 
    GPIO.cleanup()

#network = raw_input("Enter the name of network to spy")




checkNetwork("network")

