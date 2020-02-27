import vehicles
import Strings
import re
import base64
import binascii


if __name__ == '__main__':
    # vehicles.ExpVehicles()
    # Strings.ExpString()
    cc = base64.b64encode("\x15\x55\xD3\x0F\x38\xB0\xDB\xCA\xEC\x83\xC0\xF9".encode('utf-8'))
    print(cc)
