import streamlit as st
from datetime import datetime
from utils import save_uploaded_file, save_history, load_history
import pandas as pd
import io
import os

st.set_page_config(page_title="文件计算网页", layout="wide")

# -----------------
# 初始化 session_state
# -----------------
if "mode" not in st.session_state:
    st.session_state.mode = "main"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None
if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None
if "input_numbers" not in st.session_state:
    st.session_state.input_numbers = [0.0, 0.0, 0.0]
if "calculation_result" not in st.session_state:
    st.session_state.calculation_result = None
if "selected_history_idx" not in st.session_state:
    st.session_state.selected_history_idx = None

# -----------------
# 侧边栏
# -----------------
st.sidebar.title("操作")

uploaded_file = st.sidebar.file_uploader("上传文件", key="uploader")
if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    st.session_state.uploaded_file_name = uploaded_file.name

if st.sidebar.button("历史记录"):
    st.session_state.mode = "history"
    st.session_state.selected_history_idx = None

# -----------------
# 页面主占位符
# -----------------
placeholder = st.empty()

# -----------------
# 历史界面
# -----------------
with placeholder.container():
    if st.session_state.mode == "history":
        st.title("历史记录")
        history = load_history()

        if history:
            options = [
                f"{idx+1}: {record['timestamp']}" for idx, record in enumerate(history)
            ]
            default_index = st.session_state.selected_history_idx or 0
            selected = st.selectbox(
                "选择历史记录查看元数据", options, index=default_index
            )
            st.session_state.selected_history_idx = options.index(selected)

            record = history[st.session_state.selected_history_idx]
            st.subheader("历史记录元数据")
            st.json(record)

            if st.button("使用历史记录回主界面"):
                st.session_state.mode = "main"
                st.session_state.input_numbers = record["numbers"]
                st.session_state.calculation_result = sum(record["numbers"])

                # 复用上传文件
                try:
                    if os.path.exists(record["file_path"]):
                        with open(record["file_path"], "rb") as f:
                            st.session_state.uploaded_file = io.BytesIO(f.read())
                        st.session_state.uploaded_file_name = os.path.basename(
                            record["file_path"]
                        )
                    else:
                        st.session_state.uploaded_file = None
                        st.session_state.uploaded_file_name = None
                except:
                    st.session_state.uploaded_file = None
                    st.session_state.uploaded_file_name = None

                st.session_state.selected_history_idx = None
                placeholder.empty()  # 清空历史界面占位符
        else:
            st.info("暂无历史记录")

# -----------------
# 主界面
# -----------------
if st.session_state.mode == "main":
    st.title("计算页面")

    # 文件显示
    if st.session_state.uploaded_file:
        st.write(f"已上传文件: {st.session_state.uploaded_file_name}")

        try:
            content = st.session_state.uploaded_file.read()
            if hasattr(st.session_state.uploaded_file, "seek"):
                st.session_state.uploaded_file.seek(0)

            # 尝试文本显示
            try:
                text_content = content.decode("utf-8")
                st.text_area("文件内容预览", text_content, height=200)
            except:
                # 尝试解析为 CSV
                try:
                    df = pd.read_csv(io.BytesIO(content))
                    st.dataframe(df.head())
                except:
                    st.info("文件无法解析为文本或表格，显示为二进制")
        except Exception as e:
            st.error(f"显示文件内容失败: {e}")
    else:
        st.write("尚未上传文件")

    # 数字输入
    col1, col2, col3 = st.columns(3)
    num1 = col1.number_input(
        "数字1", value=st.session_state.input_numbers[0], format="%.4f", key="num1"
    )
    num2 = col2.number_input(
        "数字2", value=st.session_state.input_numbers[1], format="%.4f", key="num2"
    )
    num3 = col3.number_input(
        "数字3", value=st.session_state.input_numbers[2], format="%.4f", key="num3"
    )
    st.session_state.input_numbers = [num1, num2, num3]

    # 自动计算
    st.session_state.calculation_result = sum(st.session_state.input_numbers)
    st.write("计算结果:", st.session_state.calculation_result)

    # 保存按钮（primary + 去重 + 文件已存在判断）
    if st.button("保存", type="primary"):
        if st.session_state.uploaded_file_name is None:
            st.warning("请先上传文件再保存！")
        else:
            file_name = st.session_state.uploaded_file_name
            input_numbers_rounded = [
                round(n, 4) for n in st.session_state.input_numbers
            ]

            history = load_history()
            exists = False

            for record in history:
                record_file_name = os.path.basename(record.get("file_path", ""))
                record_numbers = [round(n, 4) for n in record.get("numbers", [])]
                if (
                    record_file_name == file_name
                    and record_numbers == input_numbers_rounded
                ):
                    exists = True
                    break

            if exists:
                st.warning("已保存过同样的记录，请到历史记录页面查看！")
            else:
                # 保存文件到 data/，如果已存在则不覆盖
                uploaded_file = st.session_state.uploaded_file
                file_path = save_uploaded_file(uploaded_file, file_name)
                file_size = os.path.getsize(file_path)

                record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "file_path": file_path,
                    "file_size": file_size,
                    "numbers": input_numbers_rounded,
                    "result": st.session_state.calculation_result,
                }
                save_history(record)
                st.success("保存成功！")
