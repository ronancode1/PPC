import streamlit as st
import pandas as pd
import altair as alt

def calculate_cost(grams, hours, filament_type, cost_per_hour):
    if filament_type == "PLA":
        customer_price = ((grams * 6 + hours * (cost_per_hour * 100)) / 100)
        maker_price = (grams * 2.6 / 100)
    elif filament_type == "PETG":
        customer_price = ((grams * 8 + hours * (cost_per_hour * 100)) / 100)
        maker_price = (grams * 4.1 / 100)
    elif filament_type == "TPU":
        customer_price = ((grams * 10 + hours * (cost_per_hour * 100)) / 100)
        maker_price = (grams * 5.4 / 100)
    else:
        customer_price = maker_price = 0

    profit = customer_price - maker_price
    return customer_price, maker_price, profit

# Streamlit UI
st.title("🖨️ 3D Print Cost Calculator")
st.markdown("Estimate the **customer price**, **maker cost**, and **profit** of your 3D prints.")

# Inputs
grams = st.number_input("📦 Grams of filament used:", min_value=0, step=5)
hours = st.number_input("⏱️ Hours of printing time:", min_value=0, step=1)
filament_type = st.selectbox("🎯 Filament Type", ["PLA", "PETG", "TPU"])
cost_per_hour = st.number_input("💵 Cost per Hour ($):", min_value=0.0, step=0.5)

# Calculate and Show
if st.button("Calculate Cost"):
    customer_price, maker_price, profit = calculate_cost(grams, hours, filament_type, cost_per_hour)

    st.subheader("📊 Cost Breakdown")
    st.success(f"💰 Customer Price: **${customer_price:.2f}**")
    st.info(f"🧾 Maker Cost: **${maker_price:.2f}**")
    st.warning(f"📈 Profit: **${profit:.2f}**")

    # 📈 Profit Graph with Custom Colors
    data = pd.DataFrame({
        'Category': ['Customer Price', 'Maker Cost', 'Profit'],
        'Amount': [customer_price, maker_price, profit],
        'Color': ['#c40000', '#000a94', '#08c925']  # Yellow, Blue, Green
    })

    chart = alt.Chart(data).mark_bar().encode(
        x=alt.X('Category', sort=['Customer Price', 'Maker Cost', 'Profit']),
        y='Amount',
        color=alt.Color('Color:N', scale=None),
        tooltip=['Category', 'Amount']
    ).properties(
        width=500,
        height=400,
        title="Cost & Profit Breakdown"
    )

    st.altair_chart(chart, use_container_width=True)
