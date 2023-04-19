import openai
import json


class OpenAI_API:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key

    def send_message(self, message, conversation_history):
        if len(conversation_history) > 50:
            conversation_history = self.summarize_conversation(
                conversation_history)
        prompt = f"{conversation_history}\nUser: {message}"
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                n=1,
                stop=None,
                temperature=0.5,
            )
            result = json.loads(str(response))[
                "choices"][0]["message"]["content"]
            return result
        except Exception as e:
            return None

    def summarize_conversation(self, conversation_history):
        try:
            response = openai.Completion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"Summarize our discussion briefly in 200 words or less to use as a prompt for future context:\n\n{conversation_history}"}
                ],
                max_tokens=200,
                n=1,
                stop=None,
                temperature=0.5,
            )
            result = json.loads(str(response))[
                "choices"][0]["message"]["content"]

            return result.strip()
        except Exception as e:
            return None
