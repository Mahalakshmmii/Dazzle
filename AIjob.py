import streamlit as st



import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="SalaryNex | Data & AI Career Intelligence",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)
# 🌈 Vibrant dashboard color palette
vibrant_colors = [
    "#6C5CE7",  # Pink
    "#290EAE",  # Purple
    "#00C2FF",  # Cyan
    "#00D084",  # Green
    "#FFB000",  # Orange
    "#FF5A5F",  # Coral
    "#00B8A9",  # Teal
    "#845EC2"   # Violet
]


# ---------------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------------

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }

    /* Main title */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 25px;
    }

    /* KPI cards */
    .kpi-card {
        background: linear-gradient(135deg, #1e293b, #172033);
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #334155;
        box-shadow: 0 4px 15px rgba(0,0,0,0.25);
    }

    .kpi-title {
        color: #94a3b8;
        font-size: 14px;
        font-weight: 600;
    }

    .kpi-value {
        color: #f8fafc;
        font-size: 28px;
        font-weight: 800;
        margin-top: 5px;
    }

    .kpi-description {
        color: #38bdf8;
        font-size: 13px;
        margin-top: 5px;
    }

    /* Section headings */
    .section-title {
        font-size: 24px;
        font-weight: 700;
        color: #f8fafc;
        margin-top: 15px;
        margin-bottom: 10px;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    /* Buttons */
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }

    /* Improve text visibility on dark theme */
.stApp,
.stApp p,
.stApp span,
.stApp label,
.stApp div,
.stMarkdown,
.stCaption {
    color: #F5F7FA !important;
}

/* Sidebar text */
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label {
    color: #E8ECF2 !important;
}

/* Metric labels and values */
[data-testid="stMetricLabel"] {
    color: #DDE3EA !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
}

/* Captions */
.stCaption {
    color: #B8C0CC !important;
}

/* Tab names */
button[data-baseweb="tab"] {
    color: #E8ECF2 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #FFFFFF !important;
}
/* Reset Filters button */
section[data-testid="stSidebar"] .stButton button {
    background-color: #FFFFFF !important;
    color: #000000 !important;
    border: 1px solid #FFFFFF !important;
    font-weight: 800 !important;
}

section[data-testid="stSidebar"] .stButton button p,
section[data-testid="stSidebar"] .stButton button span {
    color: #000000 !important;
}
/* Match Streamlit header with dashboard background */
header[data-testid="stHeader"] {
    background-color: #0F172A !important;
}



</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">💼 SalaryNex</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Global Data & AI Career Intelligence • Explore • Compare • Discover'
    '</div>',
    unsafe_allow_html=True
)
# ---------------------------------------------------------
# LOAD REAL KAGGLE DATASET
# ---------------------------------------------------------

@st.cache_data
def load_data():

    df = pd.read_csv("ds_salaries.csv")

    # Remove unnecessary index column if present
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    return df


df = load_data()


# ---------------------------------------------------------
# DATA PREPARATION
# ---------------------------------------------------------

# Convert experience level codes into readable names
experience_map = {
    "EN": "Entry Level",
    "MI": "Mid Level",
    "SE": "Senior Level",
    "EX": "Executive Level"
}

df["experience_level"] = df["experience_level"].map(experience_map)


# Convert employment type codes
employment_map = {
    "FT": "Full Time",
    "PT": "Part Time",
    "CT": "Contract",
    "FL": "Freelance"
}

df["employment_type"] = df["employment_type"].map(employment_map)


# Convert remote ratio into readable categories
def remote_category(value):

    if value == 0:
        return "On-site"
    elif value == 50:
        return "Hybrid"
    else:
        return "Fully Remote"


df["remote_status"] = df["remote_ratio"].apply(remote_category)


# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------


# ---------------------------------------------------------
# SIDEBAR — INTERACTIVE FILTERS
# ---------------------------------------------------------

# =========================================================
# SIDEBAR HEADER — FINAL UI
# =========================================================

st.sidebar.markdown(
    """
    <div style="text-align:center; padding:10px 0 20px 0;">
        <div style="font-size:32px;">⚡</div>
        <h2 style="margin:0;">SalaryNex</h2>
        <p style="margin-top:5px; opacity:0.7;">
            Data & AI Career Intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎛️ Filters")
st.sidebar.caption(
    "Customize the dashboard to explore salary trends."
)
# ---------------------------------------------------------
# RESET BUTTON
# ---------------------------------------------------------

if st.sidebar.button("🔄 Reset Filters", use_container_width=True):
    st.rerun()


# ---------------------------------------------------------
# JOB TITLE
# ---------------------------------------------------------

job_options = sorted(df["job_title"].dropna().unique())

selected_jobs = st.sidebar.multiselect(
    "💼 Job Title",
    options=job_options,
    default=job_options
)


# ---------------------------------------------------------
# EXPERIENCE LEVEL
# ---------------------------------------------------------

experience_options = [
    "Entry Level",
    "Mid Level",
    "Senior Level",
    "Executive Level"
]

selected_experience = st.sidebar.multiselect(
    "📊 Experience Level",
    options=experience_options,
    default=experience_options
)


# ---------------------------------------------------------
# EMPLOYMENT TYPE
# ---------------------------------------------------------

employment_options = sorted(
    df["employment_type"].dropna().unique()
)

selected_employment = st.sidebar.multiselect(
    "🧑‍💻 Employment Type",
    options=employment_options,
    default=employment_options
)


# ---------------------------------------------------------
# EMPLOYEE RESIDENCE
# ---------------------------------------------------------

country_options = sorted(
    df["employee_residence"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "🌎 Employee Residence",
    options=country_options,
    default=country_options
)


# ---------------------------------------------------------
# REMOTE WORK
# ---------------------------------------------------------

remote_options = [
    "On-site",
    "Hybrid",
    "Fully Remote"
]

selected_remote = st.sidebar.multiselect(
    "🏠 Work Mode",
    options=remote_options,
    default=remote_options
)


# ---------------------------------------------------------
# WORK YEAR
# ---------------------------------------------------------

year_options = sorted(
    df["work_year"].dropna().unique()
)

selected_years = st.sidebar.multiselect(
    "📅 Work Year",
    options=year_options,
    default=year_options
)


# ---------------------------------------------------------
# SALARY RANGE
# ---------------------------------------------------------

min_salary = int(df["salary_in_usd"].min())
max_salary = int(df["salary_in_usd"].max())

selected_salary = st.sidebar.slider(
    "💰 Salary Range (USD)",
    min_value=min_salary,
    max_value=max_salary,
    value=(min_salary, max_salary),
    step=5000,
    format="$%d"
)


# ---------------------------------------------------------
# APPLY FILTERS
# ---------------------------------------------------------

filtered_df = df[
    (df["job_title"].isin(selected_jobs)) &
    (df["experience_level"].isin(selected_experience)) &
    (df["employment_type"].isin(selected_employment)) &
    (df["employee_residence"].isin(selected_countries)) &
    (df["remote_status"].isin(selected_remote)) &
    (df["work_year"].isin(selected_years)) &
    (df["salary_in_usd"].between(
        selected_salary[0],
        selected_salary[1]
    ))
].copy()


# ---------------------------------------------------------
# FILTER SUMMARY
# ---------------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.markdown(
    f"""
    **📌 Active Records**

    ### {len(filtered_df):,}

    out of **{len(df):,}** total records
    """
)
# =========================================================
# MACHINE LEARNING — SALARY PREDICTION MODEL
# =========================================================

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

features = [
    "work_year",
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence",
    "remote_ratio"
]

target = "salary_in_usd"

X = df[features]
y = df[target]

categorical_features = [
    "experience_level",
    "employment_type",
    "job_title",
    "employee_residence"
]

numerical_features = [
    "work_year",
    "remote_ratio"
]

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        )
    ],
    remainder="passthrough"
)

salary_model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "model",
            RandomForestRegressor(
                n_estimators=200,
                random_state=42
            )
        )
    ]
)

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

salary_model.fit(X_train, y_train)

y_pred = salary_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# =========================================================
# EXECUTIVE SUMMARY
# =========================================================

st.markdown("---")
st.markdown("## ⚡ Executive Summary")
st.caption(
    "A quick overview of the current salary market selection."
)

if len(filtered_df) > 0:

    summary_avg_salary = filtered_df["salary_in_usd"].mean()

    summary_top_job = (
        filtered_df["job_title"]
        .value_counts()
        .idxmax()
    )

    summary_top_country = (
        filtered_df
        .groupby("employee_residence")["salary_in_usd"]
        .mean()
        .idxmax()
    )

    summary_top_experience = (
        filtered_df
        .groupby("experience_level")["salary_in_usd"]
        .mean()
        .idxmax()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "💰 Average Salary",
            f"${summary_avg_salary:,.0f}"
        )

    with col2:
        st.metric(
            "🏆 Most Represented Career",
            summary_top_job
        )

    with col3:
        st.metric(
            "🌎 Highest-Paying Country",
            summary_top_country
        )

    with col4:
        st.metric(
            "📈 Highest Salary Level",
            summary_top_experience
        )

    st.markdown("### 💡 Key Finding")

    st.success(
        f"""
        **{summary_top_experience}** positions currently show the
        highest average salary, while **{summary_top_job}** is the
        most represented career in the selected dataset.
        """
    )

else:

    st.warning(
        "⚠️ No records match the current filters."
    )
# =========================================================
# DASHBOARD TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Market Overview",
    "🔬 Advanced Analytics",
    "🧠 Career Intelligence",
    "🤖 ML & Dataset"
])
with tab1:

    st.markdown("## 📊 Salary Market Snapshot")
    st.caption(
        "A high-level overview of salary trends, experience levels and career demand."
    )

    if len(filtered_df) == 0:

        st.warning("⚠️ No records match your selected filters.")

    else:

        # =====================================================
        # KPI CARDS
        # =====================================================

        total_records = len(filtered_df)

        avg_salary = filtered_df["salary_in_usd"].mean()

        median_salary = filtered_df["salary_in_usd"].median()

        highest_salary = filtered_df["salary_in_usd"].max()

        top_job = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "📁 Records",
                f"{total_records:,}"
            )

        with col2:
            st.metric(
                "💰 Average Salary",
                f"${avg_salary:,.0f}"
            )

        with col3:
            st.metric(
                "📈 Median Salary",
                f"${median_salary:,.0f}"
            )

        with col4:
            st.metric(
                "🏆 Highest Salary",
                f"${highest_salary:,.0f}"
            )

        st.caption(
            f"🔥 Most represented career: **{top_job}**"
        )

        st.markdown("---")

        # =====================================================
        # ROW 1 — EXPERIENCE SALARY + YEAR TREND
        # =====================================================

        col1, col2 = st.columns(2)

        # -----------------------------------------------------
        # AVERAGE SALARY BY EXPERIENCE
        # -----------------------------------------------------

        with col1:

            st.markdown("### 📈 Salary by Experience Level")

            experience_salary = (
                filtered_df
                .groupby("experience_level")["salary_in_usd"]
                .mean()
                .reindex([
                    "Entry Level",
                    "Mid Level",
                    "Senior Level",
                    "Executive Level"
                ])
                .dropna()
                .reset_index()
            )

            fig_experience_salary = px.bar(
                experience_salary,
                x="experience_level",
                y="salary_in_usd",
                title="Average Salary by Experience Level",
                labels={
                    "experience_level": "Experience Level",
                    "salary_in_usd": "Average Salary (USD)"
                },
                text_auto=".2s"
            )

            fig_experience_salary.update_traces(
                marker_color="#7B61FF"
            )

            fig_experience_salary.update_layout(
                height=400,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                ),
                showlegend=False
            )

            st.plotly_chart(
                fig_experience_salary,
                use_container_width=True
            )

        # -----------------------------------------------------
        # SALARY TREND BY YEAR
        # -----------------------------------------------------

        with col2:

            st.markdown("### 📅 Salary Trend")

            yearly_salary = (
                filtered_df
                .groupby("work_year")["salary_in_usd"]
                .mean()
                .reset_index()
            )

            fig_salary_trend = px.line(
                yearly_salary,
                x="work_year",
                y="salary_in_usd",
                markers=True,
                title="Average Salary Trend by Work Year",
                labels={
                    "work_year": "Work Year",
                    "salary_in_usd": "Average Salary (USD)"
                }
            )

            fig_salary_trend.update_traces(
                line_width=3,
                marker_size=9,
                text=yearly_salary["salary_in_usd"],
                texttemplate="$%{text:,.0f}",
                textposition="top center"
            )

            fig_salary_trend.update_layout(
                height=400,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                )
            )

            st.plotly_chart(
                fig_salary_trend,
                use_container_width=True
            )

        # =====================================================
        # ROW 2 — TOP CAREERS + WORK MODE
        # =====================================================

        col1, col2 = st.columns(2)

        # -----------------------------------------------------
        # TOP CAREERS
        # -----------------------------------------------------

        with col1:

            st.markdown("### 💼 Top Career Roles")

            top_jobs = (
                filtered_df["job_title"]
                .value_counts()
                .head(7)
                .sort_values()
                .reset_index()
            )

            top_jobs.columns = [
                "job_title",
                "job_count"
            ]

            fig_top_jobs = px.bar(
                top_jobs,
                x="job_count",
                y="job_title",
                orientation="h",
                title="Most Represented Career Roles",
                text="job_count",
                labels={
                    "job_title": "Job Role",
                    "job_count": "Number of Records"
                }
            )

            fig_top_jobs.update_traces(
                marker_color="#00C2FF",
                textposition="outside"
            )

            fig_top_jobs.update_layout(
                height=400,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                ),
                showlegend=False
            )

            st.plotly_chart(
                fig_top_jobs,
                use_container_width=True
            )

        # -----------------------------------------------------
        # WORK MODE DISTRIBUTION
        # -----------------------------------------------------

        with col2:

            st.markdown("### 🏠 Work Mode Distribution")

            work_mode_counts = (
                filtered_df["remote_status"]
                .value_counts()
                .reset_index()
            )

            work_mode_counts.columns = [
                "work_mode",
                "count"
            ]

            fig_work_mode = px.pie(
                work_mode_counts,
                names="work_mode",
                values="count",
                hole=0.5,
                title="On-site vs Hybrid vs Fully Remote"
            )

            fig_work_mode.update_traces(
                textinfo="label+percent+value",
                textposition="inside",
                marker=dict(
                    colors=[
                        "#290EAE",
                        "#00C2FF",
                        "#00D084"
                    ]
                )
            )

            fig_work_mode.update_layout(
                height=400,
                margin=dict(
                    l=20,
                    r=20,
                    t=60,
                    b=20
                )
            )

            st.plotly_chart(
                fig_work_mode,
                use_container_width=True
            )

        # =====================================================
        # KEY MARKET INSIGHT
        # =====================================================

        st.markdown("---")
        st.markdown("### 💡 Market Insight")

        highest_experience = (
            filtered_df
            .groupby("experience_level")["salary_in_usd"]
            .mean()
            .idxmax()
        )

        highest_experience_salary = (
            filtered_df
            .groupby("experience_level")["salary_in_usd"]
            .mean()
            .max()
        )

        st.success(
            f"""
            **{highest_experience}** positions have the highest average
            salary in the current selection, at approximately
            **${highest_experience_salary:,.0f}**.

            The dashboard currently contains **{total_records:,} records**
            across **{filtered_df["job_title"].nunique():,} career roles**.
            """
        )



    # ============================================================
# 🔬 ADVANCED ANALYTICS
# ============================================================

with tab2:

    st.markdown("## 🔬 Advanced Analytics")
    st.caption("Explore salary patterns, employment structure, remote work and experience-level trends.")

    # ========================================================
    # ROW 1 — EMPLOYMENT TYPE + EXPERIENCE LEVEL
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 1. Employment Type Donut
    # --------------------------------------------------------
    with col1:

        st.markdown("### 💼 Employment Type")

        employment_counts = (
            filtered_df["employment_type"]
            .value_counts()
            .reset_index()
        )

        employment_counts.columns = [
            "employment_type",
            "count"
        ]

        fig_employment = px.pie(
            employment_counts,
            names="employment_type",
            values="count",
            hole=0.55,
            title="Employment Type Distribution"
        )

        fig_employment.update_traces(
            textinfo="label+percent+value",
            textposition="inside",
            marker=dict(
            colors=[
            "#370472",
            "#7B61FF",
            "#00C2FF",
            "#00D084",
            "#FFB000",
            "#FF5A5F"]


        ))

        fig_employment.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True
        )

        st.plotly_chart(
            fig_employment,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 2. Experience Level Pie
    # --------------------------------------------------------
    with col2:

        st.markdown("### 🎓 Experience Level")

        experience_counts = (
            filtered_df["experience_level"]
            .value_counts()
            .reset_index()
        )

        experience_counts.columns = [
            "experience_level",
            "count"
        ]

        fig_experience = px.pie(
            experience_counts,
            names="experience_level",
            values="count",
            hole=0.45,
            title="Experience Level Distribution"
        )

        fig_experience.update_traces(
            textinfo="label+percent+value",
            textposition="inside",
            marker=dict(
            colors=[
            "#B9E616",
            "#7B61FF",
            "#00C2FF",
            "#00D084",
            "#FFB000",
            "#FF5A5F"
            ]
            )
            )
        fig_experience.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=True
        )

        st.plotly_chart(
            fig_experience,
            use_container_width=True
        )


    # ========================================================
    # ROW 2 — HISTOGRAM + BOX PLOT
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 3. Salary Distribution Histogram
    # --------------------------------------------------------
    with col1:

        st.markdown("### 💰 Salary Distribution")

        fig_hist = px.histogram(
            filtered_df,
            x="salary_in_usd",
            nbins=25,
            title="Salary Distribution",
            labels={
                "salary_in_usd": "Salary (USD)"
            }
        )
        fig_hist.update_traces(
        marker_color="#7B61FF",
        marker_line_color="#FFFFFF",
        marker_line_width=1,
        texttemplate="%{y}",
        textposition="outside"
        )



        fig_hist.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            xaxis_title="Salary (USD)",
            yaxis_title="Number of Employees"
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 4. Salary Spread & Outliers Box Plot
    # --------------------------------------------------------
    with col2:

        st.markdown("### 📦 Salary Spread & Outliers")

        fig_box = px.box(
            filtered_df,
            x="experience_level",
            y="salary_in_usd",
            color="experience_level",
            title="Salary Spread by Experience Level",
            labels={
                "experience_level": "Experience Level",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_box.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_box,
            use_container_width=True
        )


    # ========================================================
    # ROW 3 — HEATMAP + REMOTE WORK SCATTER
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 5. Salary Heatmap
    # --------------------------------------------------------
    with col1:

        st.markdown("### 🔥 Salary Heatmap")

        heatmap_data = (
            filtered_df
            .groupby(
                ["experience_level", "remote_status"]
            )["salary_in_usd"]
            .mean()
            .reset_index()
        )

        heatmap_pivot = heatmap_data.pivot(
            index="experience_level",
            columns="remote_status",
            values="salary_in_usd"
        )

        fig_heatmap = px.imshow(
            heatmap_pivot,
            text_auto=".0f",
            aspect="auto",
            title="Average Salary by Experience & Work Mode",
            labels={
                "x": "Work Mode",
                "y": "Experience Level",
                "color": "Average Salary (USD)"
            
            },
            color_continuous_scale=[
    "#E0F2F1",
    "#4DB6AC",
    "#00A896",
    "#00796B",
    "#004D40"
]
        )

        fig_heatmap.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_heatmap,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 6. Salary vs Remote Work Scatter
    # --------------------------------------------------------
    with col2:

        st.markdown("### 🌍 Salary vs Remote Work")

        fig_remote = px.scatter(
            filtered_df,
            x="remote_ratio",
            y="salary_in_usd",
            color="experience_level",
            hover_data=[
                "job_title",
                "employee_residence",
                "employment_type"
            ],
            title="Salary vs Remote Work Ratio",
            labels={
                "remote_ratio": "Remote Work (%)",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_remote.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_remote,
            use_container_width=True
        )


    # ========================================================
    # ROW 4 — VIOLIN + YEAR TREND
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # 7. Salary Distribution Density Violin
    # --------------------------------------------------------
    with col1:

        st.markdown("### 🎻 Salary Density")

        fig_violin = px.violin(
            filtered_df,
            y="salary_in_usd",
            x="experience_level",
            color="experience_level",
            box=True,
            points="outliers",
            title="Salary Density by Experience Level",
            labels={
                "experience_level": "Experience Level",
                "salary_in_usd": "Salary (USD)"
            }
        )

        fig_violin.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20),
            showlegend=False
        )

        st.plotly_chart(
            fig_violin,
            use_container_width=True
        )

    # --------------------------------------------------------
    # 8. Salary Trend by Work Year
    # --------------------------------------------------------
    with col2:

        st.markdown("### 📈 Salary Trend")

        yearly_salary = (
            filtered_df
            .groupby("work_year")["salary_in_usd"]
            .mean()
            .reset_index()
        )

        fig_year = px.line(
            yearly_salary,
            x="work_year",
            y="salary_in_usd",
            markers=True,
            title="Average Salary Trend by Year",
            labels={
                "work_year": "Work Year",
                "salary_in_usd": "Average Salary (USD)"
            }
        )

        fig_year.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=60, b=20)
        )

        st.plotly_chart(
            fig_year,
            use_container_width=True
        )

    if len(filtered_df) > 0:

    # =================================================
    # SECTION 1 — TOP JOB ROLES BY DEMAND
    # =================================================

        st.markdown("### 📊 Most Represented Career Roles")

        top_jobs = (
        filtered_df["job_title"]
        .value_counts()
        .head(10)
        .reset_index()
        )

        top_jobs.columns = [
        "job_title",
        "job_count"
        ]

        fig_jobs = px.bar(
        top_jobs,
        x="job_count",
        y="job_title",
        orientation="h",
        title="Top 10 Career Roles by Demand",
        color="job_count",
        color_continuous_scale=[
            "#FF4B91",
            "#7B61FF",
            "#00C2FF",
            "#00D084",
            "#FFB000"
        ],
        text="job_count"
        )

        fig_jobs.update_traces(
        texttemplate="%{text}",
        textposition="outside"
        )

        fig_jobs.update_layout(
        height=500,
        yaxis={"categoryorder": "total ascending"},
        showlegend=False,
        xaxis_title="Number of Records",
        yaxis_title="Job Role"
        )

        st.plotly_chart(
        fig_jobs,
        use_container_width=True
    )


        # =================================================
        # SECTION 2 — HIGHEST PAYING JOB ROLES
        # =================================================

        st.markdown("### 💰 Highest-Paying Career Roles")

        job_salary = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig_job_salary = px.bar(
            job_salary,
            x="salary_in_usd",
            y="job_title",
            orientation="h",
            color="job_title",
            title="Top 10 Job Roles by Average Salary",
            labels={
                "job_title": "Job Role",
                "salary_in_usd": "Average Salary (USD)"
            },
            text_auto=".2s"
        )

        fig_job_salary.update_layout(
            height=500,
            yaxis={"categoryorder": "total ascending"},
            showlegend=False
        )

        st.plotly_chart(
            fig_job_salary,
            use_container_width=True
        )


        # =================================================
        # SECTION 3 — CAREER SUMMARY
        # =================================================

        st.markdown("### 🏆 Career Highlights")

        highest_paid_role = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .idxmax()
        )

        highest_paid_salary = (
            filtered_df
            .groupby("job_title")["salary_in_usd"]
            .mean()
            .max()
        )

        most_demanded_role = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🏆 Highest-Paying Role",
                highest_paid_role
            )

        with col2:
            st.metric(
                "💰 Average Salary",
                f"${highest_paid_salary:,.0f}"
            )

        with col3:
            st.metric(
                "🔥 Most Represented Role",
                most_demanded_role
            )

    else:

        st.warning(
            "⚠️ No records match your current filters. "
            "Try changing the selections in the sidebar."
        )
    


# =========================================================
# TAB 3 — CAREER INTELLIGENCE
# =========================================================

with tab3:

    st.markdown("## 🧠 Career Intelligence")
    st.caption(
        "Explore career growth, salary opportunities, market insights, "
        "and career recommendations."
    )

    # =====================================================
    # CAREER GROWTH SIMULATOR
    # =====================================================

    st.markdown("---")
    st.markdown("### 📈 Career Growth Simulator")
    st.caption(
        "See how average salary changes as experience increases."
    )

    if len(filtered_df) > 0:

        growth_job = st.selectbox(
            "💼 Select a Career",
            sorted(
                filtered_df["job_title"]
                .dropna()
                .unique()
            ),
            key="growth_job"
        )

        growth_data = (
            filtered_df[
                filtered_df["job_title"] == growth_job
            ]
            .groupby("experience_level")["salary_in_usd"]
            .mean()
            .reindex([
                "Entry Level",
                "Mid Level",
                "Senior Level",
                "Executive Level"
            ])
            .reset_index()
        )

        growth_data = growth_data.dropna()

        if len(growth_data) >= 2:

            fig_growth = px.line(
                growth_data,
                x="experience_level",
                y="salary_in_usd",
                markers=True,
                title=f"Salary Growth Path — {growth_job}",
                labels={
                    "experience_level": "Experience Level",
                    "salary_in_usd": "Average Salary (USD)"
                }
            )

            fig_growth.update_traces(
                texttemplate="$%{y:,.0f}",
                textposition="top center"
            )

            fig_growth.update_layout(
                height=450,
                xaxis_title=None,
                yaxis_title="Average Salary (USD)"
            )

            st.plotly_chart(
                fig_growth,
                use_container_width=True
            )

            # Growth Summary

            first_salary = growth_data[
                "salary_in_usd"
            ].iloc[0]

            last_salary = growth_data[
                "salary_in_usd"
            ].iloc[-1]

            salary_difference = (
                last_salary - first_salary
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "💰 Salary Difference",
                    f"${salary_difference:,.0f}"
                )

            with col2:

                if first_salary > 0:

                    growth_percentage = (
                        salary_difference
                        / first_salary
                    ) * 100

                    st.metric(
                        "📈 Growth",
                        f"{growth_percentage:.1f}%"
                    )

        else:

            st.info(
                "Not enough experience-level data for this "
                "career to display a growth path."
            )

    else:

        st.warning(
            "⚠️ No records match the current filters. "
            "Please adjust the sidebar filters."
        )


    # =====================================================
    # AUTOMATIC CAREER INSIGHTS
    # =====================================================

    st.markdown("---")
    st.markdown("### 🧠 Automatic Career Insights")
    st.caption(
        "Key insights generated automatically from the selected data."
    )

    if len(filtered_df) > 0:

        # Highest-paying experience level

        experience_salary = (
            filtered_df
            .groupby("experience_level")["salary_in_usd"]
            .mean()
        )

        highest_experience = (
            experience_salary.idxmax()
        )

        highest_experience_salary = (
            experience_salary.max()
        )

        # Most demanded job

        most_demanded = (
            filtered_df["job_title"]
            .value_counts()
            .idxmax()
        )

        most_demanded_count = (
            filtered_df["job_title"]
            .value_counts()
            .max()
        )

        # Highest-paying country

        country_salary = (
            filtered_df
            .groupby("employee_residence")[
                "salary_in_usd"
            ]
            .mean()
            .sort_values(ascending=False)
        )

        highest_country = (
            country_salary.idxmax()
        )

        highest_country_salary = (
            country_salary.max()
        )

        # Best work mode

        remote_salary = (
            filtered_df
            .groupby("remote_status")[
                "salary_in_usd"
            ]
            .mean()
            .sort_values(ascending=False)
        )

        best_work_mode = (
            remote_salary.idxmax()
        )

        best_work_mode_salary = (
            remote_salary.max()
        )

        col1, col2 = st.columns(2)

        with col1:

            st.success(
                f"""
                💰 **Salary Insight**

                **{highest_experience}** roles have the highest
                average salary at
                **${highest_experience_salary:,.0f}**.
                """
            )

            st.info(
                f"""
                🔥 **Demand Insight**

                **{most_demanded}** is the most represented
                career with **{most_demanded_count:,} records**.
                """
            )

        with col2:

            st.info(
                f"""
                🌎 **Geography Insight**

                **{highest_country}** has the highest average
                salary at **${highest_country_salary:,.0f}**.
                """
            )

            st.info(
                f"""
                🏠 **Work Mode Insight**

                **{best_work_mode}** has the highest average
                salary at **${best_work_mode_salary:,.0f}**.
                """
            )

    else:

        st.info(
            "Select some records using the sidebar filters "
            "to generate career insights."
        )


    # =====================================================
    # CAREER RECOMMENDATION ENGINE
    # =====================================================

    st.markdown("---")
    st.markdown("### 🎯 Career Recommendation Engine")
    st.caption(
        "Discover career options based on salary and market demand."
    )

    if len(filtered_df) > 0:

        recommendation_level = st.selectbox(
            "📊 Select Experience Level",
            [
                "Entry Level",
                "Mid Level",
                "Senior Level",
                "Executive Level"
            ],
            key="recommendation_level"
        )

        recommendation_data = filtered_df[
            filtered_df["experience_level"]
            == recommendation_level
        ]

        if len(recommendation_data) > 0:

            career_recommendations = (
                recommendation_data
                .groupby("job_title")
                .agg(
                    Average_Salary=(
                        "salary_in_usd",
                        "mean"
                    ),
                    Demand=(
                        "salary_in_usd",
                        "count"
                    )
                )
                .reset_index()
            )

            # Normalize salary

            salary_min = (
                career_recommendations[
                    "Average_Salary"
                ].min()
            )

            salary_max = (
                career_recommendations[
                    "Average_Salary"
                ].max()
            )

            # Normalize demand

            demand_min = (
                career_recommendations[
                    "Demand"
                ].min()
            )

            demand_max = (
                career_recommendations[
                    "Demand"
                ].max()
            )

            # Salary score

            if salary_max != salary_min:

                career_recommendations[
                    "Salary_Score"
                ] = (
                    (
                        career_recommendations[
                            "Average_Salary"
                        ]
                        - salary_min
                    )
                    / (salary_max - salary_min)
                )

            else:

                career_recommendations[
                    "Salary_Score"
                ] = 1

            # Demand score

            if demand_max != demand_min:

                career_recommendations[
                    "Demand_Score"
                ] = (
                    (
                        career_recommendations[
                            "Demand"
                        ]
                        - demand_min
                    )
                    / (demand_max - demand_min)
                )

            else:

                career_recommendations[
                    "Demand_Score"
                ] = 1

            # Combined Career Score

            career_recommendations[
                "Career_Score"
            ] = (
                career_recommendations[
                    "Salary_Score"
                ] * 0.6
                +
                career_recommendations[
                    "Demand_Score"
                ] * 0.4
            ) * 100

            # Top 10 careers

            career_recommendations = (
                career_recommendations
                .sort_values(
                    "Career_Score",
                    ascending=False
                )
                .head(10)
            )

            # Round values

            career_recommendations[
                "Average_Salary"
            ] = (
                career_recommendations[
                    "Average_Salary"
                ].round(0)
            )

            career_recommendations[
                "Career_Score"
            ] = (
                career_recommendations[
                    "Career_Score"
                ].round(1)
            )

            st.dataframe(
                career_recommendations[
                    [
                        "job_title",
                        "Average_Salary",
                        "Demand",
                        "Career_Score"
                    ]
                ],
                use_container_width=True,
                hide_index=True,
                column_config={

                    "job_title": "💼 Career",

                    "Average_Salary":
                        st.column_config.NumberColumn(
                            "💰 Average Salary",
                            format="$%d"
                        ),

                    "Demand": "🔥 Demand",

                    "Career_Score":
                        st.column_config.NumberColumn(
                            "🎯 Career Score",
                            format="%.1f"
                        )
                }
            )

        else:

            st.info(
                "Not enough data for this experience level."
            )

    else:

        st.warning(
            "⚠️ Select records using the sidebar filters first."
        )

    

    
# ---------------------------------------------------------
# TAB 4 — DATASET STUDIO
# ---------------------------------------------------------

with tab4:

    st.markdown("## 🗂️ Dataset Studio")
    st.caption(
        "Inspect, explore and download the salary dataset."
    )

    # =====================================================
    # ML SALARY PREDICTOR
    # =====================================================

    st.markdown("## 🤖 ML Salary Predictor")

    st.caption(
        "Predict an estimated salary based on career and work-related factors."
    )

    col1, col2 = st.columns(2)

    with col1:

        selected_job = st.selectbox(
            "💼 Job Title",
            sorted(df["job_title"].dropna().unique())
        )

        selected_experience = st.selectbox(
            "📈 Experience Level",
            sorted(df["experience_level"].dropna().unique())
        )

        selected_employment = st.selectbox(
            "💼 Employment Type",
            sorted(df["employment_type"].dropna().unique())
        )

    with col2:

        selected_residence = st.selectbox(
            "🌎 Employee Residence",
            sorted(df["employee_residence"].dropna().unique())
        )

        selected_work_mode = st.selectbox(
            "🏠 Work Mode",
            ["On-site", "Hybrid", "Fully Remote"]
        )

        selected_year = st.selectbox(
            "📅 Work Year",
            sorted(df["work_year"].dropna().unique(), reverse=True)
        )

    if st.button("🔮 Predict Salary", use_container_width=True):

        remote_value_map = {
            "On-site": 0,
            "Hybrid": 50,
            "Fully Remote": 100
        }

        input_data = pd.DataFrame({
            "work_year": [selected_year],
            "experience_level": [selected_experience],
            "employment_type": [selected_employment],
            "job_title": [selected_job],
            "employee_residence": [selected_residence],
            "remote_ratio": [
                remote_value_map[selected_work_mode]
            ]
        })

        predicted_salary = salary_model.predict(input_data)[0]

        st.success("✅ Salary prediction generated!")

        st.metric(
            "💰 Predicted Salary",
            f"${predicted_salary:,.0f}"
        )

    # =====================================================
    # MODEL PERFORMANCE
    # =====================================================

    st.markdown("### 📊 Model Performance")

    metric_col1, metric_col2 = st.columns(2)

    with metric_col1:
        st.metric(
            "Mean Absolute Error",
            f"${mae:,.0f}"
        )

    with metric_col2:
        st.metric(
            "R² Score",
            f"{r2:.2f}"
        )

    st.caption(
        "Lower MAE indicates smaller prediction errors, while an R² value "
        "closer to 1 indicates better model fit."
    )

    # =====================================================
    # ACTUAL VS PREDICTED
    # =====================================================

    st.markdown("### 🎯 Actual vs Predicted Salary")

    prediction_df = pd.DataFrame({
        "Actual Salary": y_test.values,
        "Predicted Salary": y_pred
    })

    fig_prediction = px.scatter(
        prediction_df,
        x="Actual Salary",
        y="Predicted Salary",
        title="Actual vs Predicted Salary",
        labels={
            "Actual Salary": "Actual Salary (USD)",
            "Predicted Salary": "Predicted Salary (USD)"
        }
    )

    min_salary = min(
        prediction_df["Actual Salary"].min(),
        prediction_df["Predicted Salary"].min()
    )

    max_salary = max(
        prediction_df["Actual Salary"].max(),
        prediction_df["Predicted Salary"].max()
    )

    fig_prediction.add_shape(
    type="line",
    x0=min_salary,
    y0=min_salary,
    x1=max_salary,
    y1=max_salary,
    line=dict(
        color="red",
        dash="dash",
        width=3
    )
)

    fig_prediction.add_annotation(
    x=max_salary,
    y=max_salary,
    text="Ideal Prediction",
    showarrow=False,
    xanchor="right",
    yanchor="bottom"
)

    fig_prediction.update_traces(
        marker=dict(
            size=9,
            opacity=0.75
        )
    )

    fig_prediction.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        )
    )

    st.plotly_chart(
        fig_prediction,
        use_container_width=True
    )

    # =====================================================
    # MISSING VALUE CHECK
    # =====================================================

    st.markdown("---")
    st.markdown("### 🔎 Missing Value Analysis")

    missing_data = (
        df.isnull()
        .sum()
        .reset_index()
    )

    missing_data.columns = [
        "Column",
        "Missing Values"
    ]

    missing_data = missing_data[
        missing_data["Missing Values"] > 0
    ]

    if len(missing_data) == 0:

        st.success(
            "✅ No missing values found in the dataset."
        )

    else:

        st.warning(
            "⚠️ Missing values were found."
        )

        st.dataframe(
            missing_data,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # DATASET OVERVIEW
    # =====================================================

    st.markdown("### 📊 Dataset Overview")

    overview_col1, overview_col2, overview_col3 = st.columns(3)

    with overview_col1:
        st.metric(
            "Total Records",
            f"{len(df):,}"
        )

    with overview_col2:
        st.metric(
            "Total Columns",
            f"{len(df.columns):,}"
        )

    with overview_col3:
        duplicate_count = df.duplicated().sum()

        st.metric(
            "Duplicate Rows",
            f"{duplicate_count:,}"
        )

    st.markdown("#### Dataset Preview")

    st.dataframe(
        df.head(10),
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    st.markdown("### 🔎 Column Information")

    column_info = pd.DataFrame({
        "Column": df.columns,
        "Data Type": [
            str(dtype)
            for dtype in df.dtypes
        ],
        "Non-Null Values": [
            df[column].notna().sum()
            for column in df.columns
        ]
    })

    st.dataframe(
        column_info,
        use_container_width=True,
        hide_index=True
    )

    # =====================================================
    # DOWNLOAD DATASET
    # =====================================================

    st.markdown("### 📥 Download Data")

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="⬇️ Download Filtered Dataset",
        data=csv_data,
        file_name="salarynex_filtered_dataset.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.caption(
        f"Download the currently filtered dataset ({len(filtered_df):,} records)."
    )