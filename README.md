````

---

## 📁 Repository Architecture

```text
.
├── Week_01_02_Data_Cleaning_EDA/
│   ├── data/                           # Raw & cleaned dataset storage (E-commerce, Netflix)
│   ├── notebooks/                      # Data_Cleaning_EDA_Pipeline.ipynb
│   └── docs/                           # One_Page_Summary_Report.pdf
├── Week_03_SQL_Querying/
│   ├── scripts/                        # Chinook_AdventureWorks_Queries.sql
│   └── docs/                           # Query_Insights_Document.pdf
├── Week_04_BI_Dashboarding/
│   ├── dashboards/                     # Superstore_Sales_Dashboard.pbix
│   └── presentation/                   # Strategic_KPI_Presentation.pdf
├── Week_05_Business_Case_Study/
│   ├── reports/                        # Executive_Case_Study_Report.pdf
│   └── presentation/                   # Business_Presentation_Slides.pdf
├── Week_06_Advanced_Python_TimeSeries/
│   ├── notebooks/                      # AAPL_Stock_Feature_Engineering.ipynb
│   └── reports/                        # Financial_Trend_Summary.pdf
├── Week_07_ETL_Pipelines_Automation/
│   ├── pipeline/                       # weather_etl_pipeline.py
│   └── docs/                           # README.md & Demo_Video_Link.txt
└── Week_08_Final_Capstone/
    ├── dashboards/                     # WDI_Global_Development_Dashboard.pbix
    ├── reports/                        # Final_Capstone_Analytical_Report.pdf
    └── README.md                       # Comprehensive Capstone Documentation
````

## 🛠️ Detailed Weekly Track & Technical Executions

### 🔍 Weeks 1 & 2: Data Cleaning & Exploratory Data Analysis (EDA)

- **Objective:** Ingest, clean, validate, and isolate patterns from structurally compromised raw datasets.
    
- **Datasets Evaluated:** 1. _E-commerce Retail Transactions Dataset_ (Kaggle)
    
    2. _Netflix Movies & TV Shows Dataset_ (Kaggle)
    
- **Core Tasks Executed:**
    
    - **Data Profile & Schema Auditing:** Implemented programmatic schema exploration using Pandas (`shape`, `dtypes`, primary key constraints profiling).
        
    - **Data Cleaning Rigor:** Quantified, handled, and strategically justified missing value treatments; removed duplicate entries; standardized inconsistent dates, text housing (case uniformity), and schema names.
        
    - **EDA & Summary Statistics:** Evaluated full matrix central tendency metrics (Mean, Median, Std Dev, Min/Max). Executed $\ge 5$ targeted thematic breakdowns per dataset (e.g., Top revenue countries, monthly sales spikes, Netflix content distribution velocity).
        
- **Deliverables Included:** Cleaned `.csv` output matrices, annotated `.ipynb` pipeline, and an explicit Execution Summary Report.
    

### 🗄️ Week 3: SQL & Relational Data Querying

- **Objective:** Author scalable, optimized SQL architecture to extract business intelligence from complex relational databases.
    
- **Environments & Datasets:** PostgreSQL / MySQL utilizing _Chinook (Music Store)_ and _AdventureWorks Lite_ relational schemas.
    
- **Core Tasks Executed:**
    
    - **Database Setup:** Normalized schemas, verified primary/foreign constraints, and mapped Entity-Relationship Diagrams (ERD).
        
    - **Advanced Query Operations:** Created window operations (`ROW_NUMBER()`, `RANK() OVER (PARTITION BY ...)`), multi-tier relational joins (`INNER`, `LEFT`, `RIGHT`), nested subqueries, and conditional aggregate filters (`GROUP BY`, `HAVING`).
        
    - **Optimization:** Applied indexing paradigms to minimize query execution overhead on large transactional records.
        
- **Deliverables Included:** Production-ready `.sql` script files and a deep-dive Query Insight Document.
    

### 📊 Week 4: Data Visualization & Interactive Dashboarding

- **Objective:** Model and implement executive-ready business intelligence dashboards utilizing industry standard platforms.
    
- **Tools & Datasets:** Microsoft Power BI / Tableau using _Global Superstore Sales_ or _Johns Hopkins COVID-19 Trend Dataset_.
    
- **Core Tasks Executed:**
    
    - **KPI Engineering:** Designed and isolated primary high-level metrics (Total Revenue, Profit Margin, Sales Growth, Case Recovery Rates).
        
    - **Interactive Controls:** Developed custom dimensional filters, slicing hierarchies, dynamic trend cross-filtering, and granular location drill-downs.
        
    - **Data Storytelling Layout:** Applied rigorous visual hierarchy layouts, maintaining desaturated, professional color palettes to optimize stakeholder comprehension.
        
- **Deliverables Included:** Interactive `.pbix` / `.twb` files and a 5–10 slide strategic presentation.
    

### 📈 Week 5: Business Analytics Case Study

- **Objective:** Apply rigorous diagnostic and prescriptive analytics workflows to unpack real-world enterprise operational bottlenecks.
    
- **Case Selected:** _Telco Customer Churn_ OR _Bank Direct Marketing Campaign Optimization_.
    
- **Core Tasks Executed:**
    
    - **Operational Diagnostic Modeling:** Outlined underlying business problem statements and assessed demographic, behavioral, and operational variables via correlation matrices and distribution box-plots.
        
    - **Driver Identification:** Isolated key customer churn/subscription indicators (e.g., contract types, charges, historic campaign touchpoints).
        
    - **Prescriptive Recommendations:** Designed 3–5 highly specific, data-validated actionable strategies (retention pathways, targeted loyalty frameworks, tailored campaign profiles).
        
- **Deliverables Included:** Formal 3–5 Page Management Case Report and a streamlined Stakeholder Slide Deck.
    

### 🐍 Week 6: Advanced Python Analysis & Feature Engineering

- **Objective:** Execute complex time-series transformations and programmatically engineer features on volatile financial market streams.
    
- **Dataset:** Apple Inc. (AAPL) Historical Stock Data extracted via `yfinance`.
    
- **Core Tasks Executed:**
    
    - **Time-Series Transformation:** Managed complex date/time indexes, implemented rolling statistical boundaries (7-day, 30-day moving averages), and performed multi-interval percentage change calculations.
        
    - **Feature Engineering Execution:** Programmatically generated new analytical features including Daily Price Deltas, Rolling Volatility Indices, and Normalized Monthly Returns.
        
    - **Visualizations:** Created interactive multi-axis time plots tracking Close Price vs. Volume and Bollinger-band style moving average channels.
        
- **Deliverables Included:** Structured `.ipynb` research notebook and a concise Financial Trend Summary.
    

### ⚙️ Week 7: Data Pipelines & Automated ETL Architectures

- **Objective:** Construct a fully automated end-to-end Extract, Transform, Load (ETL) pipeline harvesting live streaming data.
    
- **Data Source & Core Tools:** Python (`requests`, `pandas`), OpenWeather API, and local database storage (SQLite/CSV).
    
- **Core Tasks Executed:**
    
    - **Automated Extraction:** Constructed an authenticated programmatic interface connecting to the OpenWeather API to parse real-time environmental metrics for multi-city vectors.
        
    - **Structural Transformation:** Standardized JSON objects into normalized Pandas DataFrames, handling type casting, field remapping, and metric standardization.
        
    - **Target Load Execution:** Configured automated loading routines into local SQLite databases and structured CSV formats.
        
- **Deliverables Included:** Automated ETL `.py` scripts, GitHub codebase architecture, a comprehensive `README.md`, and an organic project demo video walking through execution steps.
    

### 🌍 Week 8: Data Analytics Capstone Project (Final)

- **Objective:** Orchestrate the complete end-to-end data analytics workflow on a multi-dimensional macro-level public policy framework.
    
- **Dataset:** World Bank's World Development Indicators (WDI) — encompassing global economic, environmental, and infrastructure telemetry.
    
- **Core Tasks Executed:**
    
    - **Thematic Specialization:** Formulated a specific developmental hypothesis tracking multi-decade socio-economic indicators across nations.
        
    - **Analytical Rigor & BI Modeling:** Engineered a complex corporate-grade Power BI multi-page dashboard, mapping core thematic KPIs, time-series projections, and regional statistical comparisons.
        
    - **Comprehensive C-Suite Communication:** Structured a formal academic-grade PDF research paper documenting the core methodology, data transformation protocols, and actionable, systemic global recommendations.
        
- **Deliverables Included:** Technical `.pbix` dashboard file, peer-reviewed Final Project Report (PDF), modular GitHub ecosystem, and an end-to-end recorded 5-10 minute executive presentation.
    

## 🚀 Key Certifications & Technical Proficiencies Gained

- **Languages & Libraries:** Python (Pandas, NumPy, Requests, Matplotlib, Seaborn, yfinance), SQL (PostgreSQL, MySQL).
    
- **BI & Workflow Automation:** Microsoft Power BI, Tableau, Git/GitHub, ETL Pipeline Architecture.
    
- **Domain Expertise:** Exploratory Data Analysis (EDA), Statistical Profiling, Time-Series Forecasting, Feature Engineering, Metric/KPI Modeling, Strategic Reporting.
    

## 🤝 Acknowledgments

Special thanks to the instructors, mentors, and program coordinators at **AnalystLab Africa** for providing a world-class, rigorous framework to develop professional data analytics capabilities during Batch B.

_Note: To review specific project code, dashboards, or executive reports, browse into the corresponding directory tracks listed above._