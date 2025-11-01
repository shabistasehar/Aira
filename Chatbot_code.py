from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception

# Retry logic
def is_503_error(exception):
    return isinstance(exception, genai.errors.ClientError) and getattr(exception, 'status_code', None) == 503

@retry(
    retry=retry_if_exception(is_503_error),
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    reraise=True
)
def send_message_with_retry(chat_session, prompt):
    return chat_session.send_message(prompt)

# Initialize client and session
client = genai.Client(api_key="AIzaSyBFd3gZKd8SB_GhzBa8hfL5pqeqe-nnk1s")
model_name = "gemini-2.5-flash"

system_instruction = (
    "You are AIra, an empathetic chatbot. Respond with care. "
    "If crisis is detected, gently suggest contacting help. Keep responses concise."
)

chat = client.chats.create(
    model=model_name,
    config=types.GenerateContentConfig(system_instruction=system_instruction)
)

# Function called from server.py
def get_bot_response(user_input: str) -> str:
    try:
        response = send_message_with_retry(chat, user_input)
        return response.text
    except genai.errors.ClientError as e:
        if getattr(e, 'status_code', None) == 503:
            return "Sorry, the model is overloaded. Please try again shortly."
        return f"Error: {getattr(e, 'message', '')}"
    except Exception as e:
        return f"Unexpected error: {e}"
