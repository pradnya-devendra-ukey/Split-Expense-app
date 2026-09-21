import json
from google import genai
from google.genai import types
from app.config import settings

def parse_receipt_with_gemini(image_bytes: bytes, mime_type: str = "image/jpeg") -> dict:
    """Uses Gemini Vision API to extract store name, total, and line items as JSON."""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    prompt = """
    Analyze this receipt image carefully. Extract:
    1. Store name
    2. Total amount paid
    3. Every individual line item with its item name and price as a float.

    Return ONLY a valid JSON object matching this structure:
    {
      "store_name": "Store Name",
      "total_amount": 45.50,
      "items": [
        {"item_name": "Milk 1L", "price": 3.50},
        {"item_name": "Organic Eggs", "price": 5.20}
      ]
    }
    Do not include markdown code block formatting or extra text.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            prompt
        ],
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)