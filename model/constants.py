ENDPOINT = '' # Add form recognizer end point
FORM_RECOGNIZER_API_KEY = '' # Add form recognizer API Key
GEMINI_API_KEY = '' # Add Gemini API Key
GPT_API_KEY =  '' # Add GPT API Key
MODEL = "gpt-4o"
conversion_chart = {
    ("USD", "EUR"): 0.92,
    ("EUR", "USD"): 1.09,
    ("USD", "INR"): 83.0,
    ("INR", "USD"): 0.012,
    ("EUR", "INR"): 90.5,
    ("INR", "EUR"): 0.011,
    ("GBP", "USD"): 1.27,
    ("USD", "GBP"): 0.79,
    ("GBP", "INR"): 106.5,
    ("INR", "GBP"): 0.0094,
    ("USD", "AUD"): 1.52,
    ("AUD", "USD"): 0.66,
    ("EUR", "AUD"): 1.65,
    ("AUD", "EUR"): 0.61,
    ("INR", "AUD"): 0.018,
    ("AUD", "INR"): 56.0,
    ("GBP", "AUD"): 1.93,
    ("AUD", "GBP"): 0.52,
    ("GBP", "EUR"): 1.17,  
    ("EUR", "GBP"): 0.85,  
    ("AUD", "INR"): 56.0,
    ("INR", "AUD"): 0.018,
    ("AUD", "GBP"): 0.52,
    ("GBP", "AUD"): 1.93
}