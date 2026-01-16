import streamlit as st
import core.functions as functions


# ============================================================
# ADD TASK
# ============================================================
def add_task():
    new_task = st.session_state.get("new_task", "").strip()
    if not new_task:
        return

    task_list = functions.get_task_list()
    task_list.append({
        "task": new_task,
        "status": "pending"
    })

    functions.write_task_list(task_list)


# ============================================================
# EDIT TASK
# ============================================================
def edit_task(index, new_text):
    task_list = functions.get_task_list()

    if 0 <= index < len(task_list):
        task_list[index]["task"] = new_text.strip()
        functions.write_task_list(task_list)


# ============================================================
# DELETE TASK
# ============================================================
def delete_task(index):
    task_list = functions.get_task_list()

    if 0 <= index < len(task_list):
        task_list.pop(index)
        functions.write_task_list(task_list)

    # Clean edit state
    if st.session_state.get("edit_index") == index:
        st.session_state.pop("edit_index", None)
        st.session_state.pop("edit_text", None)

    elif st.session_state.get("edit_index", -1) > index:
        st.session_state["edit_index"] -= 1


# ============================================================
# UPDATE STATUS
# ============================================================

def update_status(index, new_status):
    task_list = functions.get_task_list()

    if 0 <= index < len(task_list):
        task_list[index]["status"] = new_status
        functions.write_task_list(task_list)


# ============================================================
# LOAD CSS
# ============================================================

def load_css(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def start_edit(index, text):
    st.session_state.edit_index = index
    st.session_state.edit_text = text
