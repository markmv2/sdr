import struct
import numpy as np
import matplotlib.pyplot as plt
from costas_loop import *


def read_iq(filename, N, offset):

    # read IQ samples from binary file

    # 8 bytes per pair of IQ values (always)
    M = 8

    # open file, read N pairs starting at offset
    with open(filename, mode='rb') as file:
        file.seek(offset*M)
        fileContent = file.read(M*N)

    Isamples = np.zeros(N)
    Qsamples = np.zeros(N)

    # pack 4 bytes into float
    for i in range(N):
        Isamples[i] = struct.unpack('<f', fileContent[(M*i):(M*i+M/2)])[0]
        Qsamples[i] = struct.unpack('<f', fileContent[M*i+M/2:M*i+M])[0]

    # return IQ samples as complex numbers
    samples = Isamples + Qsamples*1j
    return samples


# read N samples from .bin generated in GNU Radio
N = 8000
offset_tx = 1100006
offset_rx = 1207674
samples_tx = read_iq('data/tx_cable_1p576GHz.bin', N, offset_tx)
samples_rx = read_iq('data/rx_cable_1p576GHz.bin', N, offset_rx)

# offset is 1000011 for tx
# offset is 1107679 for rx

#plt.scatter(np.real(samples_rx), np.imag(samples_rx))
#plt.show()

(samples_rx, error_out, phase_out, freq_out) = costas_loop(samples_rx, N, 1, 0.03)

#print(calculate_evm_qpsk(samples_rx, N))

#plt.scatter(np.real(samples_rx), np.imag(samples_rx))
#plt.show()

diff_bits_tx = demod_qpsk(samples_tx, N)
data_bits_tx = differential_decode(diff_bits_tx, N, 4)

diff_bits_rx = demod_qpsk(samples_rx, N)
data_bits_rx = differential_decode(diff_bits_rx, N, 4)

start = 40000
end = 40100
#plt.plot(np.real(data_bits_tx[start:end]))
#plt.plot(np.real(data_bits_rx[start:end]))
#plt.show()

#samples_rx = np.roll(samples_rx, 11)

# plot samples (optional)
#plt.plot(np.real(corr[1000:1050]))
#plt.ylim(-2,2)
#plt.plot(np.real(samples_rx[5500:5600]))
#plt.show()

# write samples to ndarray object in .npy format
np.save('data/tx_cable_1p576GHz.npy', samples_tx)
np.save('data/rx_cable_1p576GHz.npy', samples_rx)