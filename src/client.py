from pydantic import BaseModel
from typesafe_sdk import AsyncTypeSafeClient


class AsyncJev:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def ainvoke[ResponseT: BaseModel](
        self,
        state: BaseModel,
        questions: BaseModel,
        response_model: type[ResponseT],
    ) -> ResponseT:
        async with AsyncTypeSafeClient(api_key=self.api_key) as client:
            return await client.system_one(
                state=state.model_dump(mode="json", by_alias=True),
                questions=questions.model_dump(mode="json", by_alias=True),
                response_model=response_model,
            )
