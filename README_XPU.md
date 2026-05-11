# 关于更换到XPU的说明

就是根据deepseek老师的指导，把代码中的`cuda`替换成了`xpu`（

## 推理

目前只关注v2ProPlus，其他版本能不能用还缺乏测试。这个指南也是以“顺利推理 v2ProPlus 模型”为目标编写的。

### 准备运行时

为了保证python运行环境互不影响，我们从头搭建一个独立的python运行环境。以下操作假定你的网络环境没问题。

- 下载并解压`GPT-SoVITS-Intel-XPU.zip`。
- 打开`GPT-SoVITS-Intel-XPU`文件夹。接下来的操作都将以这个文件夹所在位置为基础（根目录）。
- 右键文件管理器空白处，选择`在终端中打开`，然后保留这个黑色窗口（终端）备用。另外，如果你打开的不是`命令提示符`而是`PowerShell`，输入`cmd`
   并回车，切换到命令提示符环境，方面统一后续操作。
- 在根目录下建立一个`runtime`文件夹。下载[嵌入式Python环境(3.11.9)](https://www.python.org/ftp/python/3.11.9/python-3.11.9-embed-amd64.zip)，解压，
   然后将解压后的文件全部移入`runtime`，确保`runtime`下有一个`python.exe`。
- 用记事本打开`runtime\python311._pyh`，将其全部内容替换为以下内容，然后保存。

```python
python311.zip
.

# Uncomment to run site.main() automatically
./Lib/site-packages
import site

```

- 安装pip。浏览器打开[get-pip.py](https://bootstrap.pypa.io/get-pip.py)，将其另存为`get-pip.py`，放在根目录下。（打开该网站可能需要工具。确认下载完的文件是完整的：大小在2MB出头）
- 在终端中输入：`untime\python get-pip.py`，等待其输出`Successfully installed...`字样。
- 在终端中输入：`runtime\python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/xpu`，等待其输出`Successfully installed...`字样。
- 在终端中输入：`runtime\python -m pip install -r requirements.txt`，等待其输出`Successfully installed...`字样。
- 在终端中输入：`runtime\python test-gpu.py`，看看输出中有没有出现你的显卡。如果有，那就是没问题了。

### 下载模型和其他资源

一定需要的模型：

- `GPT_SoVITS\pretrained_models\sv\pretrained_eres2netv2w24s4ep4.ckpt`
- `GPT_SoVITS\pretrained_models\chinese-roberta-wwm-ext-large`
- `GPT_SoVITS\pretrained_models\chinese-hubert-base`
- `GPT_SoVITS\pretrained_models\fast_langdetect`：需要手动创建该文件夹，之后程序应该会自动下载模型。或者也可以从[](ttps://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin)下载并手动放入。

不一定需要，但是为了方便可以添加的模型：

- `GPT_SoVITS/pretrained_models/s1v3.ckpt`
- `GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth`

这两个模型纯粹是为了简化启动流程而使用的。手动修改`tts_infer.yaml`，可以不依赖这两个模型启动推理：将`custom.t2s_weights_path`和`custom.vits_weights_path`改为自己模型所在路径即可。

- `GPT_SoVITS/text/G2PWModel`如果模型涉及到中文（多音字），会使用到该模型。这个模型会在需要的时候自动下载。
- `runtime\nltk_data`如果模型涉及到英文，就需要这个NLTK。不过它不太能自动下载，需要手动放入文件。

对于以上模型，打开[整合包及模型下载链接](https://www.yuque.com/baicaigongchang1145haoyuangong/ib3g1e/dkxgpiy9zb96hob4)，然后选择合适的链接下载。从现有的整合包里复制过来也没问题。

### ffmpeg

直接把一整个的`ffmpeg.exe`放在根目录下不管用了。从[BtbN/FFmpeg-Builds](https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl-shared.zip)下载共享的ffmpeg库，解压，将解压后的文件全部移入`ffmpeg`文件夹内。当然直接放根目录也可以，不过那样会显得根目录更加乱了……

### 启动

启动前可以先编辑`推理webui.bat`。主要是提供了一些参数，可以为推理webui指定一些默认参数。

```batch
# 这里把我们的ffmpeg文件夹添加到环境变量
set "PATH=%CD%\ffmpeg;%PATH%" #

# 填入默认的主要参考音频路径
set REF_AUDIO=参考音频.wav

# 默认的主参考音频的文本
set REF_AUDIO_TXT=もちろん、時々善良で誠実な大人が客人としてやってくることもあるけれど

# 默认的主参考音频的语种
set REF_AUDIO_LANG=日文

# 默认的合成的音频的语种
set OPT_LANG=日文
```

API目前没有变化。

## 训练
