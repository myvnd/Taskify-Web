import os
import json
import tempfile
import shutil

# ============================================================
# 1. XÁC ĐỊNH THƯ MỤC GỐC DỰ ÁN (PROJECT ROOT)
# ------------------------------------------------------------
# - __file__  →  đường dẫn tuyệt đối đến file functions.py
# - dirname  →  đi lên 1 cấp tới thư mục /core
# - dirname lần 2 → lên thư mục gốc /Taskify
# ============================================================

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ============================================================
# 2. THƯ MỤC LƯU TRỮ DỮ LIỆU: /Taskify/data
# ------------------------------------------------------------
# - Tạo thư mục nếu chưa tồn tại
# - Giữ dữ liệu trong project → dễ debug, dễ deploy Streamlit
# ============================================================

DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# ============================================================
# 3. FILE LƯU DANH SÁCH TASK
# ============================================================

TASK_FILE = os.path.join(DATA_DIR, "task-list.json")


# ============================================================
# 4. HÀM ĐỌC DANH SÁCH TASK
# ------------------------------------------------------------
# - Nếu file không tồn tại → trả về list rỗng
# - Đọc từng dòng → strip newline (\n)
# ============================================================

def get_task_list():
    """
    Read task list from data/task-list.json (list of dict objects).
    """
    if not os.path.exists(TASK_FILE):
        return []

    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[ERROR] Cannot read task list: {e}")
        return []


# ============================================================
# 5. HÀM GHI DANH SÁCH TASK (AN TOÀN)
# ------------------------------------------------------------
# - Ghi ra file tạm trước (atomic write)
# - Sau đó replace file cũ → tránh mất dữ liệu nếu crash
# ============================================================

def write_task_list(task_list):
    """
    Write list of dict tasks to task-list.json using atomic write.
    """
    try:
        # Ghi vào file tạm
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
            json.dump(task_list, tmp, indent=4, ensure_ascii=False)
            temp_name = tmp.name

        # Replace file cũ
        shutil.move(temp_name, TASK_FILE)

    except Exception as e:
        print(f"[ERROR] Cannot write task list: {e}")