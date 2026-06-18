from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant", "tool"]
    content: str = Field(..., min_length=1)
    name: str | None = None


class ChatRequest(BaseModel):
    model: str = Field(..., min_length=1, description="模型名称")
    api_key: str = Field(..., min_length=1, description="API 密钥")
    messages: list[ChatMessage] = Field(..., min_length=1, description="对话消息列表")
    stream: bool = False
    temperature: float = Field(default=0.7, ge=0, le=2)
    max_tokens: int = Field(default=4096, ge=1)
    top_p: float = Field(default=1.0, ge=0, le=1)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "model": "doubao-1-5-pro-32k-250115",
                "api_key": "your-api-key",
                "messages": [
                    {"role": "user", "content": "你好你是谁"},
                ],
                "stream": False,
                "temperature": 0.7,
                "max_tokens": 4096,
                "top_p": 1,
            }
        }
    )

    @field_validator("api_key", mode="before")
    @classmethod
    def strip_api_key(cls, value: str) -> str:
        if not isinstance(value, str):
            return value
        return value.strip()

    def to_openai_messages(self) -> list[dict[str, Any]]:
        return [message.model_dump(exclude_none=True) for message in self.messages]


class ResponseMessage(BaseModel):
    role: Literal["assistant", "system", "user", "tool"]
    content: str | None = None
    refusal: str | None = None
    annotations: Any | None = None
    audio: Any | None = None
    function_call: Any | None = None
    tool_calls: list[Any] | None = None


class Choice(BaseModel):
    index: int
    finish_reason: Literal[
        "stop", "length", "tool_calls", "content_filter", "function_call"
    ] | str | None = None
    logprobs: Any | None = None
    message: ResponseMessage


class CompletionTokensDetails(BaseModel):
    accepted_prediction_tokens: int | None = None
    audio_tokens: int | None = None
    reasoning_tokens: int | None = None
    rejected_prediction_tokens: int | None = None


class PromptTokensDetails(BaseModel):
    audio_tokens: int | None = None
    cached_tokens: int | None = None


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    completion_tokens_details: CompletionTokensDetails | None = None
    prompt_tokens_details: PromptTokensDetails | None = None


class ChatResponse(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Usage | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "0217817737953206a92a7a560d2de26f44703930971dcb57b2868",
                "object": "chat.completion",
                "created": 1781773797,
                "model": "doubao-1-5-pro-32k-250115",
                "choices": [
                    {
                        "finish_reason": "stop",
                        "index": 0,
                        "logprobs": None,
                        "message": {
                            "content": "我是豆包，是字节跳动研发的人工智能。",
                            "refusal": None,
                            "role": "assistant",
                            "annotations": None,
                            "audio": None,
                            "function_call": None,
                            "tool_calls": None,
                        },
                    }
                ],
                "usage": {
                    "completion_tokens": 36,
                    "prompt_tokens": 12,
                    "total_tokens": 48,
                    "completion_tokens_details": {
                        "accepted_prediction_tokens": None,
                        "audio_tokens": None,
                        "reasoning_tokens": 0,
                        "rejected_prediction_tokens": None,
                    },
                    "prompt_tokens_details": {
                        "audio_tokens": None,
                        "cached_tokens": 0,
                    },
                },
            }
        }
    )

    @classmethod
    def from_completion(cls, response: Any) -> "ChatResponse":
        return cls.model_validate(response.model_dump())
