set "PATH=%CD%\ffmpeg;%PATH%"
set NO_PROXY=localhost,127.0.0.1
set REF_AUDIO=参考音频.wav
set REF_AUDIO_TXT=もちろん、時々善良で誠実な大人が客人としてやってくることもあるけれど
set REF_AUDIO_LANG=日文
set OPT_LANG=日文
set TORCH_CUDNN_V8_API_DISABLED=1
runtime\python.exe GPT_SoVITS\inference_webui_fast.py
pause