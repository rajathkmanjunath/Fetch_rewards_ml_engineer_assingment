# Use an appropriate base image (e.g., Python 3.8)
FROM python:3.8

# Set the working directory
WORKDIR /app

# Install required packages
RUN pip install streamlit fastapi uvicorn torch torchvision pydantic

# Copy the Streamlit and FastAPI application code into the container
COPY streamlit_app.py /app/
COPY fastapi_app.py /app/
COPY linear_regression_model.pt /app/
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Expose the ports used by Streamlit and FastAPI
EXPOSE 8501
EXPOSE 8080

# Start both Streamlit and FastAPI apps concurrently
CMD ["sh", "-c", "streamlit run streamlit_app.py & python  fastapi_app.py"]

