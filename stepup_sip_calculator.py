import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Step-up SIP Calculator",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
    <style>
    .main {
        background-color: #1e293b !important;
    }
    .stApp {
        background-color: #0f172a !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 18px !important;
        font-weight: bold !important;
        color: #ffffff !important;
        word-wrap: break-word !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        line-height: 1.2 !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        margin-bottom: 5px !important;
    }
    div[data-testid="stMetricDelta"] {
        font-size: 14px !important;
        color: #10b981 !important;
        font-weight: 600 !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #1e293b;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 700;
        color: #94a3b8;
        font-size: 16px;
        border: 2px solid #334155;
    }
    .stTabs [aria-selected="true"] {
        background-color: #3b82f6;
        color: white !important;
        border-color: #3b82f6;
    }
    h1 {
        color: #ffffff !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 800;
    }
    h2, h3, h4 {
        color: #f1f5f9 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    p {
        color: #cbd5e1 !important;
    }
    .info-box {
        background: #1e293b;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin: 10px 0;
        border: 1px solid #334155;
    }
    /* Fix for metric boxes */
    [data-testid="metric-container"] {
        background-color: #1e293b !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 10px !important;
        padding: 15px !important;
    }
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        background-color: #1e293b !important;
    }
    /* Success/Info/Warning boxes */
    .stSuccess, .stInfo, .stWarning {
        background-color: #1e293b !important;
        color: #ffffff !important;
    }
    </style>
    """, unsafe_allow_html=True)

# Title with icon
st.markdown("<h1 style='text-align: center; color: #ffffff;'>📈 Step-up SIP Calculator</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 18px;'>Plan Your Investment Future with Precision</p>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar inputs
with st.sidebar:
    st.markdown("### 💰 Investment Details")
    
    monthly_investment = st.number_input(
        "Initial Monthly Investment (₹)",
        min_value=500,
        max_value=10000000,
        value=5000,
        step=500,
        help="The initial monthly amount you want to invest"
    )
    
    annual_stepup = st.slider(
        "Annual Step-up (%)",
        min_value=0,
        max_value=50,
        value=10,
        step=1,
        help="Percentage increase in SIP amount every year"
    )
    
    expected_return = st.slider(
        "Expected Annual Return (%)",
        min_value=1.0,
        max_value=30.0,
        value=12.0,
        step=0.5,
        help="Expected average annual return on investment"
    )
    
    investment_period = st.slider(
        "Investment Period (Years)",
        min_value=1,
        max_value=40,
        value=10,
        step=1,
        help="Duration of investment in years"
    )
    
    st.markdown("---")
    st.markdown("### 📊 Calculator Features")
    st.markdown("""
    - ✅ Banking Accuracy
    - ✅ Year-wise Breakdown
    - ✅ Interactive Charts
    - ✅ Detailed Reports
    """)

# Calculate Step-up SIP with banking accuracy
def calculate_stepup_sip(initial_investment, annual_stepup_pct, annual_return_pct, years):
    """
    Banking-accurate Step-up SIP calculation
    Uses beginning-of-month investment with monthly compounding
    """
    annual_rate = annual_return_pct / 100
    monthly_rate = (1 + annual_rate)**(1/12) - 1
    stepup_rate = annual_stepup_pct / 100
    
    total_invested = 0
    future_value = 0
    yearly_data = []
    
    current_monthly_investment = initial_investment
    
    for year in range(1, years + 1):
        year_invested = 0
        year_opening_value = future_value
        
        for month in range(12):
            # Add monthly investment at beginning of month
            year_invested += current_monthly_investment
            total_invested += current_monthly_investment
            
            # Calculate month-end value with compound interest
            future_value = (future_value + current_monthly_investment) * (1 + monthly_rate)
        
        # Calculate year-end values
        year_gain = future_value - year_opening_value - year_invested
        
        yearly_data.append({
            'Year': year,
            'Monthly SIP': round(current_monthly_investment, 2),
            'Annual Investment': round(year_invested, 2),
            'Total Invested': round(total_invested, 2),
            'Year-end Value': round(future_value, 2),
            'Annual Gain': round(year_gain, 2)
        })
        
        # Step up for next year
        current_monthly_investment = current_monthly_investment * (1 + stepup_rate)
    
    return {
        'total_invested': round(total_invested, 2),
        'future_value': round(future_value, 2),
        'total_gain': round(future_value - total_invested, 2),
        'yearly_data': yearly_data
    }

# Calculate results
results = calculate_stepup_sip(monthly_investment, annual_stepup, expected_return, investment_period)

# Display key metrics
st.markdown("## 🎯 Key Results")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Invested",
        value=f"₹{results['total_invested']:,.2f}",
        help="Total amount you will invest"
    )

with col2:
    st.metric(
        label="Future Value",
        value=f"₹{results['future_value']:,.2f}",
        help="Value at the end of investment period"
    )

with col3:
    st.metric(
        label="Total Returns",
        value=f"₹{results['total_gain']:,.2f}",
        delta=f"{(results['total_gain']/results['total_invested']*100):.2f}%",
        help="Profit from your investment"
    )

with col4:
    final_monthly = monthly_investment * ((1 + annual_stepup/100) ** (investment_period - 1))
    st.metric(
        label="Final Monthly SIP",
        value=f"₹{final_monthly:,.2f}",
        help="Monthly investment in the last year"
    )

st.markdown("---")

# Create tabs for different views
tab1, tab2, tab3 = st.tabs(["📊 Charts", "📋 Year-wise Details", "📈 Analysis"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        # Pie chart - Investment vs Returns
        fig_pie = go.Figure(data=[go.Pie(
            labels=['Invested', 'Returns'],
            values=[results['total_invested'], results['total_gain']],
            marker=dict(colors=['#3b82f6', '#10b981']),
            hole=0.4,
            textinfo='label+percent+value',
            textfont=dict(size=16, color='black', family='Arial Black'),
            hovertemplate='<b>%{label}</b><br>₹%{value:,.2f}<br>%{percent}<extra></extra>'
        )])
        
        fig_pie.update_layout(
            title={
                'text': 'Investment vs Returns',
                'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial Black'}
            },
            height=400,
            showlegend=True,
            legend=dict(font=dict(size=16, color='#ffffff')),
            paper_bgcolor='#1e293b',
            plot_bgcolor='#1e293b',
            font=dict(color='#ffffff')
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        # Growth chart
        df = pd.DataFrame(results['yearly_data'])
        
        fig_growth = go.Figure()
        
        fig_growth.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Total Invested'],
            mode='lines+markers',
            name='Total Invested',
            line=dict(color='#3b82f6', width=4),
            marker=dict(size=10, color='#3b82f6'),
            fill='tonexty'
        ))
        
        fig_growth.add_trace(go.Scatter(
            x=df['Year'],
            y=df['Year-end Value'],
            mode='lines+markers',
            name='Total Value',
            line=dict(color='#10b981', width=4),
            marker=dict(size=10, color='#10b981'),
            fill='tonexty'
        ))
        
        fig_growth.update_layout(
            title={
                'text': 'Investment Growth Over Time',
                'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial Black'}
            },
            xaxis=dict(
                title=dict(text='Year', font=dict(size=16, color='#ffffff')),
                tickfont=dict(size=14, color='#cbd5e1'),
                gridcolor='#334155'
            ),
            yaxis=dict(
                title=dict(text='Amount (₹)', font=dict(size=16, color='#ffffff')),
                tickfont=dict(size=14, color='#cbd5e1'),
                gridcolor='#334155'
            ),
            height=400,
            hovermode='x unified',
            legend=dict(
                font=dict(size=16, color='#ffffff'),
                bgcolor='rgba(30, 41, 59, 0.8)',
                bordercolor='#3b82f6',
                borderwidth=2
            ),
            paper_bgcolor='#1e293b',
            plot_bgcolor='#0f172a',
            font=dict(color='#ffffff')
        )
        st.plotly_chart(fig_growth, use_container_width=True)
    
    # Bar chart - Yearly SIP amounts
    fig_bar = go.Figure()
    
    fig_bar.add_trace(go.Bar(
        x=df['Year'],
        y=df['Monthly SIP'],
        name='Monthly SIP',
        marker=dict(
            color='#8b5cf6',
            line=dict(color='#6d28d9', width=2)
        ),
        text=df['Monthly SIP'].apply(lambda x: f'₹{x:,.0f}'),
        textposition='outside',
        textfont=dict(size=14, color='#1e3a8a', family='Arial Black')
    ))
    
    fig_bar.update_layout(
        title={
            'text': 'Monthly SIP Amount Year-wise',
            'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial Black'}
        },
        xaxis=dict(
            title=dict(text='Year', font=dict(size=16, color='#ffffff')),
            tickfont=dict(size=14, color='#cbd5e1'),
            gridcolor='#334155'
        ),
        yaxis=dict(
            title=dict(text='Monthly SIP (₹)', font=dict(size=16, color='#ffffff')),
            tickfont=dict(size=14, color='#cbd5e1'),
            gridcolor='#334155'
        ),
        height=400,
        showlegend=False,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#0f172a',
        font=dict(color='#ffffff')
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab2:
    st.markdown("### 📅 Year-wise Detailed Breakdown")
    
    df_display = pd.DataFrame(results['yearly_data'])
    
    # Format numbers for display
    for col in df_display.columns:
        if col != 'Year':
            df_display[col] = df_display[col].apply(lambda x: f"₹{x:,.2f}")
    
    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )
    
    # Download button
    csv = pd.DataFrame(results['yearly_data']).to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"stepup_sip_calculation_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv",
    )

with tab3:
    st.markdown("### 🔍 Analysis & Financial Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown("#### 💡 Key Findings")
        
        absolute_return = (results['total_gain'] / results['total_invested']) * 100
        
        st.write(f"**Absolute Return:** {absolute_return:.2f}%")
        st.write(f"**First Year Investment:** ₹{monthly_investment * 12:,.2f}")
        st.write(f"**Last Year Investment:** ₹{monthly_investment * 12 * ((1 + annual_stepup/100) ** (investment_period - 1)):,.2f}")
        st.write(f"**Average Annual Returns:** ₹{results['total_gain'] / investment_period:,.2f}")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='info-box'>", unsafe_allow_html=True)
        st.markdown("#### 📝 Recommendations")
        
        absolute_return = (results['total_gain'] / results['total_invested']) * 100
        
        if absolute_return > 100:
            st.success("✅ Excellent returns! Your investment more than doubled!")
        elif absolute_return > 50:
            st.info("👍 Good returns on your investment!")
        else:
            st.warning("⚠️ Consider increasing investment period")
        
        if annual_stepup >= 10:
            st.success("✅ Good step-up rate! Higher savings!")
        
        st.info(f"💰 After {investment_period} years, you will have **₹{results['future_value']:,.2f}**!")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Comparison chart
    st.markdown("#### 📊 Comparison with Different Scenarios")
    
    scenarios = {
        'Current Plan': results['future_value'],
        'Without Step-up': calculate_stepup_sip(monthly_investment, 0, expected_return, investment_period)['future_value'],
        '5% Higher Returns': calculate_stepup_sip(monthly_investment, annual_stepup, expected_return + 5, investment_period)['future_value'],
        '5 More Years': calculate_stepup_sip(monthly_investment, annual_stepup, expected_return, investment_period + 5)['future_value']
    }
    
    fig_comparison = go.Figure(data=[
        go.Bar(
            x=list(scenarios.keys()),
            y=list(scenarios.values()),
            marker=dict(
                color=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'],
                line=dict(color='#ffffff', width=2)
            ),
            text=[f'₹{v:,.0f}' for v in scenarios.values()],
            textposition='outside',
            textfont=dict(size=16, color='#ffffff', family='Arial Black'),
            textangle=0
        )
    ])
    
    fig_comparison.update_layout(
        title={
            'text': 'Future Value in Different Scenarios',
            'font': {'size': 22, 'color': '#ffffff', 'family': 'Arial Black'}
        },
        xaxis=dict(
            title=dict(text='Scenario', font=dict(size=16, color='#ffffff')),
            tickfont=dict(size=15, color='#ffffff'),
            tickangle=-15
        ),
        yaxis=dict(
            title=dict(text='Future Value (₹)', font=dict(size=16, color='#ffffff')),
            tickfont=dict(size=14, color='#ffffff'),
            gridcolor='#334155'
        ),
        height=450,
        paper_bgcolor='#1e293b',
        plot_bgcolor='#0f172a',
        font=dict(color='#ffffff'),
        margin=dict(b=100)
    )
    st.plotly_chart(fig_comparison, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #94a3b8; padding: 20px;'>
    <p><strong>⚠️ Important Note:</strong> This calculator is for educational purposes only. Actual returns may vary.</p>
    <p>Please consult a financial advisor before making investment decisions.</p>
    <p style='margin-top: 10px;'>© 2024 Step-up SIP Calculator | Made with ❤️</p>
</div>
""", unsafe_allow_html=True)