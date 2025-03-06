import streamlit as st
import pprint
from utils import generate_text
from coze_model import CozeAgentOutput, skill_to_command_id

st.header("大连医科大学物理学习助手")
with st.sidebar:
    # 学号登录部分
    student_id = st.text_input("请输入学号", key="student_id")
    login_button = st.button("登录")

    if 'is_logged_in' not in st.session_state:
        st.session_state.is_logged_in = False

    if login_button:
        if student_id:
            try:
                result, response = generate_text("权限管理", student_id)
                # 假设成功信息包含在 generated_texts 中
                success_keywords = ["成功", "Success"]
                success = any(any(keyword in text for keyword in success_keywords) for text in result.generated_texts)
                if success:
                    st.session_state.is_logged_in = True
                    st.success("登录成功！")
                else:
                    st.error("登录失败，请检查学号。")
                st.write("详细响应信息:")
                st.code(pprint.pformat(response), language="json")
            except Exception as e:
                st.error(f"登录过程中出现错误: {e}")
        else:
            st.error("请输入有效的学号。")

# 选择技能类别，删除权限管理选项
skill_category = st.selectbox(
    "选择技能类别",
    [
        "回答物理问题",
        "提供学习建议",
        "总结物理知识",
        "针对知识点出题",
        "批改学生答案并梳理知识点",
        "笔记管理 - 记笔记",
        "笔记管理 - 查笔记",
        "笔记管理 - 删除笔记",
        "知识图谱",
        "论文查询",
        "答疑"
    ]
)

# 用户输入内容，使用 text_area 实现大的文本块输入
data = st.text_area("请输入相关内容", height=200)
submit = st.button("提交")

if submit:
    if not data:
        st.info("请输入相关内容")
        st.stop()
    if not st.session_state.is_logged_in:
        st.info("请先使用学号登录。")
        st.stop()

    with st.spinner("AI 正在处理中，请稍等..."):
        try:
            result, response = generate_text(skill_category, data)
            result = CozeAgentOutput(**result.dict())
        except Exception as e:
            st.error(f"处理过程中出现错误: {e}")
            st.write("异常信息详细内容：")
            st.write(str(e))
            st.stop()

    st.divider()
    st.markdown("#### 生成结果")
    for text in result.generated_texts:
        st.write(text)
    st.markdown("#### 总结")
    st.write(result.summary)
    st.markdown("#### 快捷命令ID")
    st.write(result.commandId)

    st.write("详细响应信息:")
    st.code(pprint.pformat(response), language="json")