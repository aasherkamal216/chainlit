import chainlit as cl
from litellm import acompletion
import os
from dotenv import load_dotenv

_ : bool = load_dotenv()

@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chat history from the user session
    messages = cl.user_session.get("messages", [])
    
    # Append the current message to the chat history
    messages.append({"role": "user", "content": message.content})

    msg = cl.Message(content="")

    stream = await acompletion(
        model="gemini/gemini-2.0-flash",
        messages=messages,
        api_key=os.getenv("GOOGLE_API_KEY"),
        stream=True
        )
    
    full_response = "" # create an empty string to store the full response
    async for part in stream:
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)
            full_response += token # concatenate each token to the full response

    # Append the response to the chat history
    messages.append({"role": "assistant", "content": full_response})
    cl.user_session.set("messages", messages)

    await msg.update()