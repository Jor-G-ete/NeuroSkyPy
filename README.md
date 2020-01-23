# NeuroSkyPy

[![](https://img.shields.io/pypi/v/neuroskypy.svg)](https://pypi.org/project/NeuroSkyPy/)
[![](https://img.shields.io/pypi/pyversions/neuroskypy.svg)](https://pypi.org/project/NeuroSkyPy/)
[![](https://img.shields.io/pypi/l/neuroskypy.svg)](https://github.com/Jor-G-ete/NeuroSkyPy/blob/master/LICENSE)
[![](https://img.shields.io/pypi/dd/neuroskypy.svg)]()
[![](https://img.shields.io/github/last-commit/Jor-G-ete/NeuroSkyPy)]()
[![](https://img.shields.io/github/v/release/Jor-G-ete/NeuroSkyPy)]()
[![](https://img.shields.io/github/v/tag/Jor-G-ete/NeuroSkyPy)]()

NeuroSkyPy library written in python3.7 to connect, interact, get, save and plot data  from **NeuroSky's MindWave** EEG headset, the first one ( black ).

This library is based on the mindwave mindset communication protocol published by [Neurosky](http:://neurosky.com) and is tested with Neurosky Mindwave EEG headset. Where It's readen the data in hex, after that it's decoded.

## Installation

### Source file
1. Download the source file from github
2. Unzip and navigate to the folder containing `setup.py` and other files
3. Run the following command: `python setup.py install`

### Pip
```python3
    pip3 install NeuroSkyPy
```

## Usage

A test-script which is used as experiment it's left in order to check and learn how to use the class. 
The basic steps to use the class are:
1. Importing the module: `from NeuroPy import NeuroPy`
2. Initializing: `neuropy = NeuroPy()`
3. After initializing, either the callbacks can be set or just extract data from the object as it's done in test-script. 
4. Then call `neuropy.start()` method, it will start fetching data from mindwave.
5. To stop call `neuropy.stop()`. 


### Obtaining Data from Device 

* **Obtaining value:** `attention = neuropy.attention` \#to get value of attention_
    >**Other Variable** attention, meditation, rawValue, delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, midGamma, poorSignal and blinkStrength

* **Setting callback:** A call back can be associated with all the above variables so that a function is called when the variable is updated. Syntax: 

    ```
    setCallBack("[variable]",callback_function)
    ``` 
    **for eg.** to set a callback for attention data the syntax will be 
    ```
    setCallBack("attention",callback_function)
    ```
    >**Other Variables:** attention, meditation, rawValue, delta, theta, lowAlpha, highAlpha, lowBeta, highBeta, lowGamma, midGamma, poorSignal and blinkStrength

## Sample Program 1 (Access via callback)

```python
from NeuroPy import NeuroPy
from time import sleep

neuropy = NeuroPy() 

def attention_callback(attention_value):
    """this function will be called everytime NeuroPy has a new value for attention"""
    print ("Value of attention is: ", attention_value)
    return None

neuropy.setCallBack("attention", attention_callback)
neuropy.start()

try:
    while True:
        sleep(0.2)
finally:
    neuropy.stop()
```


## Sample Program 2 (Access via object)

```python
from NeuroPy import NeuroPy
from time import sleep

neuropy = NeuroPy() 
neuropy.start()

while True:
    if neuropy.meditation > 70: # Access data through object
        neuropy.stop() 
    sleep(0.2) # Don't eat the CPU cycles
```

## Python Compatibility

* [Python](http://www.python.com) - v3.7

### Note
This library comes from the libraries [NeuroPy](https://github.com/lihas/NeuroPy) and [mindwave-python](https://github.com/BarkleyUS/mindwave-python). 
The library is tested and comes with extracted data. 

### More Information

