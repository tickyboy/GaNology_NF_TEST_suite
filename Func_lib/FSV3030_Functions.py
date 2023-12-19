import pyvisa,time,re


def Wait_Command(device, delaytime):
    while True:
        try:
            device.query('*OPC?')
            break
        except:
            time.sleep(delaytime)
            continue



def FSV3030_connect():
    global FSV3030
    rm = pyvisa.ResourceManager()
    try:
        FSV3030 = rm.open_resource('TCPIP0::FSV3030-101668::inst0::INSTR')
        Wait_Command(FSV3030, 0.2)
    except Exception as e:
        print('FSV3030 connect error!  ' + str(e) + '\n')
        exit(-1)


#FSV3030初始化
def FSV3030_RST():
    try:
        FSV3030.write('*RST')
    except Exception as e:
        print('FSV3030 RST error!  ' + str(e) + '\n')
        exit(-1)



#FSV3030读取单频点功率
def FSV3030_ReadPower_Configuration(frequency):
    try:
        FSV3030.write('FREQ:CENT '+ frequency +' Hz;SPAN 10 MHz')
        FSV3030.write('BAND:RES 10 Hz')
        FSV3030.write('CALC:MARK1 ON')
        FSV3030.write('CALC:MARK1:X ' + frequency + ' Hz')
        Wait_Command(FSV3030, 0.2)
    except Exception as e:
        print('FSV3030 ReadPower_Configuration error!  ' + str(e) + '\n')
        exit(-1)

def FSV3030_ReadPower():
    try:
        power = FSV3030.query('CALC:MARK1:Y?')
        return power.strip()
    except Exception as e:
        print('FSV3030 ReadPower error!  ' + str(e) + '\n')
        exit(-1)


def FSV3030_SetLoss(inputloss,outputloss):
    try:
        FSV3030.write('CORR:LOSS:INP:MODE SPOT')
        FSV3030.write('CORR:LOSS:INP:SPOT ' + inputloss)
        FSV3030.write('CORR:LOSS:OUTP:MODE SPOT')
        FSV3030.write('CORR:LOSS:OUTP:SPOT ' + outputloss)
    except Exception as e:
        print('FSV3030 SetLoss error!  ' + str(e) + '\n')
        exit(-1)



def FSV3030_ReadNF():
    try:
        result = FSV3030.query('TRAC1? TRACE1,NOIS')
        nf = re.findall(r"\-?\d+\.?\d*", result)
        return nf
    except Exception as e:
        print('FSV3030 ReadNF error!  ' + str(e) + '\n')
        exit(-1)



def FSV3030_ReadGAIN():
    try:
        result = FSV3030.query('TRAC2? TRACE1,GAIN')
        gain = re.findall(r"\-?\d+\.?\d*", result)
        return gain
    except Exception as e:
        print('FSV3030 ReadGAIN error!  ' + str(e) + '\n')
        exit(-1)







def FSV3030_ReadYfactor():
    try:
        result = FSV3030.query('TRAC2? TRACE1,YFAC')
        yfac = re.findall(r"\-?\d+\.?\d*", result)
        return yfac
    except Exception as e:
        print('FSV3030 ReadYfactor error!  ' + str(e) + '\n')
        exit(-1)


def FSV3030_INITsingle():
    try:
        FSV3030.write('INIT:CONT OFF')
        FSV3030.write('INIT')
        Wait_Command(FSV3030, 0.2)
    except Exception as e:
        print('FSV3030 INITsingle error!  ' + str(e) + '\n')
        exit(-1)


def FSV3030_SetLosstable(inLoss_table, ouLoss_table):
    try:
        FSV3030.write('CORR:LOSS:INP:MODE TABL')
        FSV3030.write('CORR:LOSS:INP:TABL:SEL "S1"')
        FSV3030.write('CORR:LOSS:INP:TABL ' + inLoss_table)
        FSV3030.write('CORR:LOSS:OUTP:MODE TABL')
        FSV3030.write('CORR:LOSS:OUTP:TABL:SEL "S2"')
        FSV3030.write('CORR:LOSS:OUTP:TABL ' + ouLoss_table)
    except Exception as e:
        print('FSV3030 SetLosstable error!  ' + str(e) + '\n')
        exit(-1)


