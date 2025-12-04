import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset
import numpy as np

# ==========================================
# 1. EEGNet Model
# ==========================================
class EEGNet(nn.Module):
	def __init__(self, nb_classes, Chans=64, Samples=128, input_channels=7,
                 dropoutRate=0.5, kernLength=64, F1=8, D=2, F2=16):
		super(EEGNet, self).__init__()

		# Layer 1: Temporal & Spatial Filtering
		self.block1 = nn.Sequential(
	        nn.Conv2d(input_channels, F1, (1, kernLength), padding=(0, kernLength // 2), bias=False),
	    nn.BatchNorm2d(F1),
	    nn.Conv2d(F1, F1 * D, (Chans, 1), groups=F1, bias=False),
	    nn.BatchNorm2d(F1 * D),
	    nn.ELU(),
	    nn.AvgPool2d((1, 4)),
	    nn.Dropout(dropoutRate)
	)

		# Layer 2: Mixing
		self.block2 = nn.Sequential(
	        nn.Conv2d(F1 * D, F1 * D, (1, 16), padding=(0, 16 // 2), groups=F1 * D, bias=False),
	    nn.Conv2d(F1 * D, F2, (1, 1), bias=False),
	    nn.BatchNorm2d(F2),
	    nn.ELU(),
	    nn.AvgPool2d((1, 8)),
	    nn.Dropout(dropoutRate)
	)

		# Auto-calculate classifier input size
		with torch.no_grad():
			dummy = torch.zeros(1, input_channels, Chans, Samples)
			out = self.block2(self.block1(dummy))
			self.flatten_size = out.view(1, -1).shape[1]

		self.classifier = nn.Linear(self.flatten_size, nb_classes)

	def forward(self, x):
		x = self.block1(x)
		x = self.block2(x)
		x = x.view(x.size(0), -1)
		return self.classifier(x)

# ==========================================
# 2. Main Training Logic
# ==========================================
def train():
	# --- Load Data (Super Fast Now) ---
	print("Loading data...")
	try:
		data = np.load("all_subjects_trf.npz")
		X = torch.from_numpy(data['X']) # Shape: (57, 7, 64, 128)
		y = torch.from_numpy(data['y']) # Shape: (57,)
		print(f"Data Loaded: {X.shape}")
	except FileNotFoundError:
		print("❌ File 'all_subjects_trf.npz' not found. Run the converter script first!")
		return

	# --- Setup ---
	device = torch.device("mps" if torch.backends.mps.is_available() else "cpu")
	print(f"Using Device: {device}")

	# Create Dataset (80/20 Split)
	dataset = TensorDataset(X, y)
	train_size = int(0.8 * len(dataset))
	test_size = len(dataset) - train_size
	train_set, test_set = torch.utils.data.random_split(dataset, [train_size, test_size])

	train_loader = DataLoader(train_set, batch_size=8, shuffle=True)
	test_loader = DataLoader(test_set, batch_size=8, shuffle=False)

	# --- Initialize Model ---
	# input_channels=7 (for your 7 TRF features)
	model = EEGNet(nb_classes=2, 
                   Chans=X.shape[2], 
                   Samples=X.shape[3], 
                   input_channels=7).to(device)

	optimizer = optim.Adam(model.parameters(), lr=0.001)
	criterion = nn.CrossEntropyLoss()

	# --- Train ---
	print("\nStarting Training...")
	for epoch in range(30):
		model.train()
		total_loss = 0
		correct = 0
		total = 0

		for inputs, labels in train_loader:
			inputs, labels = inputs.to(device), labels.to(device)

			optimizer.zero_grad()
			outputs = model(inputs)
			loss = criterion(outputs, labels)
			loss.backward()
			optimizer.step()

			total_loss += loss.item()
			_, predicted = torch.max(outputs.data, 1)
			correct += (predicted == labels).sum().item()
			total += labels.size(0)

		print(f"Epoch {epoch+1} | Loss: {total_loss/len(train_loader):.4f} | Acc: {100*correct/total:.1f}%")

	# --- Test ---
	print("\nEvaluating...")
	model.eval()
	correct = 0
	total = 0
	with torch.no_grad():
		for inputs, labels in test_loader:
			inputs, labels = inputs.to(device), labels.to(device)
			outputs = model(inputs)
			_, predicted = torch.max(outputs.data, 1)
			correct += (predicted == labels).sum().item()
			total += labels.size(0)

	print(f"Final Test Accuracy: {100*correct/total:.2f}%")

if __name__ == "__main__":
	train()