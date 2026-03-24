from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.tavily import TavilyTools

from dotenv import load_dotenv

load_dotenv()


def celsius_to_fahrenheit(celsius_temperature: float):
    """
    Convert the temperature from Celsius to Fahrenheit

    Args:
        celsius_temperature (float): The temperature in Celsius

    Returns:
        float: The temperature in Fahrenheit

    Example:
        celsius_to_fahrenheit(0) -> 32.0
        celsius_to_fahrenheit(100) -> 212.0
    """
    return (celsius_temperature * 9/5) + 32


agent = Agent(
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[TavilyTools(),
    celsius_to_fahrenheit],
    debug_mode=True
)

if __name__ == "__main__":
    agent.print_response("Use suas ferramentas para pesquisar a temperatura, em Fahrenheit e em Celsius, de hoje em Manaus")
