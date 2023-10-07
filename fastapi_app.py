from fastapi import FastAPI
from datetime import date
from pydantic import BaseModel
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import torchvision.transforms as transforms
import uvicorn

# Create a FastAPI app
app = FastAPI()

# Define a Pydantic model to receive the date from the Streamlit app
class DateInput(BaseModel):
    date: str

# Define your PyTorch model
class LinearRegression(nn.Module):
    def __init__(self):
        super(LinearRegression, self).__init__()
        self.linear = nn.Linear(1, 1)

    def forward(self, x):
        return self.linear(x)

# Load the PyTorch model from the saved checkpoint
# model = LinearRegression()
model = torch.jit.load('linear_regression_model.pt')

# Assuming you have a preprocessing function for input data
def preprocess_input(days_since_2022):
    """
    Preprocesses input data for the PyTorch model.

    Args:
        days_since_2022 (float): Number of days since January 1, 2022.

    Returns:
        torch.Tensor: Preprocessed input tensor.
    """
    # Replace this with your actual preprocessing logic
    return torch.tensor([[days_since_2022/365, 1.00]], dtype=torch.double)

@app.post("/predict")
async def predict(input_date: DateInput):
    """
    Endpoint for making predictions using the PyTorch model.

    Args:
        input_date (DateInput): Input date in ISO format.

    Returns:
        dict: Predicted value as a dictionary.
    """
    # Print input_date for debugging purposes
    print(input_date)
    
    # Convert the input date string to a date object
    input_date = date.fromisoformat(input_date.date)
    
    # Print the converted date for debugging purposes
    print(input_date)
    
    # Calculate the number of days since January 1, 2022
    start_date = date(2022, 1, 1)
    days_since_2022 = (input_date - start_date).days

    # Preprocess the input for the model
    input_tensor = preprocess_input(days_since_2022)

    # Make a prediction using the PyTorch model
    with torch.no_grad():
        prediction = model(input_tensor)

    return {"predicted_value": prediction.item()}

if __name__ == "__main__":
    # Run the FastAPI app with UVicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
