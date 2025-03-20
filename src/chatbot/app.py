import chainlit as cl
from litellm import acompletion

import os, base64
from dotenv import load_dotenv

from mcp import ClientSession

_ : bool = load_dotenv()

async def process_image(image: cl.Image):
    """
    Processes an image file, reads its data, and converts it to a base64 encoded string.
    """
    try:
        with open(image.path, "rb") as image_file:
            image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode("utf-8")
        return {
            "type": "image_url",
            "image_url": {
                "url": f"data:image/{image.mime.split('/')[-1]};base64,{base64_image}"
            }
        }
    except Exception as e:
        print(f"Error reading image file: {e}")
        return {"type": "text", "text": f"Error processing image {image.name}."}


@cl.on_mcp_connect
async def on_mcp(connection, session: ClientSession):
    # List available tools
    result = await session.list_tools()
    
    # Process tool metadata
    tools = [{
        "name": t.name,
        "description": t.description,
        "input_schema": t.inputSchema,
    } for t in result.tools]
    
    # Store tools for later use
    mcp_tools = cl.user_session.get("mcp_tools", {})
    mcp_tools[connection.name] = tools
    cl.user_session.set("mcp_tools", mcp_tools)


@cl.on_message
async def main(message: cl.Message):
    # Retrieve the chat history from the user session
    messages = cl.user_session.get("messages", [])
    mcp_tools = cl.user_session.get("mcp_tools", {})

    all_tools = [tool for connection_tools in mcp_tools.values() for tool in connection_tools]

    # Prepare the content list for the current message
    content = []

    # Add text content
    if message.content:
        content.append({"type": "text", "text": message.content})
    
    # Process image files
    image_elements = [element for element in message.elements if "image" in element.mime]
    for image in image_elements:
        if image.path:
            content.append(await process_image(image))
        else:
            print(f"Image {image.name} has no content and no path.")
            content.append({"type": "text", "text": f"Image {image.name} could not be processed."})
    
    # Append the current message to the chat history
    messages.append({"role": "user", "content": content})
    
    msg = cl.Message(content="")

    stream = await acompletion(
        model="gemini/gemini-2.0-flash",
        messages=messages,
        api_key=os.getenv("GOOGLE_API_KEY"),
        stream=True,
        tools=all_tools
        )
    
    full_response = "" # create an empty string to store the full response
    async for part in stream:
        print(part.choices[0].delta.tool_calls)
        if token := part.choices[0].delta.content or "":
            await msg.stream_token(token)
            full_response += token # concatenate each token to the full response

    # Append the response to the chat history
    messages.append({"role": "assistant", "content": full_response})
    cl.user_session.set("messages", messages)

    await msg.update()