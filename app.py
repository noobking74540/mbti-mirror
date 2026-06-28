"""
MBTI 灵魂镜像馆 - 治愈系完整版 (12题)
心灵的十六种镜像 · 全屏流式布局 v2.0
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import time

# ============================================================
# 页面配置
# ============================================================
st.set_page_config(
    page_title="MBTI 灵魂镜像馆",
    page_icon="🔮",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================
# 全设备全屏自适应 CSS (vh 视口单位 + 流式布局)
# ============================================================
st.markdown("""
<style>
    /* 1. 锁死全局应用高度为精确的 100% 视口高度，禁止溢出和横向滚动 */
    html, body, .stApp {
        height: 100vh !important;
        overflow: hidden !important;
        background-color: #232252 !important;
    }

    /* 2. 彻底隐藏 Streamlit 默认的 Header 和工具栏 */
    [data-testid="stHeader"] { display: none !important; }
    div[data-testid="stToolbar"] { display: none !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* 3. 核心全面屏卡片容器：采用动态比例（vh）重构 */
    .main .block-container {
        height: 100vh !important;
        padding-top: 4vh !important;
        padding-bottom: 4vh !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        max-width: 450px !important;
        margin: 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        justify-content: flex-start !important;
        gap: 2.5vh !important;
    }

    /* 4. 组件微调：确保在矮屏幕下字体和按钮自动适配 */
    @media (max-height: 700px) {
        .main .block-container { gap: 1.5vh !important; }
        h1 { font-size: 1.5rem !important; }
        div[data-testid="stRadio"] label p { font-size: 1.1rem !important; }
    }

    /* 5. 全局文字高亮白覆盖 */
    h1, h2, h3, .stMarkdown p, div[data-testid="stRadio"] label p {
        color: #FFFFFF !important;
    }

    /* 全局字体 */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; }

    /* 弹幕区域 */
    .barrage-area {
        position: relative;
        width: 100%;
        min-height: 45vh;
        overflow: hidden;
        margin-top: 1rem;
    }
    .barrage-container {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        pointer-events: none;
        z-index: 0;
    }
    .barrage-letter {
        position: absolute;
        font-size: 2.2rem;
        font-weight: 800;
        opacity: 0.08;
        color: #ffffff;
        white-space: nowrap;
        animation: barrageFlow linear infinite;
        letter-spacing: 0.1em;
    }
    .barrage-letter:nth-child(1) { top: 5%; left: -120px; animation-duration: 18s; animation-delay: 0s; font-size: 2.8rem; }
    .barrage-letter:nth-child(2) { top: 14%; left: -160px; animation-duration: 22s; animation-delay: 2s; font-size: 2.4rem; }
    .barrage-letter:nth-child(3) { top: 24%; left: -100px; animation-duration: 16s; animation-delay: 4s; font-size: 3.2rem; }
    .barrage-letter:nth-child(4) { top: 33%; left: -140px; animation-duration: 20s; animation-delay: 1s; font-size: 2.0rem; }
    .barrage-letter:nth-child(5) { top: 42%; left: -180px; animation-duration: 24s; animation-delay: 3s; font-size: 2.6rem; }
    .barrage-letter:nth-child(6) { top: 52%; left: -110px; animation-duration: 17s; animation-delay: 5s; font-size: 3.0rem; }
    .barrage-letter:nth-child(7) { top: 62%; left: -150px; animation-duration: 21s; animation-delay: 0.5s; font-size: 2.2rem; }
    .barrage-letter:nth-child(8) { top: 72%; left: -90px; animation-duration: 19s; animation-delay: 3.5s; font-size: 2.8rem; }
    .barrage-letter:nth-child(9) { top: 82%; left: -130px; animation-duration: 15s; animation-delay: 1.5s; font-size: 2.4rem; }
    .barrage-letter:nth-child(10) { top: 91%; left: -170px; animation-duration: 23s; animation-delay: 4.5s; font-size: 2.0rem; }
    .barrage-letter:nth-child(11) { top: 8%; left: 110%; animation-duration: 25s; animation-delay: 0s; font-size: 2.6rem; }
    .barrage-letter:nth-child(12) { top: 22%; left: 110%; animation-duration: 20s; animation-delay: 2.5s; font-size: 2.2rem; }
    .barrage-letter:nth-child(13) { top: 36%; left: 110%; animation-duration: 22s; animation-delay: 1s; font-size: 2.8rem; }
    .barrage-letter:nth-child(14) { top: 50%; left: 110%; animation-duration: 18s; animation-delay: 4s; font-size: 2.4rem; }
    .barrage-letter:nth-child(15) { top: 64%; left: 110%; animation-duration: 26s; animation-delay: 3s; font-size: 2.0rem; }
    .barrage-letter:nth-child(16) { top: 78%; left: 110%; animation-duration: 24s; animation-delay: 1.5s; font-size: 2.2rem; }
    @keyframes barrageFlow {
        0% { transform: translateX(0) translateY(0) rotate(0deg); opacity: 0.08; }
        10% { opacity: 0.12; }
        90% { opacity: 0.12; }
        100% { transform: translateX(calc(100vw + 200px)) translateY(-20px) rotate(3deg); opacity: 0; }
    }

    /* Banner 容器 */
    .banner-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 1rem 0.5rem 0.5rem;
    }
    .banner-icon {
        font-size: 5rem;
        margin-bottom: 1rem;
        animation: float 3s ease-in-out infinite;
    }
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-15px); }
        100% { transform: translateY(0px); }
    }
    .banner-title {
        font-size: 3.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    .banner-subtitle {
        font-size: 1.1rem;
        color: rgba(255,255,255,0.6);
        font-weight: 300;
        max-width: 500px;
        line-height: 1.7;
        margin-bottom: 2.5rem;
    }

    /* 致用户信 */
    .letter-container {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        text-align: left;
    }
    .letter-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #f093fb;
        margin-bottom: 0.8rem;
        text-align: center;
    }
    .letter-text {
        font-size: 0.95rem;
        color: rgba(255,255,255,0.8);
        line-height: 1.8;
        margin-bottom: 0.5rem;
    }
    .letter-sign {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.5);
        text-align: right;
        margin-top: 0.8rem;
        font-style: italic;
    }

    /* 答题卡片 */
    .question-card {
        background: rgba(255,255,255,0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 24px;
        padding: 2rem;
        margin: 0.5rem 0;
    }
    .question-text {
        font-size: 1.3rem;
        font-weight: 600;
        color: white;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }

    /* 进度条 */
    .progress-container {
        margin-bottom: 1rem;
    }
    .progress-label {
        color: rgba(255,255,255,0.5);
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 0.3rem;
    }

    /* 结果页 */
    .result-container {
        text-align: center;
        padding: 1rem 0;
    }
    .result-type {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin: 0.5rem 0;
    }
    .result-tag {
        display: inline-block;
        background: rgba(240, 147, 251, 0.2);
        border: 1px solid rgba(240, 147, 251, 0.3);
        color: #f093fb;
        padding: 0.3rem 1.2rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 500;
        margin: 0.3rem;
    }
    .result-quote {
        font-size: 1rem;
        color: rgba(255,255,255,0.7);
        font-style: italic;
        max-width: 500px;
        margin: 1rem auto;
        line-height: 1.6;
    }
    .result-section-title {
        color: rgba(255,255,255,0.5);
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 1.5rem;
        margin-bottom: 0.8rem;
    }
    .result-deep {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        text-align: left;
    }
    .result-deep-title {
        font-size: 1rem;
        font-weight: 700;
        color: #f093fb;
        margin-bottom: 0.5rem;
    }
    .result-deep-text {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
    }
    .result-heal {
        background: linear-gradient(135deg, rgba(240,147,251,0.1), rgba(79,172,254,0.1));
        border: 1px solid rgba(240,147,251,0.2);
        border-radius: 16px;
        padding: 1.2rem;
        margin: 0.8rem 0;
        text-align: left;
    }
    .result-heal-title {
        font-size: 1rem;
        font-weight: 700;
        color: #4facfe;
        margin-bottom: 0.5rem;
    }
    .result-heal-text {
        font-size: 0.9rem;
        color: rgba(255,255,255,0.8);
        line-height: 1.7;
    }

    /* 选项按钮 */
    .stRadio > div {
        display: flex;
        flex-direction: column;
        gap: 0.6rem;
    }
    .stRadio label {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 16px !important;
        padding: 0.8rem 1.2rem !important;
        color: #ffffff !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    .stRadio label span { color: #ffffff !important; }
    .stRadio label:hover {
        background: rgba(255,255,255,0.15) !important;
        border-color: rgba(240, 147, 251, 0.5) !important;
    }
    .stRadio label[data-selected="true"] {
        background: rgba(240, 147, 251, 0.2) !important;
        border-color: #f093fb !important;
    }
    .stRadio label [data-testid="stWidgetLabel"] + div { color: #ffffff !important; }
    .stRadio [role="radio"] { color: #ffffff !important; }

    /* 警告框 */
    .stAlert {
        background: rgba(255, 193, 7, 0.1) !important;
        border: 1px solid rgba(255, 193, 7, 0.3) !important;
        border-radius: 12px !important;
        color: #ffc107 !important;
    }
    hr { border-color: rgba(255,255,255,0.1) !important; }

    /* 按钮 */
    .stButton > button {
        width: 100% !important;
        min-height: 3rem !important;
        padding: 0.6rem 1rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        border-radius: 16px !important;
        letter-spacing: 0.03em;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Session State 初始化
# ============================================================
if "page" not in st.session_state:
    st.session_state.page = "welcome"
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "answers" not in st.session_state:
    st.session_state.answers = []
if "mbti_result" not in st.session_state:
    st.session_state.mbti_result = None

# ============================================================
# 12 道题完整题库 (4维度 × 3题)
# ============================================================
QUESTIONS = [
    # === 维度1: E vs I (Q1-Q3) ===
    {
        "text": "忙碌了一周，周末终于到来，你更倾向于如何恢复能量？",
        "options": [
            "A. 约上三五好友，去热闹的聚会或户外活动，在人群中充电",
            "B. 一个人宅家看书、看电影、听音乐，享受独处的宁静时光",
        ],
        "dimension": "EI",
    },
    {
        "text": "在社交场合中，你通常是什么样的状态？",
        "options": [
            "A. 主动与人攀谈，享受认识新朋友的过程，话题源源不断",
            "B. 更愿意待在熟悉的小圈子里，或安静观察，不太主动开启话题",
        ],
        "dimension": "EI",
    },
    {
        "text": "当你遇到一个有趣的想法时，你的第一反应是？",
        "options": [
            "A. 立刻找人分享讨论，在交流中碰撞出更多火花",
            "B. 先在内心反复琢磨，等自己想清楚了再决定是否说出来",
        ],
        "dimension": "EI",
    },
    # === 维度2: S vs N (Q4-Q6) ===
    {
        "text": "在阅读或学习时，你更容易被什么内容吸引？",
        "options": [
            "A. 具体的案例、真实的故事、能立刻应用到生活中的实用信息",
            "B. 抽象的概念、宏大的理论、关于未来可能性的畅想",
        ],
        "dimension": "SN",
    },
    {
        "text": "当你描述一件事时，你更倾向于？",
        "options": [
            "A. 按照时间顺序，详细描述发生了什么、谁说了什么、具体细节",
            "B. 抓住核心感受和整体印象，用比喻或联想来表达",
        ],
        "dimension": "SN",
    },
    {
        "text": '对于"改变"这件事，你的态度是？',

        "options": [
            "A. 更喜欢稳定和可预期，改变需要充分的理由和准备",
            "B. 拥抱变化，觉得不确定性中藏着新的机会和可能性",
        ],
        "dimension": "SN",
    },
    # === 维度3: T vs F (Q7-Q9) ===
    {
        "text": "朋友向你倾诉烦恼时，你通常会？",
        "options": [
            "A. 先帮他分析问题的根源，给出理性的建议和解决方案",
            "B. 先共情他的感受，陪伴他，让他感觉被理解和支持",
        ],
        "dimension": "TF",
    },
    {
        "text": "在做重要决定时，你更依赖什么？",
        "options": [
            "A. 逻辑分析、客观数据、公平原则和效率最大化",
            "B. 内心的价值观、对他人感受的影响、以及人情世故",
        ],
        "dimension": "TF",
    },
    {
        "text": '对于"批评"这件事，你的看法是？',

        "options": [
            "A. 对事不对人，直接指出问题是为了帮助对方进步，不需要委婉",
            "B. 批评前会考虑对方的感受，尽量用温和的方式，避免伤害关系",
        ],
        "dimension": "TF",
    },
    # === 维度4: J vs P (Q10-Q12) ===
    {
        "text": "对于即将到来的假期，你通常会怎么规划？",
        "options": [
            "A. 提前制定详细的行程计划，每天做什么都安排得明明白白",
            "B. 大概有个方向就好，到了再说，享受随遇而安的惊喜",
        ],
        "dimension": "JP",
    },
    {
        "text": "你的工作/学习空间通常是怎样的？",
        "options": [
            "A. 整洁有序，每样东西都有固定的位置，喜欢做完一件事再开始下一件",
            "B. 看起来有点乱但自己知道东西在哪，喜欢同时开启多个任务",
        ],
        "dimension": "JP",
    },
    {
        "text": "面对截止日期，你更接近哪种状态？",
        "options": [
            "A. 提前规划，稳步推进，喜欢在截止日期前早早完成",
            "B. 在压力下反而更有灵感，常常在最后一刻爆发出高效",
        ],
        "dimension": "JP",
    },
]

# ============================================================
# 治愈系人格数据库 (16型完整覆盖)
# ============================================================
MBTI_PROFILES = {
    "ISFJ": {
        "tag": "守护者 · 静谧的灯塔",
        "title": "守护者的眼泪：ISFJ（静谧的灯塔）",
        "quote": "「你总是温柔地守护着身边的一切，却忘了自己也需要被守护。」",
        "deep": "你有一种近乎本能的温柔，总是在别人开口之前就已经察觉到了他们的需要。你记得每个人的喜好，在意每个人的感受，却常常把自己的情绪藏在最深的角落。你不是没有脾气，只是选择了用善意去化解。你不是不累，只是觉得别人的笑容比自己的休息更重要。你就像一座静谧的灯塔，在黑暗中为他人照亮归途，却让自己的光芒在风中摇曳。",
        "heal": "亲爱的守护者，请允许自己偶尔也做那个被守护的人。你的善良不是理所当然的，你的付出值得被看见、被珍惜。从今天开始，试着把对自己的温柔也列入待办清单——你值得拥有同样深情的拥抱。",
        "strengths": ["细腻体贴", "责任心强", "善于倾听", "忠诚可靠"],
        "weaknesses": ["过度牺牲", "害怕改变", "压抑自我", "过于谨慎"],
    },
    "INFP": {
        "tag": "治愈者 · 流浪的星光",
        "title": "孤勇的理想主义：INFP（流浪的星光）",
        "quote": "「你的内心住着一个永不妥协的理想国，那是你在这个世界最珍贵的领地。」",
        "deep": '你看起来温和柔软，内心却有着不可动摇的坚持。你在人群中常常沉默，不是因为无话可说，而是因为你的世界太过丰富，不知从何说起。你相信真善美，相信灵魂的共鸣，相信那些别人觉得"不现实"的东西。你在这世俗的洪流中小心翼翼地守护着内心的火焰，哪怕被嘲笑天真，也不愿让它熄灭。',

        "heal": "亲爱的理想主义者，请继续相信你所相信的。这个世界需要你这样的灵魂，需要你那份不切实际的浪漫和纯粹。你的敏感不是弱点，是你感知美好的天赋。不要因为走得慢而怀疑自己，你只是在用自己的节奏，走向属于你的星辰大海。",
        "strengths": ["共情力极强", "创造力丰富", "价值观坚定", "善于倾听"],
        "weaknesses": ["过度理想化", "容易内耗", "决策困难", "过于敏感"],
    },
    "INTJ": {
        "tag": "建筑师 · 深海的独行舟",
        "title": "孤独的思考者：INTJ（深海的独行舟）",
        "quote": "「你的孤独不是缺陷，而是你选择了一条少有人走的路。」",
        "deep": "你总是那个看得最远的人，在别人还在为眼前的小事欢呼时，你已经在思考五年后的布局。你的理性让你显得疏离，但只有你知道，那层坚硬的外壳下藏着多么敏感的灵魂。你不擅长表达情感，不是因为没有感情，而是因为你的感情太深太重，找不到合适的语言去承载。你像一艘在深海中独行的舟，表面平静，内心却承载着整片海洋的重量。",
        "heal": "亲爱的思考者，你的孤独是一种力量，但请不要让它成为枷锁。世界上或许很少有人能真正理解你，但那个愿意理解你的人正在赶来的路上。在等待的同时，请记得：你不需要完美才值得被爱，你不需要强大到无坚不摧。偶尔的脆弱，也是你完整的一部分。",
        "strengths": ["战略思维", "独立自主", "高标准", "执行力强"],
        "weaknesses": ["过于挑剔", "情感疏离", "固执己见", "完美主义"],
    },
    "ENFP": {
        "tag": "倡导者 · 盛大的追光者",
        "title": "快乐的向日葵：ENFP（盛大的追光者）",
        "quote": "「你的热情像阳光一样温暖了很多人，但别忘了，你也需要被照亮。」",
        "deep": "你是人群中的小太阳，总是带着灿烂的笑容和无穷的能量。你热爱一切新鲜的事物，对世界充满好奇，你的热情感染着身边的每一个人。但很少有人知道，在那些热闹的喧嚣散去之后，你也会感到一种深深的孤独。你给了别人那么多快乐，却常常不知道如何让自己真正快乐。你追逐着光，却忘了自己本身就是光。",
        "heal": '亲爱的追光者，你的热情是这个世界上最珍贵的礼物。但请记住，你不需要永远发光，不需要永远快乐。允许自己有低落的时刻，允许自己说"我累了"。真正爱你的人，爱的不仅是你的阳光，还有你藏在阳光背后的影子。停下来休息不是放弃，而是为了更好地出发。',

        "strengths": ["热情洋溢", "社交达人", "创意无限", "善于激励他人"],
        "weaknesses": ["难以专注", "过度乐观", "计划性弱", "情绪波动大"],
    },
}

# ============================================================
# 通用兜底文案 (其余12型)
# ============================================================
FALLBACK_PROFILES = {
    "ENFJ": {
        "tag": "主人公 · 魅力导师",
        "quote": "「你天生就是别人的灯塔，但别忘了为自己留一盏灯。」",
    },
    "INFJ": {
        "tag": "提倡者 · 洞察先知",
        "quote": "「你看见了这个世界的复杂，却依然选择温柔以待。」",
    },
    "ENTJ": {
        "tag": "指挥官 · 天生领袖",
        "quote": "「你的果断和远见，是改变世界的力量。」",
    },
    "ENTP": {
        "tag": "辩论家 · 创新挑战者",
        "quote": "「你的思维是一把锋利的剑，记得用它来创造而非伤害。」",
    },
    "ISTJ": {
        "tag": "物流师 · 可靠守护者",
        "quote": "「你的可靠是这个浮躁世界里最稀缺的品质。」",
    },
    "ESTJ": {
        "tag": "总经理 · 高效执行者",
        "quote": "「你的执行力让梦想照进现实。」",
    },
    "ESFJ": {
        "tag": "执政官 · 社交润滑剂",
        "quote": "「你让身边的每个人都感到被关心，这是最温柔的超能力。」",
    },
    "ISTP": {
        "tag": "鉴赏家 · 冷静实干家",
        "quote": "「你的冷静和务实，是暴风雨中最稳的锚。」",
    },
    "ESTP": {
        "tag": "企业家 · 冒险行动派",
        "quote": "「你的行动力让一切不可能变成可能。」",
    },
    "ISFP": {
        "tag": "探险家 · 静谧艺术家",
        "quote": "「你眼中的世界，比任何人都要美丽。」",
    },
    "ESFP": {
        "tag": "表演者 · 快乐传播者",
        "quote": "「你的快乐有一种魔力，能让阴天也放晴。」",
    },
    "INTP": {
        "tag": "逻辑学家 · 哲学思考者",
        "quote": "「你的好奇心是通往无限可能的钥匙。」",
    },
}


def get_profile(mbti_type):
    """获取人格档案，带防空兜底"""
    if mbti_type in MBTI_PROFILES:
        return MBTI_PROFILES[mbti_type]
    # 兜底：从 FALLBACK 获取或生成通用文案
    fallback = FALLBACK_PROFILES.get(mbti_type, {
        "tag": "宇宙探索者",
        "quote": "「你是宇宙中独一无二的宝藏，你的光芒正在被看见。」",
    })
    return {
        "tag": fallback["tag"],
        "title": f"灵魂探索者：{mbti_type}（{fallback['tag']}）",
        "quote": fallback["quote"],
        "deep": f"亲爱的 {mbti_type}，你也是宇宙中独一无二的宝藏。每一种人格都是一首独特的诗，而你正在书写属于自己的篇章。专属深度解析正在加载中，请相信，你的存在本身就是一种治愈。",
        "heal": "无论你是谁，无论你在哪里，都请记得：你值得被爱，值得被理解，值得拥有这世间所有的温柔。你的每一次呼吸，都是宇宙在说——你在这里，就很好。",
        "strengths": ["独特视角", "内在力量", "成长潜力", "无限可能"],
        "weaknesses": ["自我探索中", "等待发现", "正在成长", "潜力无限"],
    }


# ============================================================
# 页面渲染函数
# ============================================================

def render_welcome():
    """首页：致用户信 + 开始按钮"""
    # 弹幕
    barrage_types = [
        "INTJ：建筑师", "INTP：逻辑学家", "ENTJ：指挥官", "ENTP：辩论家",
        "INFJ：提倡者", "INFP：调停者", "ENFJ：主人公", "ENFP：竞选者",
        "ISTJ：物流师", "ISFJ：守卫者", "ESTJ：总经理", "ESFJ：执政官",
        "ISTP：鉴赏家", "ISFP：艺术家", "ESTP：企业家", "ESFP：表演者",
    ]
    barrage_html = '<div class="barrage-container">'
    for t in barrage_types:
        barrage_html += f'<span class="barrage-letter">{t}</span>'
    barrage_html += "</div>"

    # Banner
    st.markdown('<div class="banner-container">', unsafe_allow_html=True)
    st.markdown('<div class="banner-icon">🔮</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="banner-title">MBTI<br>灵魂镜像馆</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="banner-subtitle">'
        "在纷繁的世界里，你究竟是怎样的灵魂？<br>"
        "12 道精选问题，带你窥见人格深处的镜像。"
        "</div>",
        unsafe_allow_html=True,
    )

    # 致用户信
    st.markdown("""
    <div class="letter-container">
        <div class="letter-title">📌 测前致你的一封信</div>
        <div class="letter-text">
            亲爱的旅人，你好。
        </div>
        <div class="letter-text">
            在开始这段探索之旅前，请允许我轻轻地对你说：<br>
            这不是一场考试，没有对错，没有好坏。<br>
            这只是你与自己内心的一次温柔对话。
        </div>
        <div class="letter-text">
            你不需要刻意选择"看起来更好"的答案，<br>
            只需要诚实地倾听内心的声音。<br>
            那个最自然的反应，往往藏着最真实的你。
        </div>
        <div class="letter-text">
            12 道题，大约 3 分钟。<br>
            愿你在这一小段旅程中，遇见那个或许被你忽略已久的自己。
        </div>
        <div class="letter-sign">—— 灵魂镜像馆 · 守馆人</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("✨ 开始契约", key="start_btn", use_container_width=True):
            st.session_state.page = "quiz"
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # 弹幕区域
    st.markdown(f'<div class="barrage-area">{barrage_html}</div>', unsafe_allow_html=True)


def render_quiz():
    """答题流：单题切换，12题完整流程"""
    total = len(QUESTIONS)
    q_idx = st.session_state.current_q

    if q_idx >= total:
        calculate_result()
        return

    q = QUESTIONS[q_idx]

    # 进度条
    progress = q_idx / total
    st.markdown('<div class="progress-container">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="progress-label">第 {q_idx + 1} / {total} 题</div>',
        unsafe_allow_html=True,
    )
    st.progress(progress)
    st.markdown("</div>", unsafe_allow_html=True)

    # 题目卡片
    st.markdown('<div class="question-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="question-text">{q["text"]}</div>', unsafe_allow_html=True)

    # 选项
    selected = st.radio(
        "选择你的答案",
        q["options"],
        key=f"q_{q_idx}",
        label_visibility="collapsed",
        index=None,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        btn_label = "✨ 查看镜像" if q_idx == total - 1 else "下一题 →"
        if st.button(btn_label, key="next_btn", use_container_width=True):
            if selected is None:
                st.warning("请先选择一个选项，再继续前进 ✨")
            else:
                # 记录答案字母
                dim = q["dimension"]
                if dim == "EI":
                    choice = "E" if selected.startswith("A") else "I"
                elif dim == "SN":
                    choice = "S" if selected.startswith("A") else "N"
                elif dim == "TF":
                    choice = "T" if selected.startswith("A") else "F"
                else:  # JP
                    choice = "J" if selected.startswith("A") else "P"
                st.session_state.answers.append(choice)
                st.session_state.current_q += 1
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def calculate_result():
    """治愈系计分引擎：统计4维度，取多数"""
    answers = st.session_state.answers

    with st.spinner("正在通过量子算法窥探你灵魂深处的镜像..."):
        time.sleep(1.5)

    # 按维度分组统计
    # Q1-Q3: EI, Q4-Q6: SN, Q7-Q9: TF, Q10-Q12: JP
    ei_answers = answers[0:3]
    sn_answers = answers[3:6]
    tf_answers = answers[6:9]
    jp_answers = answers[9:12]

    def majority(votes, opt1, opt2):
        """取多数，平局时取 opt1"""
        c1 = sum(1 for v in votes if v == opt1)
        c2 = sum(1 for v in votes if v == opt2)
        return opt1 if c1 >= c2 else opt2

    ei = majority(ei_answers, "E", "I")
    sn = majority(sn_answers, "S", "N")
    tf = majority(tf_answers, "T", "F")
    jp = majority(jp_answers, "J", "P")

    mbti_type = ei + sn + tf + jp
    st.session_state.mbti_result = mbti_type

    # 保存到 CSV
    save_result(mbti_type)

    st.session_state.page = "result"
    st.rerun()


def save_result(mbti_type):
    """将测试结果保存到 CSV"""
    csv_path = os.path.join(os.path.dirname(__file__), "test_results.csv")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame([[now, mbti_type]], columns=["timestamp", "mbti_type"])
    try:
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df = pd.concat([df, new_row], ignore_index=True)
        else:
            df = new_row
        df.to_csv(csv_path, index=False)
    except Exception:
        pass  # 静默保存，不影响用户体验


def render_result():
    """结果页：高定治愈系渲染"""
    mbti_type = st.session_state.mbti_result
    profile = get_profile(mbti_type)

    # 仪式感特效
    st.snow()
    st.balloons()

    # 结果容器
    st.markdown('<div class="result-container">', unsafe_allow_html=True)

    # 人格类型
    st.markdown(f'<div class="result-type">{mbti_type}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="result-tag">{profile["tag"]}</div>', unsafe_allow_html=True)

    # 标题
    st.markdown(f'<h2 style="color:#FFFFFF; text-align:center; margin-top:0.5rem;">{profile["title"]}</h2>', unsafe_allow_html=True)

    # 引言
    st.markdown(f'<div class="result-quote">{profile["quote"]}</div>', unsafe_allow_html=True)

    # 深度懂你
    st.markdown('<div class="result-section-title">✦ 深度懂你 ✦</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-deep">'
        f'<div class="result-deep-title">💫 灵魂素描</div>'
        f'<div class="result-deep-text">{profile["deep"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 治愈寄语
    st.markdown('<div class="result-section-title">✦ 治愈寄语 ✦</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="result-heal">'
        f'<div class="result-heal-title">🌿 给你的温柔</div>'
        f'<div class="result-heal-text">{profile["heal"]}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    # 优势与成长
    st.markdown('<div class="result-section-title">✦ 你的光芒 ✦</div>', unsafe_allow_html=True)
    strengths_html = "".join(
        f'<span class="result-tag">✨ {s}</span>' for s in profile["strengths"]
    )
    st.markdown(f'<div style="text-align:center;">{strengths_html}</div>', unsafe_allow_html=True)

    st.markdown('<div class="result-section-title">✦ 成长空间 ✦</div>', unsafe_allow_html=True)
    weaknesses_html = "".join(
        f'<span class="result-tag" style="color:#f5576c; border-color:rgba(245,87,108,0.3); background:rgba(245,87,108,0.1);">🌱 {w}</span>'
        for w in profile["weaknesses"]
    )
    st.markdown(f'<div style="text-align:center;">{weaknesses_html}</div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # 重新测试按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🔄 重新探索", key="restart_btn", use_container_width=True):
            st.session_state.page = "welcome"
            st.session_state.current_q = 0
            st.session_state.answers = []
            st.session_state.mbti_result = None
            st.rerun()


# ============================================================
# 主路由
# ============================================================
def main():
    page = st.session_state.page
    if page == "welcome":
        render_welcome()
    elif page == "quiz":
        render_quiz()
    elif page == "result":
        render_result()


if __name__ == "__main__":
    main()


