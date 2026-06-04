import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------

st.set_page_config(
    page_title="Car Purchase Analyzer",
    page_icon="🚗",
    layout="wide"
)

# -----------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------

st.markdown("""
<style>

.main {
    padding-top: 1rem;
}

div[data-testid="stMetric"]{
    background-color:white;
    padding:15px;
    border-radius:12px;
    border:1px solid #E5E7EB;
    box-shadow:0px 2px 8px rgba(0,0,0,0.05);
}

.stDataFrame{
    border-radius:12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------
# TITLE
# -----------------------------------------------------

st.title("🚗 Car Purchase Financial Analyzer")

st.markdown("""
Compare the cost of purchasing a vehicle using:

- Full Loan
- Half Loan + Half Cash
- Full Cash

and determine which option is most economical.
""")

# -----------------------------------------------------
# INPUTS
# -----------------------------------------------------

col1, col2, col3, col4 = st.columns(4)

with col1:
    car_price = st.number_input(
        "Car Price (₹)",
        min_value=100000,
        value=1000000,
        step=50000
    )

with col2:
    interest_rate = st.number_input(
        "Interest Rate (%)",
        min_value=0.0,
        value=9.0,
        step=0.1
    )

with col3:
    loan_years = st.number_input(
        "Loan Duration (Years)",
        min_value=1,
        value=5
    )

with col4:
    interest_type = st.selectbox(
        "Interest Type",
        [
            "Reducing Balance",
            "Flat Interest"
        ]
    )

# -----------------------------------------------------
# FUNCTIONS
# -----------------------------------------------------

def reducing_balance_emi(principal, annual_rate, years):

    monthly_rate = annual_rate / (12 * 100)

    months = years * 12

    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (
            principal *
            monthly_rate *
            (1 + monthly_rate) ** months
        ) / (
            (1 + monthly_rate) ** months - 1
        )

    total_payment = emi * months
    interest_paid = total_payment - principal

    return emi, total_payment, interest_paid


def flat_interest_emi(principal, annual_rate, years):

    interest_paid = (
        principal *
        annual_rate *
        years
    ) / 100

    total_payment = principal + interest_paid

    emi = total_payment / (years * 12)

    return emi, total_payment, interest_paid


def calculate_loan(principal, annual_rate, years):

    if interest_type == "Reducing Balance":
        return reducing_balance_emi(
            principal,
            annual_rate,
            years
        )

    return flat_interest_emi(
        principal,
        annual_rate,
        years
    )

# -----------------------------------------------------
# ANALYZE BUTTON
# -----------------------------------------------------

if st.button("Analyze Purchase Options"):

    # -------------------------
    # FULL LOAN
    # -------------------------

    emi1, total1, interest1 = calculate_loan(
        car_price,
        interest_rate,
        loan_years
    )

    # -------------------------
    # HALF LOAN + HALF CASH
    # -------------------------

    half_loan = car_price * 0.5

    emi2, loan_total2, interest2 = calculate_loan(
        half_loan,
        interest_rate,
        loan_years
    )

    total2 = loan_total2 + half_loan

    # -------------------------
    # FULL CASH
    # -------------------------

    emi3 = 0
    interest3 = 0
    total3 = car_price

    # -------------------------
    # RESULTS TABLE
    # -------------------------

    results = pd.DataFrame({

        "Option": [
            "Full Loan",
            "Half Loan + Half Cash",
            "Full Cash"
        ],

        "Total Cost (₹)": [
            round(total1),
            round(total2),
            round(total3)
        ],

        "Interest Paid (₹)": [
            round(interest1),
            round(interest2),
            round(interest3)
        ],

        "Monthly EMI (₹)": [
            round(emi1),
            round(emi2),
            round(emi3)
        ]
    })

    # -------------------------
    # BEST OPTION
    # -------------------------

    best_option = results.loc[
        results["Total Cost (₹)"].idxmin(),
        "Option"
    ]

    # -------------------------
    # METRICS
    # -------------------------

    st.subheader("📈 Key Metrics")

    m1, m2, m3 = st.columns(3)

    with m1:
        st.metric(
            "Full Loan EMI",
            f"₹{emi1:,.0f}"
        )

    with m2:
        st.metric(
            "Half Loan EMI",
            f"₹{emi2:,.0f}"
        )

    with m3:
        st.metric(
            "Interest Saved",
            f"₹{interest1-interest2:,.0f}"
        )

    st.success(
        f"🏆 Recommended Option: {best_option}"
    )

    # -------------------------
    # TABLE
    # -------------------------

    st.subheader("📋 Comparison Table")

    st.dataframe(
        results,
        use_container_width=True
    )

    # -------------------------
    # CHART 1
    # -------------------------

    st.subheader("📊 Interest Comparison")

    fig1 = px.bar(
        results,
        x="Option",
        y="Interest Paid (₹)",
        text="Interest Paid (₹)",
        template="plotly_white"
    )

    fig1.update_layout(
        height=320,
        title="Interest Paid by Option",
        title_x=0.5,
        showlegend=False
    )

    fig1.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig1,
        use_container_width=True
    )

    # -------------------------
    # CHART 2
    # -------------------------

    st.subheader("📊 EMI Comparison")

    fig2 = px.bar(
        results,
        x="Option",
        y="Monthly EMI (₹)",
        text="Monthly EMI (₹)",
        template="plotly_white"
    )

    fig2.update_layout(
        height=320,
        title="Monthly EMI Comparison",
        title_x=0.5,
        showlegend=False
    )

    fig2.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # -------------------------
    # CHART 3
    # -------------------------

    st.subheader("📊 Total Cost Comparison")

    fig3 = px.bar(
        results,
        x="Option",
        y="Total Cost (₹)",
        text="Total Cost (₹)",
        template="plotly_white"
    )

    fig3.update_layout(
        height=320,
        title="Total Cost Comparison",
        title_x=0.5,
        showlegend=False
    )

    fig3.update_traces(
        texttemplate="₹%{y:,.0f}",
        textposition="outside"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    # -------------------------
    # SUMMARY
    # -------------------------

    st.subheader("📝 Summary")

    st.write(f"""
**Interest Method:** {interest_type}

**Full Loan**
- Total Cost: ₹{total1:,.0f}
- Interest Paid: ₹{interest1:,.0f}

**Half Loan + Half Cash**
- Total Cost: ₹{total2:,.0f}
- Interest Paid: ₹{interest2:,.0f}

**Full Cash**
- Total Cost: ₹{total3:,.0f}
- Interest Paid: ₹0

🏆 Recommended Option: **{best_option}**
""")