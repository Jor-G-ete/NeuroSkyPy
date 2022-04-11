from NeuroSkyPy.NeuroSkyPy import NeuroSkyPy
# from NeuroSkyPy.IO import *
from NeuroSkyPy.DiscoverComPort import set_equipment_windows
from time import sleep
from time import time



if __name__ == "__main__":
    # find the com port
    com_port = set_equipment_windows()
    # create the object
    neuropy = NeuroSkyPy(port=com_port, sample_time=1)
    # start the thread
    neuropy.start()
    sleep(60)
    df, packet_data = neuropy.stop()
    print()
