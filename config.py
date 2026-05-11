import os
import re
import sys

import torch

from tools.i18n.i18n import I18nAuto

i18n = I18nAuto(language=os.environ.get("language", "Auto"))


pretrained_sovits_name = {
    "v1": "GPT_SoVITS/pretrained_models/s2G488k.pth",
    "v2": "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    "v3": "GPT_SoVITS/pretrained_models/s2Gv3.pth",  ###v3v4还要检查vocoder，算了。。。
    "v4": "GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth",
    "v2Pro": "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2Pro.pth",
    "v2ProPlus": "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth",
}

pretrained_gpt_name = {
    "v1": "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
    "v2": "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt",
    "v3": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
    "v4": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
    "v2Pro": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
    "v2ProPlus": "GPT_SoVITS/pretrained_models/s1v3.ckpt",
}
name2sovits_path = {
    # i18n("不训练直接推v1底模！"): "GPT_SoVITS/pretrained_models/s2G488k.pth",
    i18n("不训练直接推v2底模！"): "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s2G2333k.pth",
    # i18n("不训练直接推v3底模！"): "GPT_SoVITS/pretrained_models/s2Gv3.pth",
    # i18n("不训练直接推v4底模！"): "GPT_SoVITS/pretrained_models/gsv-v4-pretrained/s2Gv4.pth",
    i18n("不训练直接推v2Pro底模！"): "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2Pro.pth",
    i18n("不训练直接推v2ProPlus底模！"): "GPT_SoVITS/pretrained_models/v2Pro/s2Gv2ProPlus.pth",
}
name2gpt_path = {
    # i18n("不训练直接推v1底模！"):"GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt",
    i18n(
        "不训练直接推v2底模！"
    ): "GPT_SoVITS/pretrained_models/gsv-v2final-pretrained/s1bert25hz-5kh-longer-epoch=12-step=369668.ckpt",
    i18n("不训练直接推v3底模！"): "GPT_SoVITS/pretrained_models/s1v3.ckpt",
}
SoVITS_weight_root = [
    "SoVITS_weights",
    "SoVITS_weights_v2",
    "SoVITS_weights_v3",
    "SoVITS_weights_v4",
    "SoVITS_weights_v2Pro",
    "SoVITS_weights_v2ProPlus",
]
GPT_weight_root = [
    "GPT_weights",
    "GPT_weights_v2",
    "GPT_weights_v3",
    "GPT_weights_v4",
    "GPT_weights_v2Pro",
    "GPT_weights_v2ProPlus",
]
SoVITS_weight_version2root = {
    "v1": "SoVITS_weights",
    "v2": "SoVITS_weights_v2",
    "v3": "SoVITS_weights_v3",
    "v4": "SoVITS_weights_v4",
    "v2Pro": "SoVITS_weights_v2Pro",
    "v2ProPlus": "SoVITS_weights_v2ProPlus",
}
GPT_weight_version2root = {
    "v1": "GPT_weights",
    "v2": "GPT_weights_v2",
    "v3": "GPT_weights_v3",
    "v4": "GPT_weights_v4",
    "v2Pro": "GPT_weights_v2Pro",
    "v2ProPlus": "GPT_weights_v2ProPlus",
}


def custom_sort_key(s):
    # 使用正则表达式提取字符串中的数字部分和非数字部分
    parts = re.split("(\d+)", s)
    # 将数字部分转换为整数，非数字部分保持不变
    parts = [int(part) if part.isdigit() else part for part in parts]
    return parts


def get_weights_names():
    SoVITS_names = []
    for key in name2sovits_path:
        if os.path.exists(name2sovits_path[key]):
            SoVITS_names.append(key)
    for path in SoVITS_weight_root:
        if not os.path.exists(path):
            continue
        for name in os.listdir(path):
            if name.endswith(".pth"):
                SoVITS_names.append("%s/%s" % (path, name))
    if not SoVITS_names:
        SoVITS_names = [""]
    GPT_names = []
    for key in name2gpt_path:
        if os.path.exists(name2gpt_path[key]):
            GPT_names.append(key)
    for path in GPT_weight_root:
        if not os.path.exists(path):
            continue
        for name in os.listdir(path):
            if name.endswith(".ckpt"):
                GPT_names.append("%s/%s" % (path, name))
    SoVITS_names = sorted(SoVITS_names, key=custom_sort_key)
    GPT_names = sorted(GPT_names, key=custom_sort_key)
    if not GPT_names:
        GPT_names = [""]
    return SoVITS_names, GPT_names


def change_choices():
    SoVITS_names, GPT_names = get_weights_names()
    return {"choices": SoVITS_names, "__type__": "update"}, {
        "choices": GPT_names,
        "__type__": "update",
    }


# 推理用的指定模型
sovits_path = ""
gpt_path = ""
is_half_str = os.environ.get("is_half", "True")
is_half = True if is_half_str.lower() == "true" else False
is_share_str = os.environ.get("is_share", "False")
is_share = True if is_share_str.lower() == "true" else False

cnhubert_path = "GPT_SoVITS/pretrained_models/chinese-hubert-base"
bert_path = "GPT_SoVITS/pretrained_models/chinese-roberta-wwm-ext-large"
pretrained_sovits_path = "GPT_SoVITS/pretrained_models/s2G488k.pth"
pretrained_gpt_path = "GPT_SoVITS/pretrained_models/s1bert25hz-2kh-longer-epoch=68e-step=50232.ckpt"

exp_root = "logs"
python_exec = sys.executable or "python"

webui_port_main = 9874
webui_port_uvr5 = 9873
webui_port_infer_tts = 9872
webui_port_subfix = 9871

api_port = 9880


def get_device_dtype_sm(idx: int) -> tuple[torch.device, torch.dtype, float, float]:
    """
    返回 (device, dtype, fake_sm, mem_gb)
    依据 Intel GPU 的显存和 fp16 支持能力决定是否推荐半精度。
    """
    cpu = torch.device("cpu")
    if not torch.xpu.is_available():
        return cpu, torch.float32, 0.0, 0.0

    device_idx = idx
    try:
        props = torch.xpu.get_device_properties(device_idx)
    except Exception:
        return cpu, torch.float32, 0.0, 0.0

    mem_bytes = props.total_memory
    mem_gb = mem_bytes / (1024**3) + 0.4   # 保留原逻辑的 +0.4 GiB 补偿
    has_fp16 = getattr(props, 'has_fp16', False)

    # 显存不足 4 GiB 或不支持 fp16 → 回退 CPU
    if mem_gb < 4 or not has_fp16:
        return cpu, torch.float32, 0.0, 0.0

    # 推荐使用半精度，并给出一个虚拟的“计算能力”值 10.0（仅用于兼容旧判断）
    fake_sm = 10.0
    device = torch.device(f"xpu:{device_idx}")
    return device, torch.float16, fake_sm, mem_gb

IS_GPU = True
GPU_INFOS: list[str] = []
GPU_INDEX: set[int] = set()
GPU_COUNT = torch.xpu.device_count()
CPU_INFO: str = "0\tCPU " + i18n("CPU训练,较慢")
tmp: list[tuple[torch.device, torch.dtype, float, float]] = []
memset: set[float] = set()

for i in range(max(GPU_COUNT, 1)):
    tmp.append(get_device_dtype_sm(i))

for j in tmp:
    device = j[0]
    memset.add(j[3])
    if device.type != "cpu":
        GPU_INFOS.append(f"{device.index}\t{torch.xpu.get_device_name(device.index)}")
        GPU_INDEX.add(device.index)

if not GPU_INFOS:
    IS_GPU = False
    GPU_INFOS.append(CPU_INFO)
    GPU_INDEX.add(0)

infer_device = max(tmp, key=lambda x: (x[2], x[3]))[0]
is_half = any(dtype == torch.float16 for _, dtype, _, _ in tmp)


class Config:
    def __init__(self):
        self.sovits_path = sovits_path
        self.gpt_path = gpt_path
        self.is_half = is_half

        self.cnhubert_path = cnhubert_path
        self.bert_path = bert_path
        self.pretrained_sovits_path = pretrained_sovits_path
        self.pretrained_gpt_path = pretrained_gpt_path

        self.exp_root = exp_root
        self.python_exec = python_exec
        self.infer_device = infer_device

        self.webui_port_main = webui_port_main
        self.webui_port_uvr5 = webui_port_uvr5
        self.webui_port_infer_tts = webui_port_infer_tts
        self.webui_port_subfix = webui_port_subfix

        self.api_port = api_port
