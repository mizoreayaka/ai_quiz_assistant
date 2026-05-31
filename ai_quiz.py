import streamlit as st
from openai import OpenAI
import random
import os

# ==================== 配置 ====================
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
if not DEEPSEEK_API_KEY:
    try:
        import streamlit as st
        DEEPSEEK_API_KEY = st.secrets["DEEPSEEK_API_KEY"]
    except:
        raise ValueError("未找到 DEEPSEEK_API_KEY，请设置环境变量或Streamlit Secrets。")

# 初始化 DeepSeek 客户端
client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com"
)

# ==================== 页面布局 ====================
st.set_page_config(page_title="语文课堂AI出题助手", layout="centered")

st.title("📚 语文课堂AI出题助手")
st.markdown("点击下方按钮，AI会随机生成一道语文知识题，适合课堂互动。")

# 题目类型列表
question_types = ["成语填空", "诗词接龙", "文学常识", "修辞手法判断", "字音字形"]

# 会话状态：保存当前题目和答案
if "current_question" not in st.session_state:
    st.session_state.current_question = None
if "current_answer" not in st.session_state:
    st.session_state.current_answer = None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# ==================== 生成题目函数 ====================
import re  # 记得在文件顶部添加这个 import

def generate_question():
    """调用DeepSeek生成一道语文题，使用健壮的解析方法"""
    q_type = random.choice(question_types)
    
    prompt = f"""
    你是一位高年级小学语文老师。请出一道关于“{q_type}”的题目，要求综合考验学生水平。
    要求：
    1. 题目要适合课堂提问,不要出很基础的题目。
    2. 题目要有明确的答案。
    3. 输出格式必须严格如下：先以“题目：”开头，紧跟着题目内容；然后换行，以“答案：”开头，紧跟着答案内容。
    4. 不要输出其他任何无关的文字或空行。
    5. 如果是成语填字，给出空缺字时也给出成语的意思。
    
    示例输出格式：
    题目：请说出“月落乌啼霜满天”的下一句。
    答案：江枫渔火对愁眠。
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=500  # 增大 token 限制，防止长答案被截断
        )
        content = response.choices[0].message.content.strip()
        
        # 使用正则表达式提取题目和答案，不再依赖固定的行数
        # 提取“题目：”到“答案：”之间的内容作为题目
        question_match = re.search(r"题目：\s*(.*?)\s*答案：", content, re.DOTALL)
        # 提取“答案：”之后的所有内容作为答案
        answer_match = re.search(r"答案：\s*(.*)", content, re.DOTALL)
        
        if question_match and answer_match:
            question = question_match.group(1).strip()
            answer = answer_match.group(1).strip()
            return question, answer
        else:
            # 如果解析失败，尝试按行解析作为备选方案
            lines = content.split('\n')
            question = lines[0].replace("题目：", "").strip()
            # 如果第二行存在但不是答案，尝试寻找真正的“答案：”行
            answer = "答案见上"
            for line in lines:
                if line.startswith("答案："):
                    answer = line.replace("答案：", "").strip()
                    break
            return question, answer
            
    except Exception as e:
        return f"出题失败：{str(e)}", ""

# ==================== 页面按钮 ====================
col1, col2 = st.columns(2)

with col1:
    if st.button("🎯 出题", use_container_width=True):
        st.session_state.show_answer = False
        q, a = generate_question()
        st.session_state.current_question = q
        st.session_state.current_answer = a

with col2:
    if st.button("💡 显示答案", use_container_width=True):
        st.session_state.show_answer = True

# ==================== 显示内容 ====================
if st.session_state.current_question:
    st.markdown("---")
    st.subheader("📝 题目")
    st.markdown(f"### {st.session_state.current_question}")
    
    if st.session_state.show_answer:
        st.markdown("---")
        st.subheader("✅ 答案")
        st.markdown(f"### {st.session_state.current_answer}")
        st.balloons()  # 放个彩蛋，增加课堂趣味
else:
    st.info("👆 点击「出题」按钮开始课堂互动！")

# ==================== 页脚 ====================
st.markdown("---")
st.caption("💡 每道题由AI实时生成，适合课堂互动。")
