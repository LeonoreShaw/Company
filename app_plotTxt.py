import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="centered")
st.title("📈 多 txt 文件曲线叠加与可选显示")

# 侧边栏
with st.sidebar:
    # 1️⃣ 上传多个 txt
    uploaded_files = st.file_uploader(
        "上传多个 txt 文件（两列数据）", type="txt", accept_multiple_files=True
    )

# 用字典存每个文件对应的 DataFrame
dfs = {}

# ===============================
# 2️⃣ 读取 + 转置 + 折叠显示
# ===============================
if uploaded_files:

    for file in uploaded_files:
        df = pd.read_csv(
            file,
            sep=r"\s+",
            header=None,
            names=["x", "y"]
        )

        # 转置：x/y 作为行
        df_t = df.T
        df_t.index = ["x", "y"]

        dfs[file.name] = df


# ===============================
# 3️⃣ 多选：控制显示哪些曲线
# ===============================
selected_files = st.multiselect(
    "选择要显示的曲线",
    options=list(dfs.keys()),
    default=list(dfs.keys())
)

# ===============================
# 4️⃣ 画图
# ===============================
fig = go.Figure()

for file_name, df in dfs.items():
    fig.add_trace(
        go.Scatter(
            x=df["x"],
            y=df["y"],
            mode="markers",
            name=file_name,
            visible=file_name in selected_files
        )
    )

fig.update_layout(
    title="多 txt 文件折线图（可选显示）",
    xaxis_title="X",
    yaxis_title="Y",
    template="plotly_white",
    # legend=dict(
    #     orientation="h",
    #     yanchor="top",
    #     y=-0.25,
    #     xanchor="center",
    #     x=0.5
    # )
)

if dfs:
    st.plotly_chart(fig, use_container_width=True)
    st.subheader("📄 原始数据")
    for file in uploaded_files:
        # 折叠显示
        with st.expander(f"原始数据：{file.name}", expanded=False):
            st.dataframe(df_t, use_container_width=True)

else:
    st.info("请上传 txt 文件")
