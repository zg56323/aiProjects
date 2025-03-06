
import sqlite3
from cozepy import COZE_CN_BASE_URL
from cozepy import Coze, TokenAuth, Message, ChatEventType
from prompt_template import skill_prompt_templates
coze_api_token = 'pat_BtEoJPFQQOi1TQNjKfTLNomEDOoLHPfTTCq7QB9ltrpvdn3RJMQsI7osoMENPQVS'
coze_api_base = COZE_CN_BASE_URL
coze = Coze(auth=TokenAuth(token=coze_api_token), base_url=coze_api_base)
bot_id = '7475982490700890151'
user_id = 'gavin'

def generate_text(skill_category, data):

    if skill_category not in skill_prompt_templates:
        raise ValueError(f"不支持的技能类别: {skill_category}")
    user_template = skill_prompt_templates[skill_category]["user"]
    formatted_user = user_template.format(data=data)
    full_prompt = f"{formatted_user}"
    user_message = Message.build_user_question_text(full_prompt)

    response = ""
    for event in coze.chat.stream(
        bot_id=bot_id,
        user_id=user_id,
        additional_messages=[user_message],
    ):
        if event.event == ChatEventType.CONVERSATION_MESSAGE_DELTA:
            generated_text = event.message
            print(f"role={generated_text.role}, content={generated_text.content}")
            response += generated_text.content

    return response

def check_student_id_exists(student_id):
    conn = sqlite3.connect('identifier.sqlite')  # 修改为 identifier.sqlite
    cursor = conn.cursor()
    cursor.execute('SELECT 1 FROM main.student WHERE student_id = ?', (student_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

