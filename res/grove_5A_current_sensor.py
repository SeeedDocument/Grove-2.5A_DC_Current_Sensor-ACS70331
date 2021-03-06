import time
from grove.i2c import Bus

ADC_DEFAULT_IIC_ADDR = 0X04

ADC_CHAN_NUM = 8

REG_RAW_DATA_START = 0X10
REG_VOL_START = 0X20
REG_RTO_START = 0X30

REG_SET_ADDR = 0XC0

sensitivity = 1000.0 / 200.0
Vref = 1498              #The value of the sensorValue is read when there is no current load.
averageValue = 500       #Take the average of 500 times
class Pi_hat_adc():
    def __init__(self,bus_num=1,addr=ADC_DEFAULT_IIC_ADDR):
        self.bus=Bus(bus_num)
        self.addr=addr
    #get n chanel data with unit mv.  
    def get_nchan_vol_milli_data(self,n):
        data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
        val =data[1]<<8|data[0]
        return val

    #get n chanel data with unit mv.  
    def get_nchan_current_data(self,n):
        val = 0
        for i in range(averageValue):
            data=self.bus.read_i2c_block_data(self.addr,REG_VOL_START+n,2)
            val +=data[1]<<8|data[0]
        val = val / averageValue
        currentVal = (val - Vref) * sensitivity
        return currentVal

ADC = Pi_hat_adc()
def main():
    while True:
        pin_voltage = ADC.get_nchan_vol_milli_data(0)   #A0
        current = ADC.get_nchan_current_data(0)         #A0
        current = round(current)
        print("pin_voltage(mV):")
        print(pin_voltage)
        print("current(mA):")
        print(current)
        print
        time.sleep(1)

if __name__ == '__main__':
    main()