from openai import OpenAI
from openai.constants import OPEN_AI_KEY

class OpenAIServices:

    def __init__(self) -> None:
        self.__client = OpenAI()
        self.__open_ai_key = OPEN_AI_KEY


    


    