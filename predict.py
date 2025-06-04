"""
Prediction Module for Phishing Email Detection
Handles loading the AI model and making predictions
"""

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import time

class PhishingPredictor:
    """
    Class for predicting whether an email is phishing using a pre-trained model
    For demonstration, we use a sentiment model where negative sentiment maps to phishing
    """
    
    def __init__(self):
        """Initialize the predictor with model and tokenizer"""
        # Using sentiment analysis model as a stand-in for phishing detection
        # In a real implementation, use a properly fine-tuned model for phishing
        self.model_name = "distilbert-base-uncased-finetuned-sst-2-english"
        
        # Initialize as None, load on first prediction to avoid startup delay
        self.model = None
        self.tokenizer = None
    
    def load_model(self):
        """Load the model and tokenizer if not already loaded"""
        if self.model is None or self.tokenizer is None:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
                return True
            except Exception as e:
                # Fallback to dummy model if loading fails
                print(f"Error loading model: {e}")
                print("Using dummy prediction instead")
                self.model = None
                self.tokenizer = None
                return False
        return True
    
    def predict(self, email_content):
        """
        Predict if an email is phishing based on its content
        
        Args:
            email_content (str): The email content to analyze
            
        Returns:
            tuple: (is_phishing, confidence_percentage)
        """
        # For demo purposes, simulate loading delay
        time.sleep(1)
        
        # Try to load the model
        model_loaded = self.load_model()
        
        if not model_loaded:
            # Use dummy prediction for demonstration if model fails to load
            return self._dummy_predict(email_content)
        
        # Prepare the email content
        processed_text = email_content.lower()
        
        # Tokenize the text
        inputs = self.tokenizer(
            processed_text,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding="max_length"
        )
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(**inputs)
            predictions = outputs.logits
            
            # Apply softmax to get probabilities
            probs = torch.nn.functional.softmax(predictions, dim=1)[0]
            
            # For this sentiment model:
            # Index 0 = negative sentiment (mapped to phishing)
            # Index 1 = positive sentiment (mapped to safe)
            phishing_prob = probs[0].item()
            
            # Convert to percentage and determine if phishing
            confidence = phishing_prob * 100
            is_phishing = confidence > 50
            
            # If not phishing, use the safe probability for confidence
            if not is_phishing:
                confidence = probs[1].item() * 100
            
            # Adjust confidence for demo purposes
            if is_phishing:
                # Scale confidence to make it more realistic
                confidence = min(confidence * 1.2, 99.9)
            else:
                # For safe emails, sometimes reduce confidence
                if confidence > 90:
                    confidence *= 0.9
            
            return is_phishing, confidence
    
    def _dummy_predict(self, email_content):
        """
        Fallback prediction method when model loading fails
        Uses simple heuristics for demonstration purposes
        
        Args:
            email_content (str): The email content to analyze
            
        Returns:
            tuple: (is_phishing, confidence_percentage)
        """
        text = email_content.lower()
        
        # Simple keyword-based heuristics
        phishing_keywords = [
            "urgent", "verify", "account", "suspend", "bank", "click", "link",
            "password", "update", "confirm", "security", "unusual activity",
            "won", "prize", "million", "lottery", "prince", "inheritance"
        ]
        
        # Count occurrences of phishing keywords
        keyword_count = sum(1 for keyword in phishing_keywords if keyword in text)
        
        # Calculate a simple score
        score = min(keyword_count * 10, 100)
        
        # Determine if it's phishing based on score
        is_phishing = score > 40
        
        # Add some randomness to make it more realistic
        import random
        confidence = score + random.uniform(-10, 10)
        confidence = max(min(confidence, 99.9), 20.0)  # Keep between 20% and 99.9%
        
        return is_phishing, confidence