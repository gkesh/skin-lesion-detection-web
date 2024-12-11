import os
import torch
import numpy as np

from torchvision import models, transforms
from torch.nn import functional as F
from PIL import Image


class DenseNetClassifier:    
    def __init__(self, img_size = 224):
        """
        Initializing the Image Proprocessor
        
        It transforms the image so that it can be used by 
        the model for classification
        """
        self.preprocessor = transforms.Compose([
            transforms.Resize((img_size, img_size)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[
                    np.float32(0.7630331), 
                    np.float32(0.5456457), 
                    np.float32(0.5700467)
                ], std=[
                    np.float32(0.1409281), 
                    np.float32(0.15261227), 
                    np.float32(0.16997086)
                ])
        ])
        self.device = torch.device('cuda:0')
        self.labels = [
            'Melanocytic Nevi', 
            'Melanoma',
            'Benign Keratosis-like Lesions',
            'Basal Cell Carcinoma',
            'Actinic Keratoses',
            'Vascular Lesions',
            'Dermatofibroma'
        ]
        
        model_path = f"{os.getcwd()}/models/densenet_ham10000.pth"
        model = models.densenet121(pretrained=False)
        model.classifier = torch.nn.Linear(model.classifier.in_features, len(self.labels))
        model.load_state_dict(torch.load(model_path, map_location=self.device))
        model.to(self.device)
        model.eval()
        
        self.model = model
        self.input_tensor = None
    
    
    def preprocess(self, img_path):
        """
        Using the defined preprocessor to
        tranform the image into tensor
        """
        image = Image.open(img_path).convert("RGB")
        self.input_tensor = self.preprocessor(image).unsqueeze(0).to(self.device)
        return self
    
    def classify(self):
        """
        Takes input tensor and uses it to
        predict classes using the model
        """
        if (self.input_tensor is None):
            raise ValueError("Image is not preprocessed before classification!")
        with torch.no_grad():
            outputs = self.model(self.input_tensor)
            # predicted_class = output.argmax(dim=1).item()
            probabilities = F.softmax(outputs, dim=1)
            confidence, predicted_class = torch.max(probabilities, dim=1)
            
            return self.labels[predicted_class], confidence
