import os
import openai
import json
from dotenv import load_dotenv
from app.chat import tools
from openai import OpenAIError, RateLimitError
from datetime import date

# Load environment variables
load_dotenv()

# Set API key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENAI_API_KEY in environment variables.")
openai.api_key = api_key
client = openai.OpenAI()

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
                    "subsidiary": {"type": "string", "description": "Filter by subsidiary name"},
                    "customer": {"type": "string", "description": "Filter by customer name"},
                    "status": {"type": "string", "description": "Invoice status (e.g., 'Open', 'Paid In Full')"},
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
                        "enum": ["subsidiary", "customer"],
                        "description": "Group AR by this field"
                    },
                    "status": {
                        "type": "string",
                        "description": "Filter invoices by status (e.g., 'Open')"
                    }
                },
                "required": []
            }
        }
    }
]

# Start chatbot
print("\n📊 Finance ChatBot is ready. Type 'exit' to quit.")
print("💬 Try asking:\n - Show open invoices\n - What's the AR balance by customer?\n")

history = []

while True:
    user_input = input("User: ")
    if user_input.lower() in ("exit", "quit"):
        break

    try:
        today_str = date.today().strftime("%B %d, %Y")  # Example: "May 7, 2025"
        # First completion: detect intent
        response = client.chat.completions.create(
            model="gpt-4-turbo-2024-04-09",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful financial assistant for a company controller. "
                        "Answer clearly and concisely. Only return data that matches user filters, like 'Open'. "
                        "Use bullet points or lists for readability. "
                        "Do not speculate or fabricate data. Only use what is returned by the API."
                        "Always try to be helpful and offer reporting suggestions based on data you have available."
                        "When applicable, interpret the user's intent and provide a detailed response."
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

                # Dispatch to appropriate tool
                if tool_name == "get_invoices":
                    result = tools.get_invoices(**arguments)
                elif tool_name == "get_ar_balance":
                    result = tools.get_ar_balance(**arguments)
                else:
                    result = {"error": f"No handler implemented for tool {tool_name}"}

                # Limit large result sets to avoid GPT token overflow
                """if isinstance(result, list) and len(result) > 25:
                    result = result[:25]"""

                # Summarize the tool result before adding it to the history
                summary = f"Tool {tool_name} executed successfully. Returned {len(result)} records." \
                    if isinstance(result, list) else str(result)

                # Append tool response as JSON
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result)
                })

                # Second completion: generate user-facing response
                follow_up = client.chat.completions.create(
                    model="gpt-4-turbo-2024-04-09",
                    messages=history
                )
                reply = follow_up.choices[0].message.content
                print(f"Bot: {reply}")
                history.append({"role": "assistant", "content": reply})
        else:
            print(f"Bot: {message.content}")

    except RateLimitError:
        print("Bot: ⚠️ I'm currently overloaded. Please wait and try again.")
    except OpenAIError as e:
        print(f"Bot: 🚫 OpenAI API error: {e}")
    except Exception as ex:
        print(f"Bot: ❌ Unexpected error: {ex}")