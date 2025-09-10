# 🧠 Brain Tumor Classification Web App

![Brain Tumor Classification](data/glioma.jpeg)  

A **Python Flask web application** that classifies brain tumors from MRI images into categories like **Glioma**, **Meningioma**, and **Pituitary Tumor** using **PyTorch deep learning models**. This project is ideal for **medical imaging enthusiasts** and **AI/ML learners**.

---

## 🚀 Features

- Upload MRI images and classify tumors automatically.
- Provides detailed **tumor type description**.
- Easy-to-use **web interface** built with Flask, HTML, CSS.
- Lightweight and **fast predictions** using a pre-trained PyTorch model.
- Fully open-source and customizable.

---

## 🧰 Tech Stack

- **Backend:** Python, Flask  
- **Machine Learning:** PyTorch, Torchvision  
- **Frontend:** HTML, CSS, Bootstrap  
- **Other Libraries:** NumPy, Pillow, Werkzeug  

---

## 🖼️ Project Structure

classiification_tumor/
├── app.py                   # Main Flask application
├── tumor_classifier.pth     # Pre-trained PyTorch model
├── requirements.txt         # Python dependencies
├── templates/               # HTML templates
│   ├── index.html           # Home page
│   └── result.html          # Prediction result page
├── static/                  # Static assets
│   ├── style.css            # CSS styles
│   └── images/              # Icons, backgrounds, sample images
└── data/                    # Sample MRI images for testing



---


## ⚡ How to Run Locally

1. Clone the repository:

```bash
git clone https://github.com/pyprojectpi/tumor_classify.git
cd tumor_classify

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python app.py

