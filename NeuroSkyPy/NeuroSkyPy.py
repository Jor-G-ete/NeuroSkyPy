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
import pandas as pd

class NeuroSkyPy(object):
    """NeuroSkyPy libraby, to get data from Neurosky Mindwave Mobile.

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

    # Private properties
    __port = None
    __baudRate = None
    __thread_id = None
    __df_saved_data = pd.DataFrame(columns=["epoch", "poorSignalHex", "poorSignal", "attentionHex", "attention",
                                            "meditationHex", "meditation", "blinkStrengthHex", "blinkStrength",
                                            "rawValueHex0", "rawValueHex1", "rawValue",
                                            "deltaHex0","deltaHex1","deltaHex2", "delta",
                                            "thetaHex0","thetaHex1","thetaHex2", "theta",
                                            "lowAlphaHex0","lowAlphaHex1","lowAlphaHex2", "lowAlpha",
                                            "highAlphaHex0", "highAlphaHex1", "highAlphaHex2", "highAlpha",
                                            "lowBetaHex0","lowBetaHex1","lowBetaHex2", "lowBeta",
                                            "highBetaHex0","highBetaHex1","highBetaHex2", "highBeta",
                                            "lowGammaHex0","lowGammaHex1","lowGammaHex2", "lowGamma",
                                            "midGammaHex0","midGammaHex1","midGammaHex2", "midGamma"])
    # Public properties
    srl = None
    threadRun = True  # controls the running of thread
    callBacksDictionary = {}  # keep a track of all callbacks
    time_value = {}  # keep time and value of the different values

    def __init__(self, port, baudRate=57600):
        self.__port, self.__baudRate = port, baudRate
        
    def __del__(self):
        self.srl.close()

    def __payload_parser(self, payload):
        """
        Function to parse the payload. For more info about this read:
            http://developer.neurosky.com/docs/lib/exe/fetch.php?media=mindset_communications_protocol.pdf
        Depending on the Data we want to extract we will have to look one or two or three bytes ahead and compute its value

        Params:
        ------
        param: payload: List -> Where the payload bytes are stored and need to be converted and analyzed

        Returns:
        --------
        return: payload: Dict > Payload bytes parsed and ready to be saved

        """
        payload_parsed = {}
        # Create a counter
        i = 0
        while i < len(payload):
            # PoorSignal
            if payload[i] == '02':
                i += 1
                payload_parsed["poorSignalHex"] = payload[i]
                payload_parsed["poorSignal"] = int(payload[i], 16)
            # Attention
            elif payload[i] == '04':
                i += 1
                payload_parsed["attentionHex"] = payload[i]
                payload_parsed["attention"] = int(payload[i], 16)
            # Meditation
            elif payload[i] == '05':
                i += 1
                payload_parsed["meditationHex"] = payload[i]
                payload_parsed["meditation"] = int(payload[i], 16)
            # Blink Strength
            elif payload[i] == '16':
                i += 1
                payload_parsed["blinkStrengthHex"] = payload[i]
                payload_parsed["blinkStrength"] = int(payload[i], 16)
            # Raw Value
            elif payload[i] == '80':
                # This is a 3 byte value. The first byte shows the length of the raw wavelength. It always be 2
                i += 1
                # That's why we move to the next byte
                i += 1
                byte0 = payload[i]
                # Then we extract the next byte
                i += 1
                byte1 = payload[i]
                # Then we perform the operation Value[0]<<8 | value[1]
                payload_parsed["rawValueHex0"] = byte0
                payload_parsed["rawValueHex1"] = byte1
                payload_parsed["rawValue"] = (int(byte0, 16) << 8) | int(byte1, 16)
                # In case we want to use arithmetic operations we will have to use the following formula
                # self.rawValue = byte0*256 + byte1
                # if self.rawValue>32768: self.rawValue=self.rawValue-65536
            # ASIC_EEG_POWER
            elif payload[i] == '83':
                # We discard the length of the payload
                i += 1
                # Each wavelength has 3 bytes. That's why we will apply << 16  to the first byte and << 8 to the second
                # with that we will create a decimal number for those 3 bytes
                # The arithmetic operation is:  self.delta=val0*65536+val1*256+int(payload[i],16)
                # Run over the waves and set its value
                for wave in ["delta", "theta", "lowAlpha", "highAlpha", "lowBeta", "highBeta", "lowGamma", "midGamma"]:
                    # Delta:
                    i += 1
                    byte0 = payload[i]
                    i += 1
                    byte1 = payload[i]
                    i += 1
                    byte2 = payload[i]
                    payload_parsed[wave+"Hex0"] = byte0
                    payload_parsed[wave+"Hex1"] = byte1
                    payload_parsed[wave+"Hex2"] = byte2
                    payload_parsed[wave] = (int(byte0, 16) << 16) |(int(byte1, 16) << 8) | int(byte2, 16)

            # Read the next byte
            i += 1
        # Return the payload parsed
        return payload_parsed

    def __packetParser(self, srl):
        """
        Function used by the thread. This function reads packets from
        """
        "packetParser runs continously in a separate thread to parse packets from mindwave and update the corresponding variables"
        # if not srl.isOpen(): srl.open()
        while self.threadRun and srl.isOpen():
            # read the first two bytes of SYNC
            sync1 = srl.read(1).hex()
            sync2 = srl.read(1).hex()
            # loop until sync1 and sync2 are both 0xAA
            while sync1 != 'aa' or sync2 != 'aa':
                sync1 = sync2
                sync2 = srl.read(1).hex()
            else:
                # SYNC Done
                # Declare the variables
                payload = []
                checksum = 0
                # obtain the length of the payload, convert it from hex ( mod-16 ) to int ( mod-10 )
                payload_length = int(srl.read(1).hex(), 16)
                # In case payload is bigger than 170 bytes discard the packet, in case it's 170 ( means SYNC) so we read it again
                if payload_length == 170: payload_length = int(srl.read(1).hex(),16)
                elif payload_length > 170: continue
                # Run over the payload
                for i in range(payload_length):
                    temp_payload = srl.read(1).hex()
                    # Save the payload to posterior analysis
                    payload.append(temp_payload)
                    # Add the values to compute the checksum later
                    checksum += int(temp_payload, 16)
                # compute the checksum, inverting the last 8 bits ( or the last byte )
                checksum =~ checksum & 0x000000ff
                # Check if the checksum match with the computed checksum
                if checksum != int(): continue
                # parse the payload
                payload_parsed = self.__payload_parser(payload)
            # Save the data inside a DataFrame of pandas
            # Extract and create a timestamp with Hours / Minutes / Seconds / MiliSeconds
            payload_parsed["epoch"] = datetime.now().strftime("%H%M%S%f")
            # Save it
            self.__df_saved_data.append(payload_parsed, ignore_index=True)
        # when the thread is closed then we exit and close the thread
        self.srl.close()
        # raise exception to close the thread
        thread.exit()

    def start(self):
        """
        Starts __packetParser in a separate thread and fix the data of the Thread in the Object private properties

        Params:
        -------
        param: Self -> Main NeuroSkyPy Objetct

        Return: Nothing
        """
        # Declare that the thread is running
        self.threadRun = True
        # Open and collect data from the Serial Port
        self.srl = serial.Serial(self.__port, self.__baudRate)
        # uncomment when the know how to kill a thread

        # Save the thread id
        self.__thread_id = thread.start_new_thread(self.__packetParser, (self.srl,))

    def stop(self):
        """
        Stops the __packetParser thread

        Params:
        -------
        param: Self -> Main NeuroSkyPy ObjetctM

        Return: Nothing
        """
        self.threadRun = False
