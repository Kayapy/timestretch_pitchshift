import streamlit as st
import torchaudio
import torch
import io
import base64

# Carregar o arquivo de áudio
def carregar_audio(file):
    waveform, sample_rate = torchaudio.load(file)
    return waveform, sample_rate

# Função para aplicar pitch shift
def aplicar_pitch_shift(waveform, sample_rate, pitch_shift):
    transform = torchaudio.transforms.PitchShift(sample_rate, n_steps=pitch_shift)
    return transform(waveform)

# Função para obter a codificação base64 de um arquivo binário
@st.cache_data(show_spinner=False)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Função para definir a imagem de fundo da página
def set_jpeg_as_page_bg(jpeg_file):
    bin_str = get_base64_of_bin_file(jpeg_file)
    page_bg_img = '''
    <style>
    .stApp {
        background-image: url("data:image/jpeg;base64,%s");
        background-size: cover;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# Definir a imagem de fundo (substitua 'background.jpg' pelo caminho do seu arquivo JPEG)
set_jpeg_as_page_bg('backgroundapp.jpg')

# Conteúdo do aplicativo Streamlit
st.title("Time Stretch + Pitch Shift")

uploaded_file = st.file_uploader("Escolha um arquivo de áudio", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav', start_time=0)
    waveform, sample_rate = carregar_audio(uploaded_file)

    pitch_shift = st.slider("Pitch Shift (semitones)", -12, 12, 0)

    if st.button("Aplicar Pitch Shift"):
        try:
            waveform_shifted = aplicar_pitch_shift(waveform, sample_rate, pitch_shift)
            # Salvar o áudio processado temporariamente em um buffer de memória
            output_file = 'output_pitch_shifted.wav'
            torchaudio.save(output_file, waveform_shifted, sample_rate)
            st.success(f"Áudio processado salvo como {output_file}")
        except Exception as e:
            st.error(f"Erro ao aplicar Pitch Shift: {e}")

    # Botões de controle de reprodução para o áudio original
    if st.button("Play Original"):
        st.audio(uploaded_file, format='audio/wav', start_time=0)

    # Botões de controle de reprodução para o áudio processado
    if 'output_file' in locals():
        if st.button("Play Processed"):
            st.audio(output_file, format='audio/wav', start_time=0)

