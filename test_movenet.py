import torch
from lib.models.movenet_mobilenetv2 import MoveNet # Example path from community repos

# 1. Instantiate the model
model = MoveNet(num_classes=17, width_mult=1.0) # Parameters must match saved state

# 2. Load the state dictionary
# Use map_location='cpu' if you don't have a GPU
state_dict = torch.load('movenet.pth', map_location=torch.device('cpu'))
model.load_state_dict(state_dict)

# 3. Set to evaluation mode for inference
model.eval()

