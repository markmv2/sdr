import struct
import numpy as np
import matplotlib.pyplot as plt

def read_iq(filename, N, offset):

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


def costas_loop(samples, N, alpha, beta):

    phase = 0
    freq = 0

    samples_out = np.zeros(N, dtype=np.complex)
    error_out = np.zeros(N)
    phase_out = np.zeros(N)
    freq_out = np.zeros(N)

    for i in range(N):

        samples_out[i] = samples[i] * np.exp(-1j*phase)

        # estimate error
        error = np.sign(np.real(samples_out[i])) * np.imag(samples_out[i]) - np.sign(np.imag(samples_out[i])) * np.real(samples_out[i])
        error_out[i] = error

        # accumulate freq and phase offset 
        freq += beta * error
        phase += freq + (alpha * error)

        while phase >= 2*np.pi:
            phase -= 2*np.pi
        while phase < 0:
            phase += 2*np.pi
        
        phase_out[i] = phase
        freq_out[i] = freq
        
    return (samples_out, error_out, phase_out, freq_out)


def calculate_evm_qpsk(samples, N):

    error_sum = 0

    # sum the squared error vector over all symbols
    # reference constellations have magnitude of 1
    for i in range(N):
        samples_I = np.real(samples[i])
        samples_Q = np.imag(samples[i])
        error_sum += (samples_I - np.sign(samples_I)*1/np.sqrt(2))**2 + (samples_Q - np.sign(samples_Q) * 1/np.sqrt(2))**2

    # average over all samples and take square root for rms value
    error_avg = error_sum/N
    evm_rms = np.sqrt(error_avg)
    evm_db = 20*np.log10(evm_rms)

    return (evm_rms, evm_db)


def demod_qpsk(samples, N):

    bits = np.zeros(N, dtype = np.byte)

    for i in range(N):
        real_sign = np.sign(np.real(samples[i]))
        imag_sign = np.sign(np.imag(samples[i]))

        # symbol mapping must be consistent
        if (real_sign == 1 and imag_sign == 1):
            bits[i] = 0
        elif (real_sign == -1 and imag_sign == 1):
            bits[i] = 1
        elif (real_sign == -1 and imag_sign == -1):
            bits[i] = 2
        else:
            bits[i] = 3

    return bits


def differential_decode(bits_in, N, modulus):

    bits_out = np.zeros(N, dtype = np.byte)
    prev = np.byte(0)

    for i in range(N):
        bits_out[i] = (bits_in[i] - prev) % modulus
        prev = bits_in[i]

    return bits_out




# read IQ samples from file, after gnu radio clock sync
N = 2048
samples = read_iq("data/clock_sync_200MHz.bin", N, 1000000)

# read IQ samples from file, after gnu radio costas loop
gnucostas = read_iq("data/phase_sync_200MHz.bin", N, 1000000)

# try different alpha and beta values to optimize evm
#for i in range(10):
    #(samples_out, error_out, phase_out, freq_out) = costas_loop(samples, N, 0.6, 0.03)
    #print(calculate_evm_qpsk(samples_out, N))

(samples_out, error_out, phase_out, freq_out) = costas_loop(samples, N, 0.13177, 0.009318)

# demodulate symbols
diff_bits = demod_qpsk(samples_out, N)
data_bits = differential_decode(diff_bits, N, 4)

# plot data