import pyvisa,time


def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue


def SMB100A_connect():
    global SMB100A
    rm = pyvisa.ResourceManager()
    try:
        SMB100A = rm.open_resource('TCPIP0::rssmb100a181560::inst0::INSTR')
        Wait_Command(SMB100A, 0.2)
    except Exception as e:
        print('SMB100A connect error!  ' + str(e) + '\n')
        exit(-1)



#SMB100A初始化
def SMB100A_RST():
    try:
        SMB100A.write('*RST')
        Wait_Command(SMB100A, 0.1)
    except Exception as e:
        print('SMB100A RST error!  ' + str(e) + '\n')
        exit(-1)

#SMB100A设置参数
def SMB100A_SETparas(frequency,power):
    try:
        SMB100A.write('SOUR1:FREQ ' + frequency + ' Hz')
        Wait_Command(SMB100A, 0.1)
        SMB100A.write('SOUR1:POW ' + power + ' dBm')
        Wait_Command(SMB100A, 0.1)
    except Exception as e:
        print('SMB100A SETparas error!  ' + str(e) + '\n')
        exit(-1)

#SMB100A输出信号
def SMB100A_ON():
    try:
        SMB100A.write('OUTP ON')
        Wait_Command(SMB100A, 0.1)
    except Exception as e:
        print('SMB100A ON error!  ' + str(e) + '\n')
        exit(-1)

#SMB100A停止输出信号
def SMB100A_OFF():
    try:
        SMB100A.write('OUTP OFF')
        Wait_Command(SMB100A, 0.1)
    except Exception as e:
        print('SMB100A OFF error!  ' + str(e) + '\n')
        exit(-1)