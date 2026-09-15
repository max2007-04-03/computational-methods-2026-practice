from openai import OpenAI
from utils.lab_logger import custom_logger

logger = custom_logger('lab1', overwrite=True)

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

SYSTEM = "Відповідай лише українською, максимум двома реченнями."
USER = "Поясни різницю між функцією і методом."

response = client.chat.completions.create(
    model="qwen3:4b",
    messages=[
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": USER},
    ],
    temperature=0.7,
)

content = response.choices[0].message.content
logger.info(content)
logger.info(response.usage)
