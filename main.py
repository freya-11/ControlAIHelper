# 备份主文件
# 原始文件：main.py
import streamlit as st
import time
import hashlib
from functions import (
    generate_ai_exam_paper,
    plot_root_locus,
    plot_bode_diagram,
    calculate_second_order_params,
    plot_second_order_step,
    plot_pid_step_response,
    calculate_steady_error,
    init_ark_client_once,
    get_word_download_data
)

# ---------------------- 页面配置 ----------------------
st.set_page_config(
    page_title="自动控制原理学习助手 | AI出题+考点解析+系统分析",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------- 自定义CSS样式 ----------------------
st.markdown("""
<style>
    /* 全局样式 */
    body {
        background-color: #fff9e6 !important;
        font-family: 'Microsoft YaHei', sans-serif;
        background-image: 
            radial-gradient(circle at 20% 80%, rgba(248, 196, 196, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(248, 196, 196, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(248, 196, 196, 0.05) 0%, transparent 50%);
        background-attachment: fixed;
    }
    
    /* Streamlit 主容器 */
    .css-18e3th9 {
        background-color: #fff9e6 !important;
    }
    
    /* 主内容区域 */
    .css-1d391kg {
        background-color: #fff9e6 !important;
        border-right: 1px solid #f8e0e6;
    }
    
    /* 侧边栏 */
    .css-1lcbmhc {
        background-color: #fff9e6 !important;
    }
    
    /* 卡片容器 */
    .css-1v0mbdj {
        background-color: #fff9e6 !important;
    }
    
    /* 标题样式 */
    h1 {
        color: #e68a8a;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 1px 1px 2px rgba(230, 138, 138, 0.1);
        animation: fadeInDown 1s ease-out;
        position: relative;
    }
    
    h1::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 100px;
        height: 4px;
        background: linear-gradient(90deg, transparent, #e68a8a, transparent);
        border-radius: 2px;
        animation: slideIn 1.5s ease-out 0.5s both;
    }
    
    h2 {
        color: #f8b4b4;
        font-weight: 600;
        animation: fadeInUp 1s ease-out 0.2s both;
        position: relative;
    }
    
    h2::before {
        content: '✨';
        margin-right: 8px;
        animation: bounce 2s infinite;
    }
    
    /* 卡片样式 */
    .feature-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef5f7 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05), 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        border-left: 4px solid #f8c4c4;
        animation: fadeInUp 1s ease-out forwards;
        opacity: 0;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(248, 196, 196, 0.2), transparent);
        transition: left 0.6s ease;
    }
    
    .feature-card::after {
        content: '';
        position: absolute;
        bottom: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(
            45deg,
            transparent 30%,
            rgba(248, 196, 196, 0.1) 50%,
            transparent 70%
        );
        border-radius: 40%;
        animation: wave 8s linear infinite;
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    
    .feature-card:hover::before {
        left: 100%;
    }
    
    .feature-card:hover::after {
        opacity: 1;
    }
    
    .feature-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 16px 32px rgba(0, 0, 0, 0.1), 0 8px 16px rgba(0, 0, 0, 0.05);
    }
    
    /* 按钮样式 */
    .stButton>button {
        background: linear-gradient(135deg, #f8c4c4 0%, #e68a8a 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        animation: pulse 2s infinite;
        position: relative;
        overflow: hidden;
        margin-top: 16px;
    }
    
    .stButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stButton>button:active::before {
        width: 300px;
        height: 300px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #e68a8a 0%, #d47a7a 100%);
        transform: translateY(-4px) scale(1.05);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
    }
    
    /* 结果卡片样式 */
    .result-card {
        background: linear-gradient(135deg, #ffffff 0%, #fef5f7 100%);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.05);
        margin-top: 24px;
        border: 1px solid #f8e0e6;
        animation: fadeIn 1s ease-out;
        position: relative;
    }
    
    .result-card::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f8c4c4, #e68a8a, #f8c4c4);
        border-radius: 16px 16px 0 0;
    }
    
    /* 滑块样式 */
    .css-1cpxqw2 {
        accent-color: #f8c4c4;
        transition: all 0.3s ease;
    }
    
    .css-1cpxqw2:hover {
        accent-color: #e68a8a;
    }
    
    /* 输入框样式 */
    .css-1x8cf1d {
        border-radius: 10px;
        border: 1px solid #f8e0e6;
        background-color: #ffffff;
        transition: all 0.3s ease;
        position: relative;
    }
    
    .css-1x8cf1d:focus {
        border-color: #e68a8a;
        box-shadow: 0 0 0 3px rgba(230, 138, 138, 0.1);
        transform: translateY(-2px);
    }
    
    /* 选择框样式 */
    .css-1gak4zt {
        border-radius: 10px;
        border: 1px solid #f8e0e6;
        background-color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .css-1gak4zt:focus {
        border-color: #e68a8a;
        box-shadow: 0 0 0 3px rgba(230, 138, 138, 0.1);
        transform: translateY(-2px);
    }
    
    /* 下载按钮样式 */
    .stDownloadButton>button {
        background: linear-gradient(135deg, #e68a8a 0%, #f8c4c4 100%);
        color: white;
        border-radius: 10px;
        border: none;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .stDownloadButton>button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        background: rgba(255, 255, 255, 0.3);
        border-radius: 50%;
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }
    
    .stDownloadButton>button:active::before {
        width: 300px;
        height: 300px;
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #f8c4c4 0%, #f8d4d4 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* 文本区域样式 */
    .stTextArea>div>textarea {
        border-radius: 10px;
        border: 1px solid #f8e0e6;
        background-color: #ffffff;
        transition: all 0.3s ease;
    }
    
    .stTextArea>div>textarea:focus {
        border-color: #e68a8a;
        box-shadow: 0 0 0 3px rgba(230, 138, 138, 0.1);
        transform: translateY(-2px);
    }
    
    /* 标题区域样式 */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #fff9e6 0%, #fef5f7 100%);
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        animation: fadeIn 1.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: 
            radial-gradient(circle at 20% 20%, rgba(248, 196, 196, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(248, 196, 196, 0.1) 0%, transparent 50%);
        z-index: 0;
    }
    
    .main-header * {
        position: relative;
        z-index: 1;
    }
    
    /* 加载动画样式 */
    .loading-animation {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(248, 196, 196, 0.3);
        border-radius: 50%;
        border-top-color: #e68a8a;
        animation: spin 1s ease-in-out infinite;
    }
    
    /* 增强的加载动画 */
    .loading-container {
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
    }
    
    .loading-spinner {
        width: 40px;
        height: 40px;
        border: 4px solid rgba(248, 196, 196, 0.3);
        border-top: 4px solid #e68a8a;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin-right: 12px;
    }
    
    /* 动画关键帧 */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes pulse {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            transform: scale(1);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    @keyframes slideIn {
        from {
            width: 0;
            opacity: 0;
        }
        to {
            width: 100px;
            opacity: 1;
        }
    }
    
    @keyframes ripple {
        0% {
            transform: scale(0);
            opacity: 1;
        }
        100% {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes wave {
        0% {
            transform: rotate(0deg);
        }
        100% {
            transform: rotate(360deg);
        }
    }
    
    /* 侧边栏标题 */
    .css-163ttbj {
        color: #e68a8a;
        animation: fadeIn 1s ease-out 0.5s both;
        position: relative;
    }
    
    .css-163ttbj::after {
        content: '';
        position: absolute;
        bottom: -5px;
        left: 0;
        width: 50px;
        height: 2px;
        background: #e68a8a;
        border-radius: 1px;
        animation: slideIn 1s ease-out 1s both;
    }
    
    /* 侧边栏选项 */
    .css-1dimb5e {
        color: #f8b4b4;
        transition: all 0.3s ease;
        position: relative;
        padding-left: 10px;
    }
    
    .css-1dimb5e::before {
        content: '➤';
        position: absolute;
        left: -10px;
        opacity: 0;
        transition: all 0.3s ease;
    }
    
    .css-1dimb5e:hover {
        color: #e68a8a;
        transform: translateX(10px);
    }
    
    .css-1dimb5e:hover::before {
        left: 0;
        opacity: 1;
    }
    
    /* 侧边栏滑块标签 */
    .css-10trblm {
        color: #f8b4b4;
        transition: all 0.3s ease;
    }
    
    .css-10trblm:hover {
        color: #e68a8a;
    }
    
    /* 错误信息样式 */
    .css-1xarl3l {
        background-color: #fef5f7;
        border-left: 4px solid #f8c4c4;
        animation: fadeIn 0.5s ease-out;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 成功信息样式 */
    .css-q8sbsg {
        background-color: #f5fef5;
        border-left: 4px solid #b4f8b4;
        animation: fadeIn 0.5s ease-out;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 警告信息样式 */
    .css-1n76uvr {
        background-color: #fef5f5;
        border-left: 4px solid #f8d4b4;
        animation: fadeIn 0.5s ease-out;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 信息样式 */
    .css-1adrfps {
        background-color: #f5f7fe;
        border-left: 4px solid #b4c8f8;
        animation: fadeIn 0.5s ease-out;
        border-radius: 8px;
        padding: 16px;
        margin: 10px 0;
    }
    
    /* 滚动条样式 */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #fff9e6;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #f8c4c4;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #e68a8a;
        transform: scale(1.1);
    }
    
    /* 卡片动画延迟 */
    .feature-card:nth-child(1) {
        animation-delay: 0.3s;
    }
    
    .feature-card:nth-child(2) {
        animation-delay: 0.6s;
    }
    
    .feature-card:nth-child(3) {
        animation-delay: 0.9s;
    }
    
    /* 响应式设计 */
    @media (max-width: 768px) {
        .feature-card {
            margin-bottom: 16px;
        }
        
        h1 {
            font-size: 1.8rem;
        }
        
        h2 {
            font-size: 1.4rem;
        }
    }
    
    /* 页面过渡动画 */
    .stApp {
        transition: all 0.5s ease;
    }
    
    /* 工具提示样式 */
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 200px;
        background-color: #e68a8a;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 8px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------- 全局状态管理 ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "ark_client" not in st.session_state:
    st.session_state.ark_client = None
if "model_id" not in st.session_state:
    st.session_state.model_id = None

# ---------------------- 渲染首页 ----------------------
def render_home_page():
    """渲染首页：核心功能展示"""
    # 主标题区域
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🎯 自动控制原理学习助手")
    st.markdown("### 智能学习平台 | AI出题+考点解析+系统分析+学习辅助")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # 4个横向排列
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class='feature-card' style='min-height: 180px;'>
            <h3 style='color: #e68a8a; margin-bottom: 1rem; font-size: 1.1rem;'>AI智能出题</h3>
            <p style='font-size: 0.85rem;'>• 专项练习</p>
            <p style='font-size: 0.85rem;'>• 整卷模拟测试</p>
            <p style='font-size: 0.85rem;'>• 智能难度调整...</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("开始出题", key="exam_button"):
            st.session_state.page = "exam"
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class='feature-card' style='min-height: 180px;'>
            <h3 style='color: #e68a8a; margin-bottom: 1rem; font-size: 1.1rem;'>系统分析工具</h3>
            <p style='font-size: 0.85rem;'>• 根轨迹分析</p>
            <p style='font-size: 0.85rem;'>• 伯德图分析</p>
            <p style='font-size: 0.85rem;'>• 二阶系统分析...</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("系统分析", key="analysis_button"):
            st.session_state.page = "analysis"
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class='feature-card' style='min-height: 180px;'>
            <h3 style='color: #e68a8a; margin-bottom: 1rem; font-size: 1.1rem;'>考研答疑</h3>
            <p style='font-size: 0.85rem;'>• 知识点解析</p>
            <p style='font-size: 0.85rem;'>• 真题解答</p>
            <p style='font-size: 0.85rem;'>• 学习规划...</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("开始答疑", key="qa_button"):
            st.session_state.page = "qa"
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class='feature-card' style='min-height: 180px;'>
            <h3 style='color: #e68a8a; margin-bottom: 1rem; font-size: 1.1rem;'>学习辅助</h3>
            <p style='font-size: 0.85rem;'>• 基础概念模块</p>
            <p style='font-size: 0.85rem;'>• 二阶系统模块</p>
            <p style='font-size: 0.85rem;'>• 稳定性判据模块...</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
        if st.button("开始学习", key="learning_button"):
            st.session_state.page = "learning"
        st.markdown("</div>", unsafe_allow_html=True)
    
    # 底部信息区域
    st.markdown("""
    <div style='margin-top: 3rem; text-align: center; padding: 2rem; background: linear-gradient(135deg, #fff9e6 0%, #fef5f7 100%); border-radius: 16px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);'>
        <h3 style='color: #e68a8a; margin-bottom: 1rem;'>✨ 功能特色</h3>
        <p style='color: #666; margin-bottom: 1.5rem;'>基于AI技术的智能学习平台，为自动控制原理学习者提供全方位的学习支持</p>
        <div style='display: flex; justify-content: center; gap: 2rem; flex-wrap: wrap;'>
            <div style='text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>🎯</div>
                <div style='color: #f8b4b4; font-weight: 600;'>精准出题</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📈</div>
                <div style='color: #f8b4b4; font-weight: 600;'>系统分析</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>💡</div>
                <div style='color: #f8b4b4; font-weight: 600;'>智能答疑</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📚</div>
                <div style='color: #f8b4b4; font-weight: 600;'>学习辅助</div>
            </div>
            <div style='text-align: center;'>
                <div style='font-size: 2rem; margin-bottom: 0.5rem;'>📄</div>
                <div style='color: #f8b4b4; font-weight: 600;'>Word导出</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ---------------------- 渲染出卷页面 ----------------------
def render_exam_page():
    """渲染AI出卷页面"""
    st.title("🤖 AI智能出题")
    
    # 出题配置
    st.sidebar.header("出题配置")
    mode = st.sidebar.selectbox(
        "出题模式",
        ["专项练习", "整卷模拟测试"]
    )
    
    if mode == "专项练习":
        scope = st.sidebar.selectbox(
            "专项考点",
            ["根轨迹分析", "伯德图分析", "二阶系统分析", "PID校正", "稳态误差计算", "综合应用题"]
        )
        num = st.sidebar.slider("题目数量", 1, 10, 5)
    else:
        scope = "整卷"
        num = None
    
    # 生成题目
    if st.button("生成题目", key="generate_paper"):
        # 使用容器来隔离UI元素，避免DOM冲突
        with st.container():
            try:
                start_time = time.time()
                status_placeholder = st.empty()
                status_placeholder.info("AI正在生成高质量题目...（优化后<10秒）")
                
                questions, answers = generate_ai_exam_paper(mode, scope, num)
                
                end_time = time.time()
                status_placeholder.success(f"✅ 题目生成完成！耗时：{end_time - start_time:.2f}秒")
                
                # 只显示题目，不显示参考答案
                for i, q in enumerate(questions, 1):
                    st.markdown(f"### 题目 {i}")
                    st.markdown(q)
                    st.markdown("---")
                
                # 导出到Word文档
                try:
                    # 确定是否为整卷模式
                    is_full_exam = (mode == "整卷模拟测试")
                    
                    # 生成Word文档数据
                    word_data = get_word_download_data(questions, answers, is_full_exam)
                    
                    if word_data:
                        # 提供下载按钮
                        filename = "控制原理学习资料.docx"
                        st.download_button(
                            label="📥 下载Word题目",
                            data=word_data,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        st.success("✅ Word文档已生成，点击上方按钮下载")
                    else:
                        st.error("❌ Word文档生成失败，请重试")
                except Exception as e:
                    st.error(f"❌ 文档处理失败：{str(e)}")
            except Exception as e:
                st.error(f"❌ 生成题目失败：{str(e)}")
    
    # 返回首页
    if st.button("返回首页", key="back_to_home"):
        st.session_state.page = "home"

# ---------------------- 渲染系统分析页面 ----------------------
def render_analysis_page():
    """渲染系统分析工具页面"""
    # 正常显示系统分析
    st.title("📊 系统分析工具")
    
    # 分析类型选择
    analysis_type = st.sidebar.selectbox(
        "分析类型",
        ["根轨迹分析", "伯德图分析", "二阶系统分析", "PID校正分析", "稳态误差计算"]
    )
    
    # 传递函数输入
    st.sidebar.header("传递函数输入")
    num_input = st.sidebar.text_input("分子多项式系数（空格分隔）", "1")
    den_input = st.sidebar.text_input("分母多项式系数（空格分隔）", "1 3 2")
    
    # 解析传递函数
    try:
        num = list(map(float, num_input.split()))
        den = list(map(float, den_input.split()))
    except:
        st.error("传递函数输入格式错误，请输入空格分隔的数字")
        return
    
    # 开环增益
    K = st.sidebar.number_input("开环增益 K", value=1.0, min_value=0.1, max_value=100.0, step=0.1)
    
    # PID参数输入 - 移到外面，选择PID校正分析时就显示
    Kp = None
    Ki = None
    Kd = None
    pid_input_type = None
    if analysis_type == "PID校正分析":
        st.sidebar.header("PID参数")
        pid_input_type = st.sidebar.selectbox(
            "输入类型",
            ["单位阶跃输入 1(t)", "单位斜坡输入 r(t)=t", "单位抛物线输入 r(t)=0.5t²"],
            index=0
        )
        Kp = st.sidebar.number_input("比例系数 Kp", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
        Ki = st.sidebar.number_input("积分系数 Ki", value=0.0, min_value=0.0, max_value=5.0, step=0.1)
        Kd = st.sidebar.number_input("微分系数 Kd", value=0.0, min_value=0.0, max_value=5.0, step=0.1)
    
    # 稳态误差计算参数
    input_type = None
    A = None
    if analysis_type == "稳态误差计算":
        st.sidebar.header("输入信号参数")
        input_type = st.sidebar.selectbox(
            "输入类型",
            ["阶跃输入 1(t)", "斜坡输入 t", "抛物线输入 0.5t²", "正弦输入 sin(ωt)", "余弦输入 cos(ωt)"]
        )
        A = st.sidebar.number_input("输入幅值 A", value=1.0, min_value=0.1, max_value=10.0, step=0.1)
    
    # 执行分析
    if st.button("开始分析", key="start_analysis"):
        if analysis_type == "根轨迹分析":
            plot_root_locus(num, den, K)
        elif analysis_type == "伯德图分析":
            plot_bode_diagram(num, den, K)
        elif analysis_type == "二阶系统分析":
            calculate_second_order_params(num, den, K)
        elif analysis_type == "PID校正分析":
            plot_pid_step_response(None, num, den, K, Kp, Ki, Kd, pid_input_type)
        elif analysis_type == "稳态误差计算":
            calculate_steady_error(num, den, K, input_type, A)
    
    # 返回首页
    if st.button("返回首页", key="back_to_home_analysis"):
        st.session_state.page = "home"

# ---------------------- 渲染考研答疑页面 ----------------------
def render_qa_page():
    """渲染考研答疑页面"""
    st.title("❓ 考研答疑")
    
    # 问题输入
    question = st.text_area("请输入您的问题（例如：如何计算根轨迹的渐近线？）", height=150)
    
    if st.button("提交问题", key="submit_question"):
        if question:
            st.info("AI正在思考...")
            # 调用AI问答功能
            from functions import get_volc_ai_answer_stream, ensure_latex_format
            st.success("✅ 问题已提交，AI正在处理...")
            
            # 先收集完整回答
            full_answer = ""
            for chunk in get_volc_ai_answer_stream(question):
                full_answer += chunk
            
            # 对完整回答进行LaTeX格式化
            formatted_answer = ensure_latex_format(full_answer)
            
            # 显示格式化后的回答（用st.markdown确保LaTeX正确渲染）
            st.markdown("**AI回答：**")
            st.markdown(formatted_answer)
        else:
            st.error("请输入问题")
    
    # 返回首页
    if st.button("返回首页", key="back_to_home_qa"):
        st.session_state.page = "home"

# ---------------------- 渲染学习辅助页面 ----------------------
def render_learning_page():
    """渲染学习辅助页面"""
    st.title("📚 控制原理知识点库")
    
    # 侧边栏：知识点类型选择
    from functions import KNOWLEDGE_CONTENT
    module_list = list(KNOWLEDGE_CONTENT.keys())
    selected_module = st.sidebar.selectbox("知识点类型", module_list)
    
    # 侧边栏底部：返回首页按钮
    st.sidebar.markdown("---")
    if st.sidebar.button("🏠 返回首页", key="back_to_home_sidebar", use_container_width=True):
        st.session_state.page = "home"
    
    # 右边展示完整内容 - 修复LaTeX渲染
    if selected_module in KNOWLEDGE_CONTENT:
        module_data = KNOWLEDGE_CONTENT[selected_module]
        content = module_data["content"]
        
        # 清理HTML标签，保留LaTeX
        import re
        
        def clean_html_tags(text):
            """移除HTML标签，保留LaTeX内容"""
            # 移除div标签
            text = re.sub(r'<div[^>]*>', '', text)
            text = re.sub(r'</div>', '', text)
            # 移除h2标签
            text = re.sub(r'<h2[^>]*>', '## ', text)
            text = re.sub(r'</h2>', '', text)
            # 移除h3标签
            text = re.sub(r'<h3[^>]*>', '### ', text)
            text = re.sub(r'</h3>', '', text)
            # 移除p标签
            text = re.sub(r'<p[^>]*>', '', text)
            text = re.sub(r'</p>', '', text)
            # 移除strong标签
            text = re.sub(r'<strong[^>]*>', '**', text)
            text = re.sub(r'</strong>', '**', text)
            # 移除br标签
            text = re.sub(r'<br[^>]*>', '\n', text)
            # 移除hr标签
            text = re.sub(r'<hr[^>]*>', '---', text)
            # 移除其他标签
            text = re.sub(r'<[^>]+>', '', text)
            return text
        
        # 清理内容
        clean_content = clean_html_tags(content)
        
        # 直接渲染清理后的内容
        st.markdown(clean_content)

# ---------------------- 主函数 ----------------------
def main():
    """主函数：页面路由"""
    # 初始化AI客户端
    init_ark_client_once()
    
    # 页面路由
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "exam":
        render_exam_page()
    elif st.session_state.page == "analysis":
        render_analysis_page()
    elif st.session_state.page == "qa":
        render_qa_page()
    elif st.session_state.page == "learning":
        render_learning_page()

if __name__ == "__main__":
    main()