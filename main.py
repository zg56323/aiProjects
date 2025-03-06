import streamlit as st
from utils import generate_text, check_student_id_exists

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
                result = check_student_id_exists(student_id)
                if result is not None:
                    st.session_state.is_logged_in = True
                    st.success("登录成功！")
                else:
                    st.error("登录失败，请检查学号。")
            except Exception as e:
                st.error(f"登录过程中出现错误: {e}")
        else:
            st.error("请输入有效的学号。")

# 选择技能类别，删除权限管理选项
skill_category = st.selectbox(
    "选择技能类别",
    [
        "知识学习",
        "针对知识点出题",
        "笔记管理 - 记笔记",
        "笔记管理 - 查笔记",
        "笔记管理 - 删除笔记",
        "思维导图",
        "论文查询",
        "留言/答疑管理"
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
            result = generate_text(skill_category, data)
        except Exception as e:
            st.error(f"处理过程中出现错误: {e}")
            st.write("异常信息详细内容：")
            st.write(str(e))
            st.stop()

    st.divider()
    st.markdown("#### 生成结果")
    st.write(result)