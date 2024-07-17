import streamlit as st
import torchaudio
import io
import base64


# Carregar o arquivo de áudio
def carregar_audio(file):
    waveform, sample_rate=torchaudio.load(file)
    return waveform, sample_rate


# Função para aplicar time stretch
def aplicar_time_stretch(waveform, sample_rate, rate):
    transform=torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=int(sample_rate * rate))
    return transform(waveform)


# Função para obter a codificação base64 de um arquivo binário
@st.cache_data(show_spinner=False)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data=f.read()
    return base64.b64encode(data).decode()


# Função para definir a imagem de fundo da página
def set_jpeg_as_page_bg(jpeg_file):
    bin_str=get_base64_of_bin_file(jpeg_file)
    page_bg_img='''
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
set_jpeg_as_page_bg('C:/Users/kayap/PycharmProjects/Fretnut App/Fretnut.venv/backgroundapp2.jpg')

# Conteúdo do aplicativo Streamlit
st.title("Time Stretch + Pitch Time")

uploaded_file=st.file_uploader("Escolha um arquivo de áudio", type=["wav"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav', start_time=0)
    waveform, sample_rate=carregar_audio(uploaded_file)

    rate=st.slider("Time Stretch (rate)", 0.5, 2.0, 1.0, step=0.1)

    if st.button("Aplicar Time Stretch"):
        try:
            waveform_stretched=aplicar_time_stretch(waveform, sample_rate, rate)
            # Salvar o áudio processado temporariamente em um buffer de memória
            output_buffer=io.BytesIO()
            torchaudio.save(output_buffer, waveform_stretched, sample_rate, format='wav')
            st.audio(output_buffer, format='audio/wav')
        except Exception as e:
            st.error(f"Erro ao aplicar Time Stretch: {e}")

    # Botões de controle de reprodução para o áudio original
    if st.button("Play Original"):
        st.audio(uploaded_file, format='audio/wav', start_time=0)

    # Botões de controle de reprodução para o áudio processado
    if 'output_buffer' in locals():
        if st.button("Play Processed"):
            st.audio(output_buffer, format='audio/wav', start_time=0)
