import json
import os
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatStatus, MessageContentType, ChatEventType
from coze_model import CozeAgentOutput, skill_to_command_id
from prompt_template import skill_prompt_templates

# Get an access_token through personal access token or oauth.
coze_api_token = 'pat_BtEoJPFQQOi1TQNjKfTLNomEDOoLHPfTTCq7QB9ltrpvdn3RJMQsI7osoMENPQVS'
# The default access is api.coze.com, but if you need to access api.coze.cn,
# please use base_url to configure the api endpoint to access
coze_api_base = COZE_CN_BASE_URL

# Init the Coze client through the access_token.
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)

# Create a bot instance in Coze, copy the last number from the web link as the bot's ID.
bot_id = '7475982490700890151'
# The user id identifies the identity of a user. Developers can use a custom business ID
# or a random string.
user_id = 'gavin'

# 用于保存聊天记录
chat_history = []

def generate_text(skill_category, data):
    global chat_history
    if skill_category not in skill_prompt_templates:
        raise ValueError(f"不支持的技能类别: {skill_category}")

    system_template = skill_prompt_templates[skill_category]["system"]
    user_template = skill_prompt_templates[skill_category]["user"]

    formatted_user = user_template.format(data=data)

    full_prompt = f"{formatted_user}"

    # 将当前用户消息添加到聊天记录
    user_message = Message.build_user_question_text(full_prompt)
    chat_history.append(user_message)

    generated_text = ""
    response = None
    for event in coze.chat.stream(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=chat_history,
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            generated_text += event.message.content
        if event.event == ChatEventType.CONVERSATION_CHAT_COMPLETED:
            token_usage = event.chat.usage.token_count
            # 模拟构建完整响应
            response = {
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "content": generated_text,
                            "role": "assistant"
                        },
                        "stop_reason": "stop"
                    }
                ],
                "model": "豆包·工具调用",
                "usage": {
                    "completion_tokens": token_usage,
                    "prompt_tokens": 0,  # 这里假设没有额外的 prompt 计算逻辑
                    "total_tokens": token_usage
                }
            }
            # 将机器人回复添加到聊天记录
            bot_message = Message.build_bot_answer_text(generated_text)
            chat_history.append(bot_message)

    # 根据 skill_category 获取 commandId
    command_id = skill_to_command_id.get(skill_category)
    if isinstance(command_id, dict):
        # 处理笔记管理的子操作，这里简单假设没有子操作，实际需要根据具体情况处理
        command_id = command_id.get("记笔记")  # 示例，可根据实际情况修改
    if command_id is None:
        command_id = "未明确映射"

    output = CozeAgentOutput(
        generated_texts=[generated_text],
        summary="",
        commandId=command_id
    )
    return output, response

def serialize_result(result):
    try:
        return json.dumps(result.dict(), ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"序列化结果时出错: {e}")
        return None