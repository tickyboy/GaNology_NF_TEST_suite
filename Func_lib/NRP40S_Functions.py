import pyvisa,time

def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue


def NRP40S_connect():
    global NRP40S
    rm = pyvisa.ResourceManager()
    try:
        NRP40S = rm.open_resource('TCPIP0::10.0.0.13::inst0::INSTR')
        Wait_Command(NRP40S, 0.2)
    except Exception as e:
        print('NRP40S connect error!  ' + str(e) + '\n')
        exit(-1)



def NRP40S_RST():
    try:
        NRP40S.write('*RST')
        Wait_Command(NRP40S, 0.1)
    except Exception as e:
        print('NRP40S RST error!  ' + str(e) + '\n')
        exit(-1)


def NRP40S_ReadPower_Configuration(frequency):
    try:
        NRP40S.write('UNIT:POW DBM')
        Wait_Command(NRP40S, 0.1)
        NRP40S.write('FREQ ' + frequency)
        Wait_Command(NRP40S, 0.1)
        NRP40S.write('INIT:CONT OFF')
    except Exception as e:
        print('NRP40S ReadPower_Configuration error!  ' + str(e) + '\n')
        exit(-1)

def NRP40S_ReadPower():
    try:
        NRP40S.write('INIT')
        Wait_Command(NRP40S, 0.2)
        power = NRP40S.query('FETCh?')
        return power.strip()
    except Exception as e:
        print('NRP40S ReadPower error!  ' + str(e) + '\n')
        exit(-1)