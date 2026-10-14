"""
UNCHAINED - LLM Configuration (DeepSeek via LangChain).
"""

import os
import json
import time
import logging
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

logger = logging.getLogger("unchained.llm")
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)

_api_key = "sk-2e8b55ee57bf4a9eb3b7166f589c51e3"


logger.info("DeepSeek API key configured: %s", "YES" if _api_key != "sk-placeholder" else "NO (using placeholder)")

llm = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=_api_key,
    temperature=0.3,
    max_tokens=4000,
)


def call_llm_json(system_prompt: str, user_prompt: str, caller: str = "unknown") -> dict:
    """Chiama il LLM e parsa la risposta come JSON."""
    logger.info("[%s] >>> Invio richiesta a DeepSeek (JSON mode)", caller)
    logger.info("[%s]     System prompt: %.100s...", caller, system_prompt.replace("\n", " "))
    logger.info("[%s]     User prompt length: %d chars", caller, len(user_prompt))

    start = time.time()
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = llm.invoke(messages)
        elapsed = time.time() - start

        content = response.content.strip()
        token_usage = getattr(response, "response_metadata", {}).get("token_usage", {})

        logger.info(
            "[%s] <<< Risposta ricevuta da DeepSeek in %.1fs | response length: %d chars | tokens: %s",
            caller, elapsed, len(content), token_usage or "N/A",
        )
        logger.debug("[%s]     Raw response: %.200s...", caller, content.replace("\n", " "))

        # Rimuovi eventuale markdown code fence
        if content.startswith("```"):
            lines = content.split("\n")
            lines = [l for l in lines if not l.strip().startswith("```")]
            content = "\n".join(lines)

        parsed = json.loads(content)
        logger.info("[%s] JSON parsed OK — top-level keys: %s", caller, list(parsed.keys()))
        return parsed

    except json.JSONDecodeError as e:
        elapsed = time.time() - start
        logger.error("[%s] ERRORE parsing JSON dopo %.1fs: %s", caller, elapsed, e)
        logger.error("[%s]     Content ricevuto: %.300s", caller, content)
        raise
    except Exception as e:
        elapsed = time.time() - start
        logger.error("[%s] ERRORE chiamata DeepSeek dopo %.1fs: %s: %s", caller, elapsed, type(e).__name__, e)
        raise


def call_llm_text(system_prompt: str, user_prompt: str, caller: str = "unknown") -> str:
    """Chiama il LLM e restituisce la risposta come testo."""
    logger.info("[%s] >>> Invio richiesta a DeepSeek (text mode)", caller)
    logger.info("[%s]     User prompt length: %d chars", caller, len(user_prompt))

    start = time.time()
    try:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt),
        ]
        response = llm.invoke(messages)
        elapsed = time.time() - start

        content = response.content.strip()
        token_usage = getattr(response, "response_metadata", {}).get("token_usage", {})

        logger.info(
            "[%s] <<< Risposta ricevuta da DeepSeek in %.1fs | response length: %d chars | tokens: %s",
            caller, elapsed, len(content), token_usage or "N/A",
        )
        return content

    except Exception as e:
        elapsed = time.time() - start
        logger.error("[%s] ERRORE chiamata DeepSeek dopo %.1fs: %s: %s", caller, elapsed, type(e).__name__, e)
        raise
