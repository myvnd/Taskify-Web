import sys
import os
import streamlit as st


# ==================================================================
# 1. PROJECT ROOT
# ==================================================================

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import functions
from core.app import (
    add_task,
    edit_task,
    delete_task,
    update_status,
    load_css,
    start_edit
)

# ==================================================================
# 2. PAGE CONFIGURATION
# ==================================================================

st.set_page_config(
    page_title="Emma | Taskify",
    layout="wide",
    initial_sidebar_state="expanded"
)
load_css("assets/styles.css")

# Reset input box after adding a task
if st.session_state.get("should_reset_task"):
    st.session_state.new_task = ""
    st.session_state.pop("should_reset_task")


# ==================================================================
# 3. HEADER
# ==================================================================

st.title("Taskify")
st.write("Forge your synergistic intelligence by staying organized.")


# ==================================================================
# 4. ADD TASK INPUT
# ==================================================================

cols = st.columns([2, 1])

with cols[0]:
    new_task = st.text_input(
        label="Type your task here:",
        placeholder="e.g., Research AI Ethics",
        key='new_task',
        label_visibility='collapsed',
        disabled=("edit_index" in st.session_state)
    )

with cols[1]:
    if st.button("Add Task",
                 key='btn_add_task',
                 disabled=("edit_index" in st.session_state)):
        new_task = st.session_state.get("new_task", "").strip()

        if new_task:
            add_task()
            st.session_state["should_reset_task"] = True
            st.success(f"Task Added: {new_task}")
            st.rerun()
        else:
            st.warning("Please enter a valid task!")


# ==================================================================
# 5. DISPLAY TASKS
# ==================================================================

st.markdown("### My Tasks")

# Render tasks
task_list = functions.get_task_list()

pending_tasks = [(i, t) for i, t in enumerate(task_list)
                 if t["status"] == "pending"]
in_progress_tasks = [(i, t) for i, t in enumerate(task_list)
                     if t["status"] == "in_progress"]
completed_tasks = [(i, t) for i, t in enumerate(task_list)
                   if t["status"] == "completed"]

cols = st.columns([1, 1, 1])

with cols[0]:
# ==================================================================
# PENDING TASKS
# ==================================================================

    with st.expander("Pending", expanded=True):

        for index, task in pending_tasks:

            # ----------------------------
            # 1) If task is being edited
            # ----------------------------

            if st.session_state.get("edit_index") == index:

                st.text_input(
                    "Update Task:",
                    key="edit_text",
                    label_visibility="collapsed"
                )

                edit_cols = st.columns([1, 1, 1])

                with edit_cols[0]:
                    if st.button("Save", key=f"save_{index}"):
                        edit_task(index, st.session_state.edit_text)
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                with edit_cols[1]:
                    if st.button("Cancel", key=f"cancel_{index}"):
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                continue

            # ----------------------------
            # 2) If task is not being edited
            # ----------------------------

            st.markdown(
                f"""
                    <div class="glass-task">
                    {task['task']}
                    </div>
                """,
                unsafe_allow_html=True)

            row = st.columns([1, 1, 1])

            with row[0]:
                if st.button(
                        "Edit",
                        key=f"p_edit_{index}",
                        on_click=start_edit,
                        args=(index, task['task']),
                        disabled=(
                                "edit_index" in st.session_state
                                and st.session_state.edit_index != index)
                ):
                    st.session_state.edit_index = index
                    st.session_state.edit_text = task["task"]
                    st.rerun()

            with row[1]:
                if st.button("Delete",
                             key=f"p_delete_{index}",
                             disabled=("edit_index" in st.session_state)
                             ):
                    delete_task(index)
                    st.rerun()

            with row[2]:
                if st.button(
                        "Start",
                        key=f"p_in_progress_{index}",
                        disabled=("edit_index" in st.session_state)
                ):
                    update_status(index, "in_progress")
                    st.rerun()

with cols[1]:
# ==================================================================
# IN PROGRESS TASKS
# ==================================================================

    with st.expander("In Progress", expanded=True):
        for index, task in in_progress_tasks:

            # ----------------------------
            # 1) If task is being edited
            # ----------------------------

            if st.session_state.get("edit_index") == index:

                st.text_input(
                    "Update Task:",
                    key="edit_text",
                    label_visibility="collapsed"
                )

                edit_cols = st.columns([1, 1, 1])

                with edit_cols[0]:
                    if st.button("Save", key=f"save_ip_{index}"):
                        edit_task(index, st.session_state.edit_text)
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                with edit_cols[1]:
                    if st.button("Cancel", key=f"cancel_ip_{index}"):
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                continue

            # ----------------------------
            # 2) If task is not being edited
            # ----------------------------

            st.markdown(
                f"""
                    <div class="glass-task">
                    {task['task']}
                    </div>
                """,
                unsafe_allow_html=True)

            row = st.columns([1, 1, 1])

            with row[0]:
                if st.button(
                        "Edit",
                        key=f"ip_edit_{index}",
                        on_click=start_edit,
                        args=(index, task['task']),
                        disabled=(
                                "edit_index" in st.session_state
                                and st.session_state.edit_index != index)
                        ):
                    st.session_state.edit_index = index
                    st.session_state.edit_text = task["task"]
                    st.rerun()

            with row[1]:
                if st.button(
                        "Delete",
                        key=f"ip_delete_{index}",
                        disabled=("edit_index" in st.session_state)
                ):
                    delete_task(index)
                    st.rerun()

            with row[2]:
                if st.button(
                        "Complete",
                        key=f"ip_complete_{index}",
                        disabled=("edit_index" in st.session_state)
                ):
                    update_status(index, "completed")
                    st.rerun()

with cols[2]:
# ==================================================================
# COMPLETED TASKS
# ==================================================================

    with st.expander("Completed", expanded=True):
        for index, task in completed_tasks:

            # ----------------------------
            # 1) If task is being edited
            # ----------------------------

            if st.session_state.get("edit_index") == index:

                st.text_input(
                    "Update Task:",
                    key="edit_text",
                    label_visibility="collapsed"
                )

                cols = st.columns([1, 1, 1])

                with cols[0]:
                    if st.button("Save", key=f"save_ip_{index}"):
                        edit_task(index, st.session_state.edit_text)
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                with cols[1]:
                    if st.button("Cancel", key=f"cancel_ip_{index}"):
                        st.session_state.pop("edit_index")
                        st.session_state.pop("edit_text")
                        st.rerun()

                continue

            # ----------------------------
            # 2) If task is not being edited
            # ----------------------------

            st.markdown(
                f"""
                    <div class="glass-task">
                    {task['task']}
                    </div>
                """,
                unsafe_allow_html=True)

            row = st.columns([1, 1, 1])

            with row[0]:
                if st.button(
                        "Edit",
                        key=f"ip_edit_{index}",
                        on_click=start_edit,
                        args=(index, task["task"]),
                        disabled=(
                                "edit_index" in st.session_state
                                and st.session_state.edit_index != index)
                        ):
                    st.session_state.edit_index = index
                    st.session_state.edit_text = task["task"]
                    st.rerun()

            with row[1]:
                if st.button(
                        "Delete",
                        key=f"ip_delete_{index}",
                        disabled=("edit_index" in st.session_state)
                ):
                    delete_task(index)
                    st.rerun()

            with row[2]:
                if st.button(
                        "Reopen",
                        key=f"c_reopen_{index}",
                        disabled=("edit_index" in st.session_state)

                ):
                    update_status(index, "pending")
                    st.rerun()
