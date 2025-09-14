#!/Users/abinav/Documents/Projects/AI_Classifier/.venv/bin/python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from classifier_CNN import BinaryCNN
from Dataset import BinaryFontDataset

if __name__ == "__main__":
    # Initialize model
    model = BinaryCNN()

    device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
    model.to(device)


    # Load dataset
    train_dataset = BinaryFontDataset(
    emnist_image_file="Datasets/EMNIST/emnist-byclass-train-images-idx3-ubyte",
    font_ubyte_folder="Datasets/GoogleFonts/Train"
    )

    # Loss and optimizer
    criterion = nn.BCELoss()  # Binary Cross Entropy
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    num_epochs = 25
    model.train()

    # Create DataLoader
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    
    # Training loop
    for epoch in range(num_epochs):
        print(f"Running epoch {epoch+1}/{num_epochs}")
        running_loss = 0.0

        for images, labels in train_loader:
            images = images.to(device)
            labels = labels.to(device).unsqueeze(1)  # shape [batch,1]

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()

        avg_loss = running_loss / len(train_loader)
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {avg_loss:.4f}")
    
    
    model.eval()  # set model to evaluation mode
    all_labels = []
    all_preds = []

    test_dataset = BinaryFontDataset(
    emnist_image_file="Datasets/EMNIST/emnist-byclass-test-images-idx3-ubyte",
    font_ubyte_folder="Datasets/GoogleFonts/Test"
    )
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    with torch.no_grad():  # disable gradients for faster evaluation
        for images, labels in test_loader:
            images = images.to(device)
            labels = labels.to(device).unsqueeze(1)
            outputs = model(images)
            preds = (outputs >= 0.5).float()  # convert probabilities to 0 or 1
            all_labels.append(labels.cpu())
            all_preds.append(preds.cpu())

    all_labels = torch.cat(all_labels)
    all_preds = torch.cat(all_preds)

    accuracy = (all_preds == all_labels).float().mean()
    print(f"Test Accuracy: {accuracy:.4f}")
