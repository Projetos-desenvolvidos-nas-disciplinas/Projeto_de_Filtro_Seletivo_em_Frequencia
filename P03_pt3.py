import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import lfilter

def add_noise(voz, a1, a2):
    n = np.arange(len(voz))  # Eixo do tempo
    noise = a1 * np.cos(0.87 * np.pi * n) + a2 * np.cos(0.92 * np.pi * n)
    voz_ruidosa = voz + noise
    return voz_ruidosa

# Configurações
duração_gravação = 5  # Duração em segundos
taxa_amostragem = 44100  # Taxa de amostragem em Hz
ruido_voz = "Ruido + Voz"
voz_normal = "Voz normal"
voz_filtrada = "Voz filtrada"

# Gravar áudio
print("Gravando...")
voz = sd.rec(int(duração_gravação * taxa_amostragem), samplerate=taxa_amostragem, channels=1)
sd.wait()

# Adicionar ruído
voz_ruidosa = add_noise(voz.flatten(), 0.7, 0.7)

def apply_filter(signal, filter_coeffs):
    filtered_signal = lfilter(filter_coeffs, 1, signal)
    return filtered_signal

# Parâmetros do filtro
N = 37  # Comprimento do filtro
M = 36
wc = 0.66 * np.pi  # Frequência de corte (rad)

# Janela retangular
nf = np.arange(N)
# print(n)
W = 1

# Função de transferência do filtro com janela aplicada
hd = np.sin(wc * (nf - (M/2))) / (np.pi * (nf - (M/2)))
# print(hd)
hd[18] = 0.66

# Filtro para remover o ruído
# filtered_signal = np.convolve(noisy_signal, noise[::-1], mode='same')
# filtered_signal = filter(hd, voz_ruidosa)
# print(filtered_signal)
filtered_signal = apply_filter(voz_ruidosa, hd)

# Salvar arquivo WAV
nome_arquivo_wav1 = ruido_voz + ".wav"
sf.write(nome_arquivo_wav1, voz_ruidosa, taxa_amostragem)

nome_arquivo_wav2 = voz_normal + ".wav"
sf.write(nome_arquivo_wav2, voz.flatten(), taxa_amostragem)

nome_arquivo_wav3 = voz_filtrada + ".wav"
sf.write(nome_arquivo_wav3, filtered_signal, taxa_amostragem)

print("Gravação concluída e arquivo salvo.")

# Plot dos gráficos
time = np.linspace(0, duração_gravação, num=len(voz))
plt.figure(figsize=(12, 10))

# Sinal de voz original
plt.subplot(3, 1, 1)
plt.plot(time, voz.flatten(), color = "orange")
plt.title("Sinal de Voz Original")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.ylim(-0.25, 0.25)

# Sinal de voz com ruído
plt.subplot(3, 1, 2)
plt.plot(time, voz_ruidosa, color = "red")
plt.title("Sinal de Voz com Ruído")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")

# Sinal de voz filtrado
plt.subplot(3, 1, 3)
plt.plot(time, filtered_signal, color = "green")
plt.title("Sinal de Voz Filtrado")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")
plt.ylim(-0.25, 0.25)

"""# Sinal do ruído
plt.subplot(4, 1, 4)
plt.plot(time, noise)
plt.title("Sinal do Ruído")
plt.xlabel("Tempo (s)")
plt.ylabel("Amplitude")"""

plt.tight_layout()
plt.savefig("graficos - parte 3.png")
plt.show()
