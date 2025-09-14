#!/usr/bin/env python3
import numpy as np
import torch
from torch.utils.data import Dataset
import os

class BinaryFontDataset(Dataset):
    def __init__(self, emnist_image_file, font_ubyte_folder, transform=None):
        """
        emnist_image_file: path to EMNIST ubyte image file (handwritten)
        font_ubyte_folder: folder containing font .ubyte files
        transform: optional torchvision transforms
        """
        self.transform = transform

        # Load EMNIST handwritten images
        with open(emnist_image_file, 'rb') as f:
            f.read(16)  # skip header
            emnist_data = np.frombuffer(f.read(), dtype=np.uint8)
            self.emnist_images = emnist_data.reshape(-1, 28, 28)
        self.emnist_labels = np.ones(len(self.emnist_images), dtype=np.uint8)  # handwritten = 1

        # Load all Google Fonts ubytes
        font_images_list = []
        for file in os.listdir(font_ubyte_folder):
            if file.endswith('-images-idx3-ubyte'):
                path = os.path.join(font_ubyte_folder, file)
                with open(path, 'rb') as f:
                    f.read(16)  # skip header
                    data = np.frombuffer(f.read(), dtype=np.uint8)
                    font_images_list.append(data.reshape(-1, 28, 28))
        if font_images_list:
            self.font_images = np.vstack(font_images_list)
            self.font_labels = np.zeros(len(self.font_images), dtype=np.uint8)  # font = 0
        else:
            self.font_images = np.empty((0,28,28))
            self.font_labels = np.empty((0,), dtype=np.uint8)

        # Combine handwritten + font
        self.images = np.vstack([self.emnist_images, self.font_images])
        self.labels = np.concatenate([self.emnist_labels, self.font_labels])

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, index):
        img = self.images[index]
        label = self.labels[index]

        if self.transform:
            img = self.transform(img)

        # Convert to PyTorch tensor and normalize 0-1
        img = torch.tensor(img, dtype=torch.float32).unsqueeze(0) / 255.0
        label = torch.tensor(label, dtype=torch.float32)

        return img, label
