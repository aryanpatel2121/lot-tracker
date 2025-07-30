import streamlit as st
import pandas as pd
import datetime
from st_aggrid import AgGrid, GridOptionsBuilder

# ---------- Load/Save Data ----------
CSV_FILE = "lots_db.csv"

def load_data():
    try:
        return pd.read_csv(CSV_FILE)
    except:
        return pd.DataFrame(columns=[
            "LOT NUMBER", "FABRICS", "FAB. DATE", "SHORT NO.", "ROLL NO.",
            "MTR", "JOBBER", "JOB DATE", "PANNO", "AVERAGE", "THREAD",
            "LENGTH", "SIZE", "K.P.", "BELT", "RATE", "WASHING"
        ])

def save_data(df):
    df.to_csv(CSV_FILE, index=False)

# ---------- Streamlit App ----------
st.set_page_config(page_title="Garment Lot Tracker", layout="wide")
st.title("🧵 Garment Lot Tracker")

df = load_data()

# ---------- Add New Lot ----------
with st.form("add_lot_form"):
    st.subheader("➕ Add New Lot")

    lot_num = st.text_input("LOT NUMBER")
    fabrics = st.text_input("FABRICS")
    fab_date = st.date_input("FAB. DATE", value=datetime.date.today(), min_value=datetime.date(1900, 1, 1))
    short_no = st.text_input("SHORT NO.")
    roll_no = st.text_input("ROLL NO.")
    mtr = st.text_input("MTR")

    st.markdown("---")

    jobber = st.text_input("JOBBER")
    job_date = st.date_input("JOB DATE", value=datetime.date.today(), min_value=datetime.date(1900, 1, 1))
    panno = st.text_input("PANNO")
    average = st.text_input("AVERAGE")

    st.markdown("---")

    thread = st.text_input("THREAD")
    length = st.text_input("LENGTH")
    size = st.text_input("SIZE")
    kp = st.text_input("K.P.")
    belt = st.text_input("BELT")
    rate = st.text_input("RATE")
    washing = st.text_input("WASHING")

    if st.form_submit_button("✅ Save Lot"):
        # ---- Validate Required Fields ----
        missing_fields = []
        required_fields = {
            "LOT NUMBER": lot_num,
            "FABRICS": fabrics,
            "SHORT NO.": short_no,
            "ROLL NO.": roll_no,
            "MTR": mtr,
            "JOBBER": jobber,
            "PANNO": panno,
            "THREAD": thread,
            "LENGTH": length,
            "SIZE": size,
            "K.P.": kp,
            "BELT": belt,
            "RATE": rate,
            "WASHING": washing,
        }

        for field, value in required_fields.items():
            if not value:
                missing_fields.append(f"❗ You didn’t add **{field}**")

        if lot_num in df["LOT NUMBER"].values:
            st.error("❗ LOT NUMBER must be unique!")
        elif missing_fields:
            for msg in missing_fields:
                st.warning(msg)
        else:
            new_row = pd.DataFrame([{
                "LOT NUMBER": lot_num,
                "FABRICS": fabrics,
                "FAB. DATE": fab_date,
                "SHORT NO.": short_no,
                "ROLL NO.": roll_no,
                "MTR": mtr,
                "JOBBER": jobber,
                "JOB DATE": job_date,
                "PANNO": panno,
                "AVERAGE": average,
                "THREAD": thread,
                "LENGTH": length,
                "SIZE": size,
                "K.P.": kp,
                "BELT": belt,
                "RATE": rate,
                "WASHING": washing,
            }])
            save_data(pd.concat([df, new_row], ignore_index=True))
            st.success("✅ Lot saved!")
            st.rerun()

# ---------- Show All Lots ----------
df = load_data()
if not df.empty:
    st.subheader("📋 All Lots")
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_selection("single")
    gb.configure_grid_options(domLayout='autoHeight')
    gb.configure_pagination()
    gb.configure_side_bar()
    grid = AgGrid(df, gridOptions=gb.build(), editable=True)

    updated_df = grid["data"]
    save_data(updated_df)

    if st.button("❌ Delete Selected Lot"):
        selected = grid["selected_rows"]
        if isinstance(selected, pd.DataFrame):
            selected = selected.to_dict(orient="records")

        if isinstance(selected, list) and len(selected) > 0 and "LOT NUMBER" in selected[0]:
            lot_number_to_delete = selected[0]["LOT NUMBER"]
            df = df[df["LOT NUMBER"] != lot_number_to_delete]
            save_data(df)
            st.success(f"✅ Deleted Lot: {lot_number_to_delete}")
            st.rerun()
        else:
            st.warning("⚠️ No valid row selected.")

    st.download_button("📤 Export CSV", df.to_csv(index=False), "lots_export.csv")
