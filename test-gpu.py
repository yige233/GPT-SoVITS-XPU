import torch

print("PyTorch version:", torch.__version__)
print("XPU available:", torch.xpu.is_available())
if torch.xpu.is_available():
    print("Device count:", torch.xpu.device_count())
    print("Current device:", torch.xpu.current_device())
    print("Device name[0]:", torch.xpu.get_device_name(0))
else:
    print("XPU not detected. Check driver or PyTorch xpu installation.")