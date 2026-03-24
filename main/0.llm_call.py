from agno.models.groq import Groq
from agno.models.message import Message
from dotenv import load_dotenv

load_dotenv()

model = Groq(id="openai/gpt-oss-120b")
assistant_message = Message(role="assistant")
msg = Message(
    role="user",
    content=[{"type": "text", "text": "Olá! Meu nome é Willon!"}]
)

response = model.invoke([msg], assistant_message)

print(response.content)
