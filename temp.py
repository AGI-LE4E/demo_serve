from app.chains import validator_chain
from langchain_core.messages import HumanMessage

human_message = HumanMessage(content="제주도 여행 추천해줘")

res = validator_chain.invoke(input={"messages": [human_message]})

print(res)
