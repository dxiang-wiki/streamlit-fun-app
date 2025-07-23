import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.font_manager import FontProperties
import random
import time
from datetime import datetime

# 设置中文字体
import matplotlib.font_manager as fm

# 获取已安装的中文字体
chinese_fonts = [f.name for f in fm.fontManager.ttflist if 'Hei' in f.name or 'YaHei' in f.name or 'WenQuanYi' in f.name]

if chinese_fonts:
    plt.rcParams['font.sans-serif'] = chinese_fonts
    print(f"使用中文字体: {chinese_fonts}")
else:
    print("警告: 未找到中文字体，将使用默认字体")

plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 设置全局字体大小
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# 设置页面配置
st.set_page_config(
    page_title="趣味数据应用",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 页面标题和描述
st.title("趣味数据应用")
st.markdown("这是一个使用Streamlit开发的趣味应用，展示了数据可视化、小游戏和实用工具等功能。")


# 模拟数据生成函数
@st.cache_data
def generate_data(n=100):
    """生成模拟数据"""
    np.random.seed(42)
    df = pd.DataFrame({
        '日期': pd.date_range(start='2023-01-01', periods=n),
        '销售额': np.random.normal(1000, 200, n),
        '访问量': np.random.randint(100, 1000, n),
        '转化率': np.random.uniform(0.01, 0.1, n),
        'Region': random.choices(['East', 'South', 'North', 'West', 'Northwest'], k=n)
    })
    return df


# 侧边栏导航
with st.sidebar:
    st.header("导航")
    page = st.radio("选择页面", [
        "数据概览",
        "销售分析",
        "小游戏",
        "实用工具",
        "联系我们"
    ])

# 初始化变量
region = []
date_range = []

st.divider()
st.header("参数设置")
if page == "销售分析":
    region = st.multiselect("选择地区", ['华东', '华南', '华北', '西南', '西北'], ['华东', '华南'])
    date_range = st.date_input(
        "选择日期范围",
        [datetime(2023, 1, 1), datetime(2023, 4, 10)],
        min_value=datetime(2023, 1, 1),
        max_value=datetime(2023, 4, 10)
    )

# 主内容区域
if page == "数据概览":
    # 显示数据表格
    st.subheader("数据概览")
    df = generate_data()
    st.dataframe(df.head(20), use_container_width=True)

    # 数据统计信息
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Avg Sales", f"{df['Sales'].mean():.2f}")
    with col2:
        st.metric("Max Visits", df['Visits'].max())
    with col3:
        st.metric("Avg Rate", f"{df['Rate'].mean() * 100:.2f}%")

    # 简单图表
    st.subheader("数据趋势")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(df['日期'], df['销售额'], label='销售额')
    ax.set_xlabel('日期')
    ax.set_ylabel('销售额')
    ax.legend()
    st.pyplot(fig)

elif page == "销售分析":
    # 筛选数据
    df = generate_data()
    filtered_df = df[
        (df['地区'].isin(region)) &
        (df['日期'] >= pd.Timestamp(date_range[0])) &
        (df['日期'] <= pd.Timestamp(date_range[1]))
        ]

    # 分析结果
    st.subheader("销售分析")
    st.write(f"筛选条件：地区={region}，日期范围={date_range[0]}至{date_range[1]}")

    # 图表展示
    col1, col2 = st.columns(2)
    with col1:
        st.write("销售额趋势")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(filtered_df['日期'], filtered_df['销售额'])
        ax.set_xlabel('日期')
        ax.set_ylabel('销售额')
        st.pyplot(fig)

    with col2:
        st.write("地区分布")
        fig, ax = plt.subplots(figsize=(8, 4))
        region_counts = filtered_df['地区'].value_counts()
        ax.bar(region_counts.index, region_counts.values)
        ax.set_xlabel('地区')
        ax.set_ylabel('数量')
        st.pyplot(fig)

    # 数据表格
    st.write("详细数据")
    st.dataframe(filtered_df, use_container_width=True)

elif page == "小游戏":
    st.subheader("猜数字游戏")
    st.write("我想了一个1到100之间的数字，你能猜出来吗？")

    # 初始化会话状态
    if 'number' not in st.session_state:
        st.session_state.number = random.randint(1, 100)
    if 'attempts' not in st.session_state:
        st.session_state.attempts = 0
    if 'guesses' not in st.session_state:
        st.session_state.guesses = []

    # 游戏界面
    guess = st.number_input("请输入你的猜测", min_value=1, max_value=100, step=1)
    if st.button("猜"):
        st.session_state.attempts += 1
        st.session_state.guesses.append(guess)

        if guess < st.session_state.number:
            st.warning("太小了！再大一点...")
        elif guess > st.session_state.number:
            st.warning("太大了！再小一点...")
        else:
            st.success(f"恭喜你，猜对了！答案就是{st.session_state.number}")
            st.balloons()
            st.write(f"你用了{st.session_state.attempts}次尝试")

            # 重置游戏
            st.session_state.number = random.randint(1, 100)
            st.session_state.attempts = 0
            st.session_state.guesses = []

    # 显示历史猜测
    if st.session_state.guesses:
        st.write("历史猜测：", st.session_state.guesses)

elif page == "实用工具":
    st.subheader("文件上传与分析")

    # 文件上传
    uploaded_file = st.file_uploader("上传CSV文件", type=["csv"])

    if uploaded_file is not None:
        # 读取数据
        data = pd.read_csv(uploaded_file)

        # 显示数据信息
        st.write("数据基本信息：")
        st.write(data.describe())  # 更适合 Streamlit 展示

        # 显示数据集行数和列数
        rows, columns = data.shape

        if rows > 0 and columns > 0:
            # 显示数据前几行
            st.write("数据前几行内容信息：")
            st.dataframe(data.head())  # 直接传入 DataFrame

            # 选择列进行分析
            selected_column = st.selectbox("选择一列进行分析", data.columns)

            # 显示列统计信息
            st.write(f"列 '{selected_column}' 的统计信息：")
            st.dataframe(data[selected_column].describe())  # 直接传入 DataFrame

            # 绘制直方图
            st.write(f"列 '{selected_column}' 的直方图：")
            fig, ax = plt.subplots()
            ax.hist(data[selected_column].dropna(), bins=20)
            ax.set_xlabel(selected_column)
            ax.set_ylabel('频次')
            st.pyplot(fig)
    else:
        st.info("请上传一个CSV文件进行分析")

elif page == "联系我们":
    st.subheader("联系我们")
    st.write("感谢使用我们的应用！如果你有任何问题或建议，请通过以下方式联系我们：")

    # 联系表单
    with st.form("contact_form"):
        name = st.text_input("姓名", key="contact_name")
        email = st.text_input("邮箱", key="contact_email")
        message = st.text_area("留言内容", key="contact_message")

        submitted = st.form_submit_button("提交")
        if submitted:
            # 模拟处理表单
            with st.spinner("提交中..."):
                time.sleep(2)
            st.success("提交成功！我们会尽快回复你。")
            # 清空表单
            st.session_state.contact_name = ""
            st.session_state.contact_email = ""
            st.session_state.contact_message = ""

    # 联系信息
    st.write("你也可以通过以下方式联系我们：")
    st.write("- 邮箱：support@example.com")
    st.write("- 电话：+86 123 4567 8910")
    st.write("- 地址：北京市朝阳区科技园A座")