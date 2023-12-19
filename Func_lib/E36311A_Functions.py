import pyvisa,time


def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue



def DC_supply_connect():
    global DC_supply
    rm = pyvisa.ResourceManager()
    try:
        DC_supply = rm.open_resource('USB0::0x2A8D::0x1002::MY58420959::INSTR')
        Wait_Command(DC_supply, 0.2)
    except Exception as e:
        print('DC_supply connect error!  ' + str(e) + '\n')
        exit(-1)



def DC_supply_RST():
    try:
        DC_supply.write('*RST')
    except Exception as e:
        print('DC_supply RST error!  ' + str(e) + '\n')
        exit(-1)


def DC_readCurrent(port):
    i = float(DC_supply.query('MEAS:CURR? (@' + port + ')'))
    return i

def DC_readVoltage(port):
    v = float(DC_supply.query('MEAS:VOLT? (@' + port + ')'))
    return v

def DC_on(port):
    DC_supply.write('OUTP ON,(@' + port + ')')

def DC_off(port):
    DC_supply.write('OUTP OFF,(@' + port + ')')
def DC_setVI(port, v, i):
    DC_supply.write('APPL Ch' + port + ', ' + v + ', ' + i)