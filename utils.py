import os
import json

DATA_DIR = "data"
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# 确保 data 目录存在
os.makedirs(DATA_DIR, exist_ok=True)


def save_uploaded_file(uploaded_file, file_name):
    """保存上传的文件到 data/ 目录"""
    file_path = os.path.join(DATA_DIR, file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # 如果文件已存在，则不覆盖
    if not os.path.exists(file_path):
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

    return file_path


def save_history(record):
    """保存一条历史记录"""
    history = load_history()
    history.append(record)
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)


def load_history():
    """读取历史记录"""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
