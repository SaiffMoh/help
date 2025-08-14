from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os

load_dotenv()
_llm_json = None
_llm_text = None

def get_llm() -> ChatOpenAI:
<<<<<<< Current (Your changes)
	global _llm
	if _llm is None:
		api_key = os.getenv("OPENAI_API_KEY")
		if not api_key:
			raise RuntimeError("LLM unavailable: OPENAI_API_KEY not set")
		_llm = ChatOpenAI(
			model="gpt-4o-mini",
			temperature=0.1,
			api_key=api_key,
			response_format={"type": "json_object"}
		)
	return _llm
=======
    """Backward-compatible: returns the JSON-mode LLM used for structured extraction."""
    return get_llm_json()


def get_llm_json() -> ChatOpenAI:
    global _llm_json
    if _llm_json is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("LLM unavailable: OPENAI_API_KEY not set")
        _llm_json = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            api_key=api_key,
            response_format={"type": "json_object"}
        )
    return _llm_json


def get_text_llm() -> ChatOpenAI:
    global _llm_text
    if _llm_text is None:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("LLM unavailable: OPENAI_API_KEY not set")
        _llm_text = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=api_key
        )
    return _llm_text
>>>>>>> Incoming (Background Agent changes)
