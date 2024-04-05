import logging
import os


DEFAULT_LLMS = {
    #"name": (LOADER, {"args": "here"}, "Privacy (public/private)", "Description...", "vision/chat/qa"),
    "openai_gpt3.5_turbo": ("OpenAI", {"temperature": 0, "model": "gpt-3.5-turbo"}, "public", "OpenAI GPT-3.5 Turbo", "chat"),
    "openai_gpt4": ("OpenAI", {"temperature": 0, "model": "gpt-4"}, "public", "OpenAI GPT-4 ", "chat"),
    "openai_gpt4_turbo": ("OpenAI", {"temperature": 0, "model": "gpt-4-turbo-preview"}, "public", "OpenAI GPT-4 Turbo", "chat"),
    "mistral_7b": ("Ollama", {"model": "mistral", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/mistral", "qa"),
    "llama2_13b": ("Ollama", {"model": "llama2:13b-chat", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/llama2", "chat"),
    "llama2_7b": ("Ollama", {"model": "llama2:7b-chat", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/llama2", "chat"),
    "llava16_13b": ("OllamaMultiModal2", {"model": "llava:13b-v1.6", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/llava", "vision"),
    "bakllava_7b": ("OllamaMultiModal2", {"model": "bakllava", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/bakllava", "vision"),
    "mixtral_8x7b": ("Ollama", {"model": "mixtral", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/mixtral", "chat"),
    "llama2_70b": ("Ollama", {"model": "llama2:70b-chat", "temperature": 0.0001, "keep_alive": 0}, "private", "https://ollama.com/library/llama2", "chat"),
}


def getLLMClass(llm_classname):
    if llm_classname == "Ollama":
        from app.llms.ollama import Ollama
        return Ollama
    elif llm_classname == "OllamaMultiModal2":
        from app.llms.ollamamultimodal import OllamaMultiModal2
        return OllamaMultiModal2
    elif llm_classname == "OpenAI":
        from llama_index.llms.openai import OpenAI
        return OpenAI
    elif llm_classname == "Groq":
        from llama_index.llms.groq import Groq
        return Groq
    elif llm_classname == "Anthropic":
        from llama_index.llms.anthropic import Anthropic
        return Anthropic
    elif llm_classname == "LiteLLM":
        from llama_index.llms.litellm import LiteLLM
        return LiteLLM
    else:
        raise Exception("Invalid LLM class name.")


def loadEnvVars():
    if "EMBEDDINGS_PATH" not in os.environ:
        os.environ["EMBEDDINGS_PATH"] = "./embeddings/"

    if "ANONYMIZED_TELEMETRY" not in os.environ:
        os.environ["ANONYMIZED_TELEMETRY"] = "False"

    if "LOG_LEVEL" not in os.environ:
        os.environ["LOG_LEVEL"] = "INFO"

    os.environ["ALLOW_RESET"] = "true"


def get_logger(name, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler("./logs/" + name + ".log")
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger
