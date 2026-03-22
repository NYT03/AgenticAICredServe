import os
import fitz
import json
import io
from PIL import Image
from google import genai
from dotenv import load_dotenv
from .verifier import verify_transactions

# Load environment variables
load_dotenv()

# Configure Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Warning: GEMINI_API_KEY for Gemini is not set.")
client = genai.Client(api_key=api_key)

def pdf_to_images(pdf_path):
    """Convert PDF pages to PIL images."""
    doc = fitz.open(pdf_path)
    images = []
    for page in doc:
        pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))  # Increase resolution for better clarity
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))
        images.append(img)
    return images

def llm_extract_vision(images):
    """Extract data from images using Gemini's vision capability."""
    prompt = """
    CRITICAL INSTRUCTIONS:
    1. Analyze the provided bank statement image(s) very carefully.
    2. These images may be low-quality, blurred, skewed, or noisy scans. Use your visual understanding to correctly identify characters.
    3. The data is unstructured. Look for headers like 'Date', 'Description', 'Withdrawal', 'Deposit', 'Balance' to identify the table.
    4. Extract the following details: 
       - account_holder_name
       - bank_name
       - account_number
       - transactions: (date, description, debit, credit, balance)
    5. For dates, standardize them to "YYYY-MM-DD" if possible; if the year is missing, assume it's the current year.
    6. Ensure that 'debit' and 'credit' are numbers (not strings with commas). 
    7. Provide ONLY a raw JSON object as the response. DO NOT include any markdown, triple backticks, or explanation.
    
    JSON Schema:
    {
      "account_holder_name": "string",
      "bank_name": "string",
      "account_number": "string",
      "transactions": [
        {
          "date": "string",
          "description": "string",
          "debit": number,
          "credit": number,
          "balance": number
        }
      ]
    }
    """

    # Prepare contents: all images + prompt
    contents = images + [prompt]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents
    )
    
    content = response.text.strip()
    
    # Cleaning markdown blocks if necessary
    if content.startswith("```json"):
        content = content[7:-3].strip()
    elif content.startswith("```"):
        content = content[3:-3].strip()
        
    return content

def process_document(pdf_path):
    # Convert PDF to images for vision processing
    try:
        images = pdf_to_images(pdf_path)
    except Exception as e:
        print(f"Error converting PDF to images: {e}")
        return {"error": "Failed to process PDF file"}

    for i in range(2):
        try:
            result = llm_extract_vision(images)
            data = json.loads(result)

            if verify_transactions(data):
                return data
            else:
                print(f"Verification failed on attempt {i+1}, retrying...")
        except Exception as e:
            print(f"Error during extraction attempt {i+1}: {e}")

    return {"error": "Verification failed or invalid response from AI"}