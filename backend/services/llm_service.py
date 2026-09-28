"""
LLM Service using Groq Cloud API.
Ultra-fast LPU inference, NO local GPU needed. Covers AISC Exp 9 (GenAI) and Exp 10 (small LMs).
"""
from groq import AsyncGroq
from config import settings


class LLMService:
    def __init__(self):
        self.client = AsyncGroq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate(self, prompt: str, max_tokens: int = 1024) -> str:
        """Generate complete response from Groq LLM with multi-model failover."""
        fallback_models = [self.model, "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
        last_error = None

        for model_candidate in fallback_models:
            try:
                response = await self.client.chat.completions.create(
                    model=model_candidate,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=max_tokens,
                    temperature=0.3,
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                last_error = e
                continue

        return f"Error generating response: {str(last_error)}"

    async def stream_generate(self, prompt: str):
        """Stream response token by token for WebSocket with multi-model failover."""
        fallback_models = [self.model, "openai/gpt-oss-120b", "openai/gpt-oss-20b"]
        last_error = None

        for model_candidate in fallback_models:
            try:
                stream = await self.client.chat.completions.create(
                    model=model_candidate,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=1024,
                    temperature=0.3,
                    stream=True,
                )
                async for chunk in stream:
                    content = chunk.choices[0].delta.content
                    if content:
                        yield content
                return
            except Exception as e:
                last_error = e
                continue

        yield f"Error: {str(last_error)}"
