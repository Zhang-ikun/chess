import torch
print(torch.cuda.is_available())
torch.cuda.current_device()
torch.cuda._initialized = True