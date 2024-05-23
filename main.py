import os
import subprocess
import time
import streamlit as st
import streamlink
from langchain.chat_models.gigachat import GigaChat
from speechkit import configure_credentials, creds, model_repository
from speechkit.stt import AudioProcessingType
from langchain.schema import HumanMessage, SystemMessage

configure_credentials(
    yandex_credentials=creds.YandexCredentials(api_key='AQVN3qwuRDroqa-9P2bAlSWuh_UVmVe_CiOHmEdF')
)

client_id = "1a8c7831-f59c-4904-9455-608bc1a3f2af"
client_secret = "609bd2e6-a51c-4ad0-8dcf-60fd55dc2e71"
authorization_data = "MWE4Yzc4MzEtZjU5Yy00OTA0LTk0NTUtNjA4YmMxYTNmMmFmOjYwOWJkMmU2LWE1MWMtNGFkMC04ZGNmLTYwZmQ1NWRjMmU3MQ=="
chat = GigaChat(credentials=authorization_data, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


class StreamProcessor:
    def __init__(self):
        self.all_result_str = ""
        self.stop = False
        self.future = None

    def short(self, chat):

        messages = [
            SystemMessage(content="Привет, нужно пересказать текст из транскрибированного аудио для моего проекта:"),
            HumanMessage(content=self.all_result_str)
        ]
        st.write("Sending to GigaChat: ", self.all_result_str)
        try:
            res = chat(messages)
            st.write("Received from GigaChat: ", res.content)
        except Exception as e:
            st.write("Error in GigaChat API call: ", str(e))

    def process_stream(self, url):
        all_result = []
        try:
            st.write(f"Вы запустили алгоритм для URL: {url}")
            streams = streamlink.streams(url)
            audio_stream = streams["audio_only"]

            model = model_repository.recognition_model()
            model.model = 'general:rc'
            model.language = 'ru-RU'
            model.audio_processing_type = AudioProcessingType.Full

            i = 0
            while not self.stop:
                duration = 20
                start = i * duration
                output = f"fragment4_{i + 1}.mp3"
                ffmpeg = [
                    "ffmpeg",
                    "-i", audio_stream.url,
                    "-ss", str(start),
                    "-t", str(duration),
                    "-vn",
                    "-c", "copy",
                    "-acodec", "libmp3lame",
                    output
                ]

                result = subprocess.run(ffmpeg, capture_output=True, text=True)
                if result.returncode != 0:
                    st.write("Error during FFmpeg process: ", result.stderr)
                    continue

                if os.path.exists(output):
                    try:
                        result = model.transcribe_file(output)
                        all_result.append(result[0].normalized_text)
                        #st.write("real-time text: ", result[0].normalized_text)
                    except Exception as e:
                        st.write(f"Error transcribing file {output}: {e}")
                    finally:
                        os.remove(output)

                #st.write("all result ", all_result)
                self.all_result_str = '\n'.join(all_result)
                st.write("Обновеленный текст: ", self.all_result_str)
                i += 1
                time.sleep(5)  # Ensure enough time for next file to process
        except Exception as e:
            st.error(f'Произошла ошибка: {e}')
        return self.all_result_str

# Additional styles for the page
st.write("""
    <style> 
    .rectangle { 
        width: 700px; 
        height: 550px; 
         
        margin: auto; 
        padding: 20px; 
    } 
    </style> 
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center; color: #42aaff;'>Short Live</h1>", unsafe_allow_html=True)

# CSS styles
css = """
<style>
    body {
        z-index:100;
    }
    .container {
        display: flex;
        flex-direction: row;
        align-items: center;
    }
    .rectangle {
        width: 700px;
        height: 550px;
        background-color: transparent;
        margin-bottom: 20px;
        margin-left: -400px;
    }
    /* footer */
    .d-flex {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    footer {
        padding-bottom: 30px;
        font-size: 22px;
        width: 100%;
        padding-left: 20px;
        padding-right: 20px;
    }
    footer img {
        display: inline;
    }
    .in_footer {
        max-width: 1440px;
        margin: 0 auto;
        align-items: flex-start;
    }
    .in_footer a {
        text-decoration: none;
        color: #000;
        font-weight: 200;
    }
    .in_footer .left img {
        width: 33px;
        height: 21px;
        margin-top: 10px;
        display: inline;
        margin-right: 50px;
    }
    .in_footer .main {
        font-weight: 700;
        margin-left: 70px;
        margin-bottom: 50px;
    }
    .in_footer p {
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 10px;
    }
    .in_footer .end {
        font-weight: 400;
        font-size: 25px;
    }
    .in_footer1 {
        max-width: 1440px;
        margin: 0 auto;
        align-items: flex-start;  
    }
    footer .bott {
        margin-top: 50px;
        text-align: center;
    }
    footer figure {
        display: inline-block;
        text-align: center;
        margin-bottom: 30px;
    }
    footer figure img {
        width: 50px;
        height: 54px;
        vertical-align: top;
        display: inline;
    }
    footer figure figcaption {
        font-weight: 300;
        font-size: 25px;
        display: table;
        text-align: center;
    }
    footer hr {
        margin: 40px 0px;
    }
    a {
        color: blue;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
</style>
"""

# Adding CSS to the app
st.markdown(css, unsafe_allow_html=True)

# Function with your algorithm

st.sidebar.info(
    """ 
    \tВведите URL онлайн аудиопотока, который нужно обработать 
"""
)
with st.sidebar.container():
    url = st.text_input('Вставьте URL', key="text_input", value="")
    submitted = st.button('Отправить')

processor = StreamProcessor()

if submitted:
    st.session_state['processor'] = processor
    processor.stop = False
    st.session_state['result'] = processor.process_stream(url)

stop_record = st.sidebar.button('Прервать текст')
if stop_record:
    if 'processor' in st.session_state:
        st.session_state['processor'].stop = True
        processor = st.session_state['processor']
        processor.stop = True
        st.write(processor.all_result_str)

# Handle the "NEW" button click
if submitted:
    processor.process_stream(url)

st.sidebar.info(
    """ 
    \tНаша система начнет анализировать аудиопоток с указанного URL.\n\n 
    \tПолученный текст отправится в чат, где Вы сможете просмотреть краткое содержание аудиозаписи и поделиться своими мыслями и комментариями. 
    """
)

# Handle the "Stop Text" button click
if stop_record:
    st.write("Текст был прерван.")

# Layout the rectangles
st.markdown('<div class="container">', unsafe_allow_html=True)
st.markdown('<div class="rectangle"></div>', unsafe_allow_html=True)
st.markdown('<div class="rectangle2"></div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
def footer():
    st.markdown(r"""       
        <footer>
            <hr>
            <div class="in_footer d-flex">
                <div class="left">
                    <p style="font-size: 23px;">Наши контакты:</p>
                    <nav>
                        <p style="font-size: 18px;">Техническая поддержка по общим вопросам:</p>
                        <div style="display: flex; align-items: center;">
                            <img src="https://img.freepik.com/premium-vector/telegram-logo-icon-set-messaging-app-brand-symbols-vector_628407-1823.jpg" alt="Телеграм" style="width: 50px; height: 50px; margin-right: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); border-radius: 5px;">
                            <a href="https://t.me/+TmmKKAg8PmJmM2Uy">Телеграм</a>
                        </div>
                    </nav>
                    <p style="font-size: 18px;">Наш проект:</p>
                    <div style="display: flex; align-items: center;">
                        <img src="https://w7.pngwing.com/pngs/670/396/png-transparent-computer-icons-github-icon-design-logo-github-cat-like-mammal-carnivoran-logo-thumbnail.png" alt="ГитХаб" style="width: 50px; height: 50px; margin-right: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); border-radius: 5px;">
                        <a href="https://github.com/Dom1no456/RTTS">GitHub</a>
                    </div>
                    <div style="display: flex; align-items: center;">
                        <img src="https://yt3.googleusercontent.com/ytc/APkrFKYAYEfAP-OXfWIF7FKVZB7xNnRgahxcOTlMwZP3=s900-c-k-c0x00ffffff-no-rj" alt="КлиарМЛ" style="width: 50px; height: 50px; margin-right: 10px; margin-top: 15px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1); border-radius: 5px;">
                        <a href="https://app.clear.ml/projects/301eaa1271a24e378b9ae8b3cde3919f/experiments/8e979876278d4392bd4427cc7f188c61/output/execution">ClearML</a>
                    </div>
                </div>
                <div class="right">
                    <p class="main" style="font-size: 23px;">Схема проезда:</p>
                    <iframe src="https://yandex.ru/map-widget/v1/?um=constructor%3A462232a5eb9cd2e4f291ee14696f914ac8d762691ad7617dbb3a44816fec42a9&amp;source=constructor&z=10" width="353" height="284" frameborder="0" style="margin-left: 20px;"></iframe>
                </div>
            </div>
            <div class="bott">
                <p class="end">Казань, 2024</p>
            </div>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    footer()
