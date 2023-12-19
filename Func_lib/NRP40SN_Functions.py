import pyvisa,time


def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue

def NRP40SN_connect():
    global NRP40SN
    rm = pyvisa.ResourceManager()
    try:
        NRP40SN = rm.open_resource('USB0::0x0AAD::0x0160::101025::INSTR')
        Wait_Command(NRP40SN, 0.2)
    except Exception as e:
        print('NRP40SN connect error!  ' + str(e) + '\n')
        exit(-1)



#NRP40SN初始化
def NRP40SN_RST():
    try:
        NRP40SN.write('*RST')
        Wait_Command(NRP40SN, 0.1)
    except Exception as e:
        print('NRP40SN RST error!  ' + str(e) + '\n')
        exit(-1)


#读取单频点功率，单位dBm
def NRP40SN_ReadPower_Configuration(frequency):
    try:
        NRP40SN.write('UNIT:POW DBM')
        Wait_Command(NRP40SN, 0.1)
        NRP40SN.write('FREQ ' + frequency)
        Wait_Command(NRP40SN, 0.1)
        NRP40SN.write('INIT:CONT OFF')
    except Exception as e:
        print('NRP40SN ReadPower_Configuration error!  ' + str(e) + '\n')
        exit(-1)

def NRP40SN_ReadPower():
    try:
        NRP40SN.write('INIT')
        Wait_Command(NRP40SN, 0.1)
        power = NRP40SN.query('FETCh?')
        return power.strip()
    except Exception as e:
        print('NRP40SN ReadPower error!  ' + str(e) + '\n')
        exit(-1)