import datetime as dt
import json
import streamlit as st
from streamlit_lottie import st_lottie

# -------------------- 함수 정의 --------------------
def loadJSON(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def saveItems(path, items):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False)

def deleteItem(path):
    if not items:
        return
    pos = st.session_state["pos"]
    if items[pos]["status"] == "Done":
        items.pop(pos)
        saveItems("data.json", items)
        st.session_state["pos"] = 0
        st.rerun()
    else:
        st.error("Error! The task must be done before deleting!")

def hasClicked(buttonName):
    return st.session_state.get("clicked" + buttonName.capitalize(), False)

# -------------------- 데이터 로드 및 초기화 --------------------
items = loadJSON("data.json")

if "pos" not in st.session_state:
    st.session_state["pos"] = 0

# -------------------- CSS 스타일링 --------------------
st.markdown("""
<style>
div.stButton > button {
    width: 100%;
    text-align: left;
    height: auto;
    padding: 10px;
    border-radius: 5px;
    border: 1px solid #eee;
    border-left: 5px solid #ccc;
    margin-bottom: 5px;
    background-color: white;
    color: black;
    outline: none !important;
    box-shadow: none !important;
    transition: background-color 0.2s, border-color 0.2s;
}
div.stButton > button[key^="select_item_"]:hover {
    border: 1px solid #eee !important;
    border-left: 5px solid #ccc !important;
    background-color: white !important;
    color: black !important;
    box-shadow: none !important;
}
div.stButton > button:not([key^="select_item_"]):hover {
    border-color: #ff4b4b !important;
    background-color: #fff1f1 !important;
    color: #ff4b4b !important;
    cursor: pointer;
}
</style>
""", unsafe_allow_html=True)

# -------------------- 로고 + 타이틀 --------------------
col1, col2 = st.columns([1, 2])
with col1:
    try:
        lottie = loadJSON("lottie-load.json")
        st_lottie(lottie, speed=1, loop=True, width=120, height=120)
    except:
        st.title("📅")
with col2:
    ""
    st.markdown("# To Do List")

# -------------------- 메인 레이아웃 --------------------
col_list, col_btns = st.columns([6, 1.5])

with col_list:
    st.write("### List")
    if not hasClicked("add") and not hasClicked("edit"):
        for i, item in enumerate(items):
            is_selected = i == st.session_state["pos"]
            selected_text = " ✅ (선택됨)" if is_selected else ""
            
            label = f"📌 {item['description']}\n{item['date']} {item['time']} | {item['status']}{selected_text}"
            
            if st.button(label, key=f"select_item_{i}"):
                st.session_state["pos"] = i
                st.rerun()

    # ADD / EDIT 폼
    if hasClicked("add"):
        with st.form("addForm"):
            what = st.text_input("TO DO")
            when_date = st.date_input("DATE", min_value=dt.datetime.today())
            when_time = st.time_input("TIME")
            status = st.selectbox("STATUS", ["Pending", "Priority"])
            if st.form_submit_button("CONFIRM"):
                items.append({"description": what, "date": str(when_date), "time": str(when_time), "status": status})
                saveItems("data.json", items)
                st.session_state["pos"] = len(items) - 1
                st.session_state["clickedAdd"] = False
                st.rerun()
            if st.form_submit_button("CANCEL"):
                st.session_state["clickedAdd"] = False
                st.rerun()

    if hasClicked("edit") and items:
        pos = st.session_state["pos"]
        item = items[pos]
        with st.form("editForm"):
            what = st.text_input("TO DO", value=item["description"])
            when_date = st.date_input("DATE", value=dt.datetime.strptime(item["date"], "%Y-%m-%d"))
            when_time = st.time_input("TIME", value=dt.datetime.strptime(item["time"], "%H:%M:%S").time())
            status = st.selectbox("STATUS", ["Pending", "Priority", "Done"], index=["Pending", "Priority", "Done"].index(item["status"]))
            if st.form_submit_button("CONFIRM"):
                items[pos].update({"description": what, "date": str(when_date), "time": str(when_time), "status": status})
                saveItems("data.json", items)
                st.session_state["clickedEdit"] = False
                st.rerun()
            if st.form_submit_button("CANCEL"):
                st.session_state["clickedEdit"] = False
                st.rerun()

with col_btns:
    st.write("### Menu")
    # 메뉴 버튼 (key 지정)
    if st.button("ADD", use_container_width=True, key="menu_add"):
        st.session_state["clickedAdd"] = True
        st.rerun()
    if st.button("EDIT", use_container_width=True, key="menu_edit") and items:
        st.session_state["clickedEdit"] = True
        st.rerun()
    if st.button("DELETE", use_container_width=True, key="menu_delete") and items:
        deleteItem("data.json")
