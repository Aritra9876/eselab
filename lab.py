import pyvisa as visa
import numpy as np
import matplotlib.pyplot as plt
from struct import unpack
from numpy.fft import fft,ifft
rm=visa.ResourceManager()
a=list(rm.list_resources())
print(a)
h=rm.open_resource(a[0])
print(h.query('*IDN?'))
h.write('DATA:SOU CH1')
h.write('CURVE?')
rdata=h.read_raw()
header_len=2+int(rdata[1])
trace=rdata[header_len:-1]
data=np.array(unpack('%sB' % len(trace), trace))
y0=h.query('WFMOutpre:YZE?')
dy=h.query('WFMOutpre:YMU?')
x0=h.query('WFMOutpre:XZEro?')
dx=h.query('WFMOutpre:XINcr?')
n=h.query('ACQ?')
print(x0,dx,y0,dy,n)
plt.xlabel('Time or frequency bins')
plt.ylabel('Amplitude in arbitrary units')
plt.title(h.query('*IDN?'))
#plt.plot(data)

#plt.show()
N=int(input("Number of averages"))
file = open('aq.txt', 'wb')
file.close()
for i in range(N):
    h.write('CURVE?')
    rdata=h.read_raw()
    data=0
    data+=np.array(unpack('%sB' % len(trace), trace))
    cspec=fft(data)
    pspec=np.abs(cspec)**2
    with open('aq.txt', 'a') as file:
        file.write(pspec)
    NL=len(cspec)
    num =np.arange(NL)
    SR=2E7
    ST=NL/SR
    freq=num/ST





plt.xlim(5E4,2E7)
#plt.ayhline(freq[np.where(cspec==np.max(cspec)]))
plt.plot(freq,20*np.log10(pspec))
plt.show()

