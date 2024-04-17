import time
import subprocess
import streamlink
import os
from speechkit import configure_credentials, creds
from speechkit.stt import AudioProcessingType
from speechkit import model_repository
from clearml import Task
from langchain.chat_models.gigachat import GigaChat
from langchain.schema import HumanMessage, SystemMessage

configure_credentials(
    yandex_credentials=creds.YandexCredentials(api_key='AQVN3qwuRDroqa-9P2bAlSWuh_UVmVe_CiOHmEdF')
)

client_id = "1a8c7831-f59c-4904-9455-608bc1a3f2af"
client_secret = "0a6fc530-79bd-4497-b37f-bf2cc10e5c97"
authorization_data = "MWE4Yzc4MzEtZjU5Yy00OTA0LTk0NTUtNjA4YmMxYTNmMmFmOjBhNmZjNTMwLTc5YmQtNDQ5Ny1iMzdmLWJmMmNjMTBlNWM5Nw=="
chat = GigaChat(credentials=authorization_data, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

def start_clearml_task():
    task = Task.init(project_name='RTTS', task_name='experiment')
    return task


def upload_audio_artifact(task, output):
    audio_artifact = task.upload_artifact(name='Custom_audio', artifact_object=output)
    task.get_logger().report_media(
        title='audio',
        series='tada',
        iteration=1,
        local_path=output
    )


def transcribe_audio(output):
    model = model_repository.recognition_model()
    model.model = 'general:rc'
    model.language = 'ru-RU'
    n = "й"
    model.audio_processing_type = AudioProcessingType.Full

    result = model.transcribe_file(output)
    return result


def process_audio(task, url, chat):
    streams = streamlink.streams(url)
    audio_stream = streams["audio_only"]
    n='z'
    all_result = []
    for i in range(3):
        duration = 30
        start = i * duration
        output = f"fragmen({n})_{i + 1}.mp3"
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
        subprocess.run(ffmpeg)
        time.sleep(2)

        upload_audio_artifact(task, output)

        result = transcribe_audio(output)
        all_result.append(result[0].normalized_text)
        print(f"Text {output}: {result[0].normalized_text}")

    all_result_str = '\n'.join(all_result)

    messages = [
        SystemMessage(
            content="Сократи текст:"
        )
    ]
    messages.append(HumanMessage(content=all_result_str))
    res = chat(messages)
    return res

    print("Response from bot:", res.content)


def short_text(url_input):
    task = start_clearml_task()
    url = url_input
    res=process_audio(task, url, chat)
    task.close()
    print("Task completed")
    return res


if __name__ == "__main__":
    short_text()
