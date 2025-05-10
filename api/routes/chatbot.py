import os
import json
from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from app.chat import tools
import openai
from openai import OpenAIError, RateLimitError
from app.logger import log_interaction

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment variables.")
openai.api_key = api_key
client = openai.OpenAI()

router = APIRouter()

class ChatRequest(BaseModel):
    user_input: str
    user_id: str | None = None
    history: list = []

# Define tool metadata
tool_definitions = [
    {
        "type": "function",
        "function": {
            "name": "get_invoices",
            "description": "Fetch open or filtered invoices from the finance system",
            "parameters": {
                "type": "object",
                "properties": {
                    "subsidiary": {"type": "string"},
                    "customer": {"type": "string"},
                    "status": {"type": "string"},
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_ar_balance",
            "description": "Get AR totals grouped by subsidiary or customer",
            "parameters": {
                "type": "object",
                "properties": {
                    "group_by": {
                        "type": "string",
                        "enum": ["subsidiary", "customer"]
                    },
                    "status": {"type": "string"}
                },
                "required": []
            }
        }
    }
]

@router.post("/chat")
def chat_with_gpt(request: ChatRequest):
    history = request.history
    user_input = request.user_input

    try:
        today_str = date.today().strftime("%B %d, %Y")
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful financial assistant for a company controller. "
                        "Answer clearly and concisely. Only return data that matches user filters, like 'Open'. "
                        "Use bullet points or lists for readability. "
                        "Do not speculate or fabricate data. Only use what is returned by the API. "
                        "Always try to be helpful and offer reporting suggestions based on data you have available. "
                        "When applicable, interpret the user's intent and provide a detailed response. "
                        "When applicable, interpret the data and provide a summary of the results."
                    )
                }
            ] + history + [{"role": "user", "content": user_input}],
            tools=tool_definitions,
            tool_choice="auto"
        )

        message = response.choices[0].message
        history.append({"role": "user", "content": user_input})
        history.append(message)

        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                arguments = json.loads(tool_call.function.arguments)

                if tool_name == "get_invoices":
                    result = tools.get_invoices(**arguments)
                elif tool_name == "get_ar_balance":
                    result = tools.get_ar_balance(**arguments)
                else:
                    result = {"error": f"No handler implemented for tool {tool_name}"}

                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

                follow_up = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=history
                )
                reply = follow_up.choices[0].message.content
                # audit-log this run
                log_interaction(
                    user_id=request.user_id or "anonymous",
                    query=user_input,
                    tool=tool_name,
                    args=arguments,
                    result=result,
                    reply=reply,
                )
                history.append({"role": "assistant", "content": reply})
                return {"reply": reply, "history": history}

        else:
            # audit-log this turn (no tool call)
            log_interaction(
                user_id=request.user_id or "anonymous",
                query=user_input,
                tool=None,
                args=None,
                result=None,
                reply=message.content,
            )
            return {"reply": message.content, "history": history}

    except RateLimitError:
        raise HTTPException(status_code=429, detail="OpenAI rate limit exceeded. Please wait and try again.")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {e}")
    except Exception as ex:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {ex}")
