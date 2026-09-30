from agno.models.groq import Groq
from agno.models.message import Message
from variables import GROQ_API_KEY

model = Groq(id="openai/gpt-oss-120b", api_key=GROQ_API_KEY)
assistant_message = Message(role="assistant")
msg = Message(
    role="user",
    content=[{"type": "text", "text": "Olá! Meu nome é Willon!"}]
)

response = model.invoke([msg], assistant_message)

print(response.content)
