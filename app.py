import streamlit as st
from sheets_helper import add_record, get_records, update_record, delete_record
from datetime import date
import re

# ========== Helpers ==========

def is_valid_mac(mac):
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return re.match(pattern, mac.strip()) is not None

@st.cache_data(ttl=30)
def cached_get_records():
    return get_records()

def safe_for_dataframe(records):
    return [{k: str(v) if v is not None else "" for k, v in row.items()} for row in records]

# ========== UI ==========
st.set_page_config(page_title="IPTV Client Manager", layout="wide")
st.title("📺 IPTV Client Manager")

tab1, tab2, tab3, tab4 = st.tabs(["➕ Add New", "📋 View All", "✏️ Edit", "🗑 Delete"])

# ➕ Add New
with tab1:
    st.subheader("➕ Add New Client")
    name = st.text_input("Name")
    phone = st.text_input("Phone Number (e.g. +355691234567)")

    start_date = st.date_input("Start Date", value=date.today())
    link = st.text_input("Link")
    end_date = st.date_input("End Date")
    mac = st.text_input("MAC Address (e.g. 00:1A:2B:3C:4D:5E)")
    cost = st.number_input("Cost", step=0.01)
    sell = st.number_input("Sell", step=0.01)
    profit = sell - cost

    if st.button("Add Record"):
        mac = mac.strip().upper()
        if mac and not is_valid_mac(mac):
            st.error("Invalid MAC Address! Use format: 00:1A:2B:3C:4D:5E")
        else:
            record = [name, phone, start_date.isoformat(), link, end_date.isoformat(), mac, cost, sell, profit]
            add_record(record)
            st.cache_data.clear()
            st.success("Record added successfully!")

# 📋 View All
with tab2:
    st.subheader("📋 All Clients")
    data = safe_for_dataframe(cached_get_records())

    if data:
        st.dataframe(data)
    else:
        st.warning("No records found.")

# ✏️ Edit
with tab3:
    st.subheader("✏️ Edit Client")
    data = safe_for_dataframe(cached_get_records())

    if not data:
        st.warning("No data to edit.")
    else:
        names = [f"{i+1}. {row['Name']}" for i, row in enumerate(data)]
        selected = st.selectbox("Select a client to edit", names)
        index = names.index(selected)
        record = data[index]

        name = st.text_input("Name", record["Name"])
        phone = st.text_input("Phone Number", record["Phone"])
        start_date = st.date_input("Start Date", value=date.fromisoformat(record["Start Date"]))
        link = st.text_input("Link", record["Link"])
        end_date = st.date_input("End Date", value=date.fromisoformat(record["End Date"]))
        mac = st.text_input("MAC Address", record["Mac Address"])
        cost = st.number_input("Cost", value=float(record["Cost"]), step=0.01)
        sell = st.number_input("Sell", value=float(record["Sell"]), step=0.01)
        profit = sell - cost

        if st.button("Update Record"):
            mac = mac.strip().upper()
            if mac and not is_valid_mac(mac):
                st.error("Invalid MAC Address! Use format: 00:1A:2B:3C:4D:5E")
            else:
                new_data = [name, phone, start_date.isoformat(), link, end_date.isoformat(), mac, cost, sell, profit]
                update_record(index, new_data)
                st.cache_data.clear()
                st.success("Record updated.")

# 🗑 Delete
with tab4:
    st.subheader("🗑 Delete Client")
    data = safe_for_dataframe(cached_get_records())

    if not data:
        st.warning("No data to delete.")
    else:
        names = [f"{i+1}. {row['Name']}" for i, row in enumerate(data)]
        selected = st.selectbox("Select a client to delete", names)
        index = names.index(selected)

        if st.button("Delete"):
            delete_record(index)
            st.cache_data.clear()
            st.success("Deleted successfully.")
