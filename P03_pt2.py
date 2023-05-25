import numpy as np
import matplotlib.pyplot as plt

# Parâmetros do filtro
N = 37  # Comprimento do filtro
M = 36
wc = 0.66 * np.pi  # Frequência de corte (rad)

# Janela retangular
n = np.arange(N)
# print(n)
W = 1

# Função de transferência do filtro com janela aplicada
hd = np.sin(wc * (n - (M/2))) / (np.pi * (n - (M/2)))
# print(hd)
hd[18] = 0.66
erro = wc / np.pi
# print(erro)

# Calcular a DFT usando numpy.fft.fft
H = np.fft.fft(hd)

# Calcular as frequências correspondentes
frequencies = np.fft.fftfreq(len(hd))
frequencies = frequencies * 13000

plt.figure(figsize=(12, 10))

# Plot da resposta ao impulso do filtro
plt.subplot(2, 1, 1)
# plt.figure()
plt.stem(n, hd)
plt.xlabel('Amostras (n)')
plt.ylabel('Amplitude - h[n]')
plt.title('Resposta ao Impulso')
plt.grid(True)
plt.axvline(0, color='k')
plt.axhline(0, color='k')
# plt.show()

# Plot da resposta em frequência do filtro
plt.subplot(2, 1, 2)
# plt.figure()
plt.plot(frequencies, 20*np.log10(np.abs(H)))
plt.xlabel('Frequência (Hz)')
plt.ylabel('Amplitude - H[n]')
plt.title('Resposta em frequência')
plt.grid(True)
plt.axvline(0, color='k')
plt.axhline(0, color='k')
# plt.show()

# Ajustar a exibição dos gráficos
plt.tight_layout()
# Nome da figura
plt.savefig("graficos - parte 2.png")
# Mostrar os gráficos
plt.show()
