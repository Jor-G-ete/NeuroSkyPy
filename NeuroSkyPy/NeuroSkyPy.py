##Copyright (c) 2020, Jorge Lopez Marcos
##
##All rights reserved.
##
##Redistribution and use in source and binary forms, with or without modification,
##are permitted provided that the following conditions are met:
##
##    * Redistributions of source code must retain the above copyright notice,
##      this list of conditions and the following disclaimer.
##    * Redistributions in binary form must reproduce the above copyright notice,
##      this list of conditions and the following disclaimer in the documentation
##      and/or other materials provided with the distribution.
##    * Neither the name of NeuroPy nor the names of its contributors
##      may be used to endorse or promote products derived from this software
##      without specific prior written permission.
##
##THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
##"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
##LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
##A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
##CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
##EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
##PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
##PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
##LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
##NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
##SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import serial
import _thread as thread  # Modified thread for _thread due to it's the new library in python 3.7
from datetime import datetime

class NeuroSkyPy(object):
    """NeuroSkyPy libraby, to get data from neurosky mindwave.
    Initialising: object1=NeuroSkyPy("COM6",57600) #windows
    After initialising , if required the callbacks must be set
    then using the start method the library will start fetching data from mindwave
    i.e. object1.start()
    similarly stop method can be called to stop fetching the data
    i.e. object1.stop()

    The data from the device can be obtained using either of the following methods or both of them together:
    
    Obtaining value: variable1=object1.attention #to get value of attention
    #other variables: attention,meditation,rawValue,delta,theta,lowAlpha,highAlpha,lowBeta,highBeta,lowGamma,midGamma, poorSignal and blinkStrength
    
    Setting callback:a call back can be associated with all the above variables so that a function is called when the variable is updated. Syntax: setCallBack("variable",callback_function)
    for eg.to set a callback for attention data the syntax will be setCallBack("attention",callback_function)"""
    __attention = 0
    __meditation = 0
    __rawValue = 0
    __delta = 0
    __theta = 0
    __lowAlpha = 0
    __highAlpha = 0
    __lowBeta = 0
    __highBeta = 0
    __lowGamma = 0
    __midGamma = 0
    __poorSignal = 0
    __blinkStrength = 0
    __port = None
    __baudRate = None
    __thread_id = None
    srl = None
    threadRun = True  # controls the running of thread
    callBacksDictionary = {}  # keep a track of all callbacks
    time_value = {}  # keep time and value of the different values

    def __init__(self, port, baudRate=57600):
        self.__port, self.__baudRate = port, baudRate
        
    def __del__(self):
        self.srl.close()
    
    def start(self):
        """starts packetparser in a separate thread"""
        self.threadRun = True
        self.srl = serial.Serial(self.__port, self.__baudRate)
        # uncomment when the know how to kill a thread
        self.__thread = thread.start_new_thread(self.__packetParser,(self.srl,))
        # thread.start_new_thread(self.__packetParser, (self.srl,))

    def __packetParser(self, srl):
        "packetParser runs continously in a separate thread to parse packets from mindwave and update the corresponding variables"
        # if not srl.isOpen(): srl.open()
        while self.threadRun:
            p1 = srl.read(1).hex()  # read first 2 packets
            p2 = srl.read(1).hex()
            while p1 != 'aa' or p2 != 'aa':
                p1 = p2
                p2 = srl.read(1).hex()
            else:
                #a valid packet is available
                payload=[]
                checksum=0;
                payloadLength=int(srl.read(1).hex(),16)
                for i in range(payloadLength):
                    tempPacket=srl.read(1).hex()
                    payload.append(tempPacket)
                    checksum+=int(tempPacket,16)
                checksum=~checksum&0x000000ff
                if checksum==int(srl.read(1).hex(),16):
                   i=0
                   while i<payloadLength:
                       code=payload[i]
                       if(code=='02'):#poorSignal
                           i=i+1; self.poorSignal=int(payload[i],16)
                       elif(code=='04'):#attention
                           i=i+1; self.attention=int(payload[i],16)
                       elif(code=='05'):#meditation
                           i=i+1; self.meditation=int(payload[i],16)
                       elif(code=='16'):#blink strength
                           i=i+1; self.blinkStrength=int(payload[i],16)
                       elif(code=='80'):#raw value
                           i=i+1 #for length/it is not used since length =1 byte long and always=2
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; self.rawValue=val0*256+int(payload[i],16)
                           if self.rawValue>32768 :
                               self.rawValue=self.rawValue-65536
                       elif(code=='83'):#ASIC_EEG_POWER
                           i=i+1;#for length/it is not used since length =1 byte long and always=2
                           #delta:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.delta=val0*65536+val1*256+int(payload[i],16)
                           #theta:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.theta=val0*65536+val1*256+int(payload[i],16)
                           #lowAlpha:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.lowAlpha=val0*65536+val1*256+int(payload[i],16)
                           #highAlpha:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.highAlpha=val0*65536+val1*256+int(payload[i],16)
                           #lowBeta:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.lowBeta=val0*65536+val1*256+int(payload[i],16)
                           #highBeta:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.highBeta=val0*65536+val1*256+int(payload[i],16)
                           #lowGamma:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.lowGamma=val0*65536+val1*256+int(payload[i],16)
                           #midGamma:
                           i=i+1; val0=int(payload[i],16)
                           i=i+1; val1=int(payload[i],16)
                           i=i+1; self.midGamma=val0*65536+val1*256+int(payload[i],16)
                       else:
                           pass
                       i=i+1

        # when the thread is closed then we exit and close the thread
        self.srl.close()
        # raise exception to close the thread
        thread.exit()

    def stop(self):
        "stops packetparser's thread and releases com port i.e disconnects mindwave"
        self.threadRun = False

    def setCallBack(self, variable_name, callback_function):
        """Setting callback:a call back can be associated with all the above variables so that a function is called when the variable is updated. Syntax: setCallBack("variable",callback_function)
           for eg. to set a callback for attention data the syntax will be setCallBack("attention",callback_function)"""
        self.callBacksDictionary[variable_name]=callback_function
        self.time_value[variable_name]={}

    def getTimeTaken(self):
        return self.time_value

    #setting getters and setters for all variables
    
    #attention
    @property
    def attention(self):
        "Get value for attention"
        return self.__attention
    @attention.setter
    def attention(self,value):
        # extract actual time
        at_time_taken = datetime.now().strftime("%H%m%S")
        self.__attention=value
        if "attetion" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["attention"](self.__attention)
            self.time_value["attention"][str(at_time_taken)] = self.__attention

    #meditation
    @property
    def meditation(self):
        "Get value for meditation"
        return self.__meditation
    @meditation.setter
    def meditation(self,value):
        md_time_taken = datetime.now().strftime("%H%m%S")
        self.__meditation=value
        if "meditation" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["meditation"](self.__meditation)
            self.time_value["meditation"][str(md_time_taken)] = self.__meditation

    #rawValue
    @property
    def rawValue(self):
        "Get value for rawValue"
        return self.__rawValue
    @rawValue.setter
    def rawValue(self,value):
        rw_time_taken = datetime.now().strftime("%H%m%S")
        self.__rawValue=value
        if "rawValue" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["rawValue"](self.__rawValue)
            self.time_value["rawValue"][str(rw_time_taken)] = self.__rawValue

    #delta
    @property
    def delta(self):
        "Get value for delta"
        return self.__delta
    @delta.setter
    def delta(self,value):
        dl_time_taken = datetime.now().strftime("%H%m%S")
        self.__delta=value
        if "delta" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["delta"](self.__delta)
            self.time_value["delta"][str(dl_time_taken)] = self.__delta

    #theta
    @property
    def theta(self):
        "Get value for theta"
        return self.__theta
    @theta.setter
    def theta(self,value):
        tt_time_taken = datetime.now().strftime("%H%m%S")
        self.__theta=value
        if "theta" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["theta"](self.__theta)
            self.time_value["theta"][str(tt_time_taken)] = self.__theta

    #lowAlpha
    @property
    def lowAlpha(self):
        "Get value for lowAlpha"
        return self.__lowAlpha
    @lowAlpha.setter
    def lowAlpha(self,value):
        la_time_taken = datetime.now().strftime("%H%m%S")
        self.__lowAlpha=value
        if "lowAlpha" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["lowAlpha"](self.__lowAlpha)
            self.time_value["lowAlpha"][str(la_time_taken)] = self.__lowAlpha

    #highAlpha
    @property
    def highAlpha(self):
        "Get value for highAlpha"
        return self.__highAlpha
    @highAlpha.setter
    def highAlpha(self,value):
        ha_time_taken = datetime.now().strftime("%H%m%S")
        self.__highAlpha=value
        if "highAlpha" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["highAlpha"](self.__highAlpha)
            self.time_value["highAlpha"][str(ha_time_taken)] = self.__highAlpha


    #lowBeta
    @property
    def lowBeta(self):
        "Get value for lowBeta"
        return self.__lowBeta
    @lowBeta.setter
    def lowBeta(self,value):
        lb_time_taken = datetime.now().strftime("%H%m%S")
        self.__lowBeta=value
        if "lowBeta" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["lowBeta"](self.__lowBeta)
            self.time_value["lowBeta"][str(lb_time_taken)] = self.__lowBeta

    #highBeta
    @property
    def highBeta(self):
        "Get value for highBeta"
        return self.__highBeta
    @highBeta.setter
    def highBeta(self,value):
        hb_time_taken = datetime.now().strftime("%H%m%S")
        self.__highBeta=value
        if "highBeta" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["highBeta"](self.__highBeta)
            self.time_value["highBeta"][str(hb_time_taken)] = self.__highBeta

    #lowGamma
    @property
    def lowGamma(self):
        "Get value for lowGamma"
        return self.__lowGamma
    @lowGamma.setter
    def lowGamma(self,value):
        lg_time_taken = datetime.now().strftime("%H%m%S")
        self.__lowGamma=value
        if "lowGamma" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["lowGamma"](self.__lowGamma)
            self.time_value["lowGamma"][str(lg_time_taken)] = self.__lowGamma

    #midGamma
    @property
    def midGamma(self):
        "Get value for midGamma"
        return self.__midGamma
    @midGamma.setter
    def midGamma(self,value):
        mg_time_taken = datetime.now().strftime("%H%m%S")
        self.__midGamma=value
        if "midGamma" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["midGamma"](self.__midGamma)
            self.time_value["midGamma"][str(mg_time_taken)] = self.__midGamma

    #poorSignal
    @property
    def poorSignal(self):
        "Get value for poorSignal"
        return self.__poorSignal
    @poorSignal.setter
    def poorSignal(self,value):
        ps_time_taken = datetime.now().strftime("%H%m%S")
        self.__poorSignal=value
        if "poorSignal" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["poorSignal"](self.__poorSignal)
            self.time_value["poorSignal"][str(ps_time_taken)] = self.__poorSignal

    #blinkStrength
    @property
    def blinkStrength(self):
        "Get value for blinkStrength"
        return self.__blinkStrength
    @blinkStrength.setter
    def blinkStrength(self,value):
        bs_time_taken = datetime.now().strftime("%H%m%S")
        self.__blinkStrength=value
        if "blinkStrength" in self.callBacksDictionary.keys(): #if callback has been set, execute the function
            self.callBacksDictionary["blinkStrength"](self.__blinkStrength)
            self.time_value["blinkStrength"][str(bs_time_taken)] = self.__blinkStrength
