from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openai import AsyncOpenAI

from app.api.deps import ChatRequest, ChatResponse
from app.core.config import settings

router = APIRouter(prefix="/api/v1", tags=["chat"])


@router.post(settings.CHAT_PATH)
async def chat(request: ChatRequest):
    client = AsyncOpenAI(
        api_key=request.api_key,
        base_url=settings.ENDPOINT,
    )
    messages = request.to_openai_messages()
    completion_kwargs = {
        "model": request.model,
        "messages": messages,
        "temperature": request.temperature,
        "max_tokens": request.max_tokens,
        "top_p": request.top_p,
    }

    if request.stream:
        async def generate():
            stream = await client.chat.completions.create(
                **completion_kwargs,
                stream=True,
            )
            async for chunk in stream:
                yield f"data: {chunk.model_dump_json()}\n\n"
            yield "data: [DONE]\n\n"

        return StreamingResponse(generate(), media_type="text/event-stream")

    response = await client.chat.completions.create(
        **completion_kwargs,
        stream=False,
    )
    return ChatResponse.from_completion(response)
