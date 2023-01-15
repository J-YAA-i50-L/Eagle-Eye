import serial
import time


def outpyt_py(mode, speedL, speedR):  # Шифрование данных для отправки
    """Шифрование данных для отправки на Arduino"""
    out_string = f'{mode}, {speedL}, {speedR}'
    print(out_string)
    return bytes(out_string, encoding='utf-8')


def input_arduino(ser_bytes):
    """Расшифровка данных полученных с Arduino"""
    decoded_bytes = str(ser_bytes[0:len(ser_bytes) - 2].decode("utf-8"))
    if decoded_bytes == "?":
        return True


# ser = serial.Serial('COM7', 9600)  # ToDo: Порт проверить и сменить!!!!!!!!!!!!!!!
# time.sleep(2)
# ser.reset_input_buffer()
#
# while True:
#     ser.write(outpy(100, 255, 255))
#     time.sleep(1.1)
