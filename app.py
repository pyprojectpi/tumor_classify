from flask import Flask, render_template, request
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
import os

app = Flask(__name__)

# =====================
# Define CNN Model
# =====================
class TumorClassifier(nn.Module):
    def __init__(self):
        super(TumorClassifier, self).__init__()
        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, stride=1, padding=1)
        self.conv3 = nn.Conv2d(64, 128, kernel_size=3, stride=1, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(128 * 16 * 16, 256)  # for input 128x128 image
        self.fc2 = nn.Linear(256, 5)

        self.relu = nn.ReLU()

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = self.pool(self.relu(self.conv3(x)))
        x = torch.flatten(x, 1)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x

# =====================
# Load Model
# =====================
model = TumorClassifier()
model_path = "tumor_classifier.pth"

if os.path.exists(model_path):
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
else:
    raise FileNotFoundError("Model file not found! Train and save the model first.")

# =====================
# Transform
# =====================
transform = transforms.Compose([
    transforms.Resize((128, 128)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# =====================
# Labels + Descriptions
# =====================
class_labels = ['Unlabeled', 'Glioma Tumor', 'Meningioma Tumor', 'No Tumor', 'Pituitary Tumor']

descriptions = {
    "Glioma Tumor": "Gliomas are tumors that develop in the brain or spinal cord. They may lead to persistent headaches, nausea, seizures and problems with memory or movement depending on their location.",
    "Meningioma Tumor": "Meningiomas arise from the protective membranes around the brain and spinal cord. They are often benign but can press on nearby brain tissue causing headaches, vision changes or difficulty concentrating.",
    "No Tumor": "This scan shows no signs of a tumor. The brain appears normal and healthy, although regular medical checkups are recommended to ensure ongoing well-being.",
    "Pituitary Tumor": "Pituitary tumors form at the base of the brain in the small gland that controls hormones. They can affect growth, vision, mood and metabolism depending on their size and activity.",
    "Unlabeled": "This MRI scan does not match any of the recognized tumor categories and further medical evaluation may be required for clarification."
}

# =====================
# Classification Function
# =====================
def classify_image(image_path):
    image = Image.open(image_path).convert("RGB")
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        output = model(image)
        predicted_class = torch.argmax(output, dim=1).item()

    return class_labels[predicted_class]

# =====================
# Flask Routes
# =====================
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded", 400
        file = request.files["file"]
        if file.filename == "":
            return "Empty filename", 400
        path = os.path.join("static", file.filename)
        file.save(path)
        label = classify_image(path)
        description = descriptions[label]
        return render_template("result.html", label=label, description=description, image_path=path)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
