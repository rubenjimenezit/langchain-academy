from dotenv import load_dotenv
load_dotenv()

from langchain_anthropic import ChatAnthropic

sonnet_chat = ChatAnthropic(model="claude-sonnet-4-5")  # type: ignore[call-arg]




from langchain_core.messages import HumanMessage

msg = HumanMessage(content="What year is it?")

messages = [msg]

answer = sonnet_chat.invoke(messages)

print (answer)