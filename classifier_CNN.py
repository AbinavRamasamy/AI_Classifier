#!/usr/bin/env python3
import torch
import torch.nn as nn
import torch.nn.functional as F

class BinaryCNN(nn.Module):
    def __init__(self):
        super(BinaryCNN, self).__init__()
        # First conv layer: 1 input channel (grayscale), 32 output channels, 3x3 kernel
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)  # 2x2 max pooling
        # Second conv layer: 32 input channels, 64 output channels
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        # Fully connected layers
        self.fc1 = nn.Linear(64 * 7 * 7, 128)  # 28x28 -> 14x14 after pool -> 7x7 after second pool
        self.fc2 = nn.Linear(128, 1)  # Single output for binary classification

    def forward(self, x):
        x = F.relu(self.conv1(x))
        x = self.pool(x)  
        x = F.relu(self.conv2(x))
        x = self.pool(x)
        x = x.view(-1, 64 * 7 * 7)  # flatten
        x = F.relu(self.fc1(x))
        x = self.fc2(x)
        return torch.sigmoid(x) # output probability
