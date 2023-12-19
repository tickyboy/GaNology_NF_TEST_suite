import pyvisa,time


def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue



def ZNB40_connect():
    global ZNB40
    rm = pyvisa.ResourceManager()
    try:
        ZNB40 = rm.open_resource('TCPIP0::10.0.0.4::inst0::INSTR')
        Wait_Command(ZNB40, 0.2)
    except Exception as e:
        print('ZNB40 connect error!  ' + str(e) + '\n')
        exit(-1)


#ZNB40初始化
def ZNB40_RST():
    try:
        ZNB40.write('*RST')
        Wait_Command(ZNB40, 0.1)
    except Exception as e:
        print('ZNB40 RST error!  ' + str(e) + '\n')
        exit(-1)

def ZNB40_measure_Configuration(frequency):
    try:
        ZNB40.write('INIT1:CONT OFF')
        ZNB40.write('INIT2:CONT OFF')
        ZNB40.write('CONF:CHAN:MEAS:OPT AUTO')
        Wait_Command(ZNB40, 0.1)
        ZNB40.write('CALC1:MARK1 ON')
        ZNB40.write('CALC1:MARK1:X ' + frequency +'Hz')
        Wait_Command(ZNB40, 0.1)
        ZNB40.write('CALC2:MARK2 ON')
        ZNB40.write('CALC2:MARK2:X ' + frequency +'Hz')
        Wait_Command(ZNB40, 0.1)
    except Exception as e:
        print('ZNB40 measure_Configuration!  ' + str(e) + '\n')
        exit(-1)


def ZNB40_readloss():
    try:
        result = []
        ZNB40.write('INIT1:IMM:ALL')
        Wait_Command(ZNB40, 0.1)
        a = float(ZNB40.query('CALC1:MARK1:Y?'))*-1
        b = float(ZNB40.query('CALC2:MARK2:Y?'))*-1
        result.append(str(a))
        result.append(str(b))
        return result
    except Exception as e:
        print('ZNB40 sinMeasureALLch!  ' + str(e) + '\n')
        exit(-1)

def ZNB40_readfile_DutSpara(file):
    try:
        ZNB40.write("MMEM:STOR:TRAC:PORTS 1,'C:\\Users\\Instrument\\Desktop\\dut_spara.s2p', LOGP, 1, 2")
        Wait_Command(ZNB40, 0.1)
        result = ZNB40.query("MMEM:DATA? 'C:\\Users\\Instrument\\Desktop\\dut_spara.s2p'")
        Wait_Command(ZNB40, 0.3)
    except Exception as e:
        print('ZNB40 readfile_DutSpara error!  ' + str(e) + '\n')
        exit(-1)
    f = open(file, 'w')
    f.write(result)
    f.close()
    f = open(file, 'r')
    s = ''
    t = '! Created: UTC8 ' + str(time.localtime().tm_year) + '/' + str(time.localtime().tm_mon) + '/' + str(
        time.localtime().tm_mday) + ', ' + str(time.localtime().tm_hour) + ':' + str(
        time.localtime().tm_min) + ':' + str(time.localtime().tm_sec)
    while True:
        l = f.readline()
        if l =='':
            break
        if l.startswith('! Created'):
            l = t + '\n'
        s = s + l
        f.readline()
    f.close()
    f = open(file, 'w')
    f.write(s)
    f.close()

