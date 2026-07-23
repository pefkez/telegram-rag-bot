from pydantic import BaseModel


class QuestionRequest(BaseModel):
    user_id: int
    text: str


class AnswerResponse(BaseModel):
    answer: str
    sources: list[str]
