from config import get_gemini_client, GEMINI_MODEL_NAME

print("Model:", GEMINI_MODEL_NAME)

try:
    genai = get_gemini_client()

    model = genai.GenerativeModel(GEMINI_MODEL_NAME)

    response = model.generate_content(
        "Say hello in one short sentence."
    )

    print("\nSUCCESS!")
    print(response.text)

except Exception as e:
    print("\nERROR:")
    print(type(e).__name__)
    print(str(e))