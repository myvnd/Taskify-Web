import sys
import os
import streamlit as st

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from core import functions

st.set_page_config(layout="wide")

st.title('Taskify')

def add_task():
    """ Add a new task """
    new_task = st.session_state['new_task'].strip()
    if not new_task:
        return

    task_list = functions.get_task_list() # Read current list
    task_list.append(new_task) # Add new task
    functions.write_task_list(task_list) # Save back to file

    st.session_state.new_task = '' # Clear input box


def edit_task(index, new_text):
    """ Edit a task """
    task_list = functions.get_task_list()
    if 0 <= index < len(task_list):
        task_list[index] = new_text.strip()
        functions.write_task_list(task_list)
    st.rerun()


def delete_task(index):
    """ Delete a task """
    task_list = functions.get_task_list()
    if 0 <= index < len(task_list):
        task_list.pop(index)
        functions.write_task_list(task_list)

    # If current edit target was deleted
    if st.session_state.get("edit_index") == index:
        st.session_state.pop("edit_index", None)
        st.session_state.pop("edit_text", None)

    # If the deletion shifts indexes AFTER the edit index
    elif st.session_state.get("edit_index", -1) > index:
        st.session_state["edit_index"] -= 1

    st.rerun()


# Load task list
task_list = functions.get_task_list()


# ==== INPUT BOX ====

st.text_input(
    label='Enter a new task here:',
    placeholder='Enter text',
    key='new_task',
    on_change=add_task,
    label_visibility='visible'
)


st.write("### My Tasks")

for index, task in enumerate(task_list):
    cols = st.columns([1, 8, 1, 1])
    checked = cols[0].checkbox(
        label='Task done',
        key=f"check_{index}",
        label_visibility="hidden"
        )

    cols[1].write(task) # Show task name

    # Edit button
    if cols[2].button("Edit", key=f"edit_{index}"):
        st.session_state.edit_index = index
        st.session_state.edit_text = task

    # Delete button
    if cols[3].button("Delete", key=f"delete_{index}"):
        delete_task(index)

    # If checkbox is checked and user presses Enter in the global input
    if checked and st.session_state.get('new_task_triggered', False):
        edit_task(index, st.session_state['new_task'])


# ==== EDIT MODE UI ====

if "edit_index" in st.session_state:

    st.write("### Edit task")

    new_text = st.text_input(
        "Edit task here:",
        value=st.session_state.get("edit_text", ""),
        key="edit_input"
    )

    col0, col1, col2, col3 = st.columns([1, 8, 1, 1])

    with col2:
        if st.button("Save"):
            idx = st.session_state.get("edit_index")
            if idx is not None:
                edit_task(idx, new_text)

    with col3:
        if st.button("Cancel"):
            st.session_state.pop("edit_index", None)
            st.session_state.pop("edit_text", None)
            st.rerun()


# Reset trigger after processing update logic
st.session_state.new_task_triggered = False