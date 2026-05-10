from hal import hal_rfid_reader as rdif_reader
import time

def read_rfid()-> bool:
    reader = rdif_reader.init()

    for _ in range (10):
        rfid = reader.read_id_no_block()    

        if rfid != None:
            return True
        
        time.sleep(1)

        
    
    return False