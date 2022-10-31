import serial
import pynmea2

class gps:
    def __init__(self):
        self.dataGPGGA()
        
    def dataGPGGA(self):
        port = "/dev/ttyUSB1"
        ser = serial.Serial(port, baudrate = 115200, timeout = 0.5,rtscts=True, dsrdtr=True)
        
        while True:
            pynmea2.NMEAStreamReader()
            newdata=ser.readline().decode("utf-8","ignore")
            if newdata[0:6] == "$GPGGA":
                newmsg=pynmea2.parse(newdata)
                self.lat=str(round(newmsg.latitude,6))
                self.lng=str(round(newmsg.longitude,6))
                break



