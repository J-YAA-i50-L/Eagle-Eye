import time
import serial
import random

ser = serial.Serial('COM7', 9600)
time.sleep(2)
ser.reset_input_buffer()
Time = 1000
while True:
    try:
        ser_bytes = ser.readline()  
        decoded_bytes = float(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
        R, G, B = 0, 0 ,0
        print(decoded_bytes)
        if decoded_bytes == 1:
            R, G, B = random.randrange(0, 2), random.randrange(0, 2), random.randrange(0, 2)
            #Time = random(1000, 2001)
            D1 = str(R) + "," + str(G) + "," + str(B) + "," + str(Time)
            print(D1)
            b1 = bytes(D1, encoding='utf-8')
            ser.write(b1)
        #print(R, G, B, Time)
               
    except:
        print("Keyboard Interrupt")
        break
