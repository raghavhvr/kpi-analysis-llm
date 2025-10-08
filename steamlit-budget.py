import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import warnings
import random

# Professional styling imports
try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, PageBreak, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.lib import colors
    HAS_REPORTLAB = True
except ImportError:
    HAS_REPORTLAB = False

warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Campaign Trends Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_marketing_color_scheme():
    """Professional marketing color scheme with readable text"""
    return {
        'primary': '#1E88E5',      # Marketing blue
        'secondary': '#FFC107',    # Conversion yellow  
        'success': '#4CAF50',      # Profitable green
        'warning': '#FF5722',      # Overspend red
        'accent': '#9C27B0',       # Premium purple
        'background': '#FFFFFF',   # White
        'text': '#000000',         # Black for maximum readability
        'grid': '#CCCCCC',         # Medium gray for visible grid
        'gradient': ['#1E88E5', '#43A047', '#FB8C00', '#E53935', '#8E24AA', '#00ACC1', '#7CB342', '#FDD835']
    }

def apply_marketing_styling(fig, chart_type='default'):
    """Apply marketing-focused styling to charts with readable text"""
    colors = get_marketing_color_scheme()
    
    marketing_layout = {
        'template': 'plotly_white',
        'font': {
            'family': 'Arial, sans-serif', 
            'size': 13,  # Larger font
            'color': colors['text']  # Black text
        },
        'title': {
            'font': {
                'family': 'Arial, sans-serif', 
                'size': 18,  # Larger title
                'color': colors['text'],  # Black text
            },
            'x': 0.5, 
            'xanchor': 'center'
        },
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'showlegend': True,
        'legend': {
            'font': {'size': 12, 'color': colors['text']},  # Larger, black legend text
            'bgcolor': 'rgba(255,255,255,0.95)',
            'bordercolor': '#333333',
            'borderwidth': 1
        },
        'margin': {'l': 70, 'r': 50, 't': 80, 'b': 100}  # More margin for labels
    }
    
    if chart_type == 'performance':
        # Performance charts get vibrant colors
        fig.update_traces(marker_color=colors['gradient'])
    elif chart_type == 'budget':
        # Budget charts get financial colors - conditional on data
        try:
            if hasattr(fig.data[0], 'y') and len(fig.data[0].y) > 0:
                bar_colors = [colors['warning'] if i % 2 == 0 else colors['success'] for i in range(len(fig.data[0].y))]
                fig.update_traces(marker_color=bar_colors)
        except:
            fig.update_traces(marker_color=colors['primary'])
    elif chart_type == 'trend':
        # Trend lines get vibrant primary colors
        for i, trace in enumerate(fig.data):
            color = colors['gradient'][i % len(colors['gradient'])]
            fig.update_traces(line=dict(color=color, width=3), selector=dict(name=trace.name))
    
    fig.update_layout(**marketing_layout)
    
    # Dark, visible axes
    fig.update_xaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=colors['grid'],
        showline=True,
        linewidth=2,
        linecolor='#333333',  # Dark axis line
        title_font=dict(size=14, color=colors['text']),  # Black axis title
        tickfont=dict(size=12, color=colors['text'])  # Black tick labels
    )
    
    fig.update_yaxes(
        showgrid=True, 
        gridwidth=1, 
        gridcolor=colors['grid'],
        showline=True,
        linewidth=2,
        linecolor='#333333',  # Dark axis line
        title_font=dict(size=14, color=colors['text']),  # Black axis title
        tickfont=dict(size=12, color=colors['text'])  # Black tick labels
    )
    
    return fig

def generate_sample_campaign_data():
    """Generate realistic sample campaign data for demo"""
    np.random.seed(42)  # For reproducible results
    
    campaigns = ['Google Search', 'Facebook Ads', 'Instagram Stories', 'YouTube Video', 'LinkedIn Sponsored', 'Twitter Promoted']
    channels = ['Search', 'Social', 'Social', 'Video', 'Professional', 'Social']
    
    # Generate 90 days of data
    dates = pd.date_range(start='2024-01-01', periods=90, freq='D')
    
    data = []
    for date in dates:
        for i, campaign in enumerate(campaigns):
            # Simulate realistic campaign performance with trends
            day_of_period = (date - dates[0]).days
            seasonal_factor = 1 + 0.2 * np.sin(2 * np.pi * day_of_period / 30)  # Monthly cycles
            
            base_impressions = np.random.normal(5000 + i * 1000, 1000) * seasonal_factor
            base_clicks = base_impressions * np.random.normal(0.02 + i * 0.005, 0.005)
            base_conversions = base_clicks * np.random.normal(0.05 + i * 0.01, 0.01)
            
            # Budget calculations
            daily_budget = np.random.normal(200 + i * 50, 30)
            cpc = np.random.normal(1.5 + i * 0.3, 0.3)
            actual_spend = min(base_clicks * cpc, daily_budget * 1.1)  # Sometimes overspend
            
            data.append({
                'Date': date,
                'Campaign': campaign,
                'Channel': channels[i],
                'Impressions': max(0, int(base_impressions)),
                'Clicks': max(0, int(base_clicks)),
                'Conversions': max(0, int(base_conversions)),
                'Budget': round(daily_budget, 2),
                'Spend': round(actual_spend, 2),
                'CTR': round((base_clicks / base_impressions) * 100, 2) if base_impressions > 0 else 0,
                'CPC': round(cpc, 2),
                'CPA': round(actual_spend / base_conversions, 2) if base_conversions > 0 else 0,
                'Conversion_Rate': round((base_conversions / base_clicks) * 100, 2) if base_clicks > 0 else 0
            })
    
    return pd.DataFrame(data)

class CampaignAnalyzer:
    def __init__(self):
        self.data = None
        self.analysis_results = {}
        
    def load_data(self, data):
        """Load campaign data"""
        self.data = data
        if 'Date' in data.columns:
            self.data['Date'] = pd.to_datetime(self.data['Date'])
        
    def calculate_key_metrics(self):
        """Calculate key marketing metrics"""
        if self.data is None:
            return {}
        
        total_spend = self.data['Spend'].sum()
        total_budget = self.data['Budget'].sum()
        total_impressions = self.data['Impressions'].sum()
        total_clicks = self.data['Clicks'].sum()
        total_conversions = self.data['Conversions'].sum()
        
        metrics = {
            'total_spend': total_spend,
            'total_budget': total_budget,
            'budget_utilization': (total_spend / total_budget * 100) if total_budget > 0 else 0,
            'budget_variance': total_spend - total_budget,
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'total_conversions': total_conversions,
            'overall_ctr': (total_clicks / total_impressions * 100) if total_impressions > 0 else 0,
            'overall_cpc': (total_spend / total_clicks) if total_clicks > 0 else 0,
            'overall_cpa': (total_spend / total_conversions) if total_conversions > 0 else 0,
            'overall_conversion_rate': (total_conversions / total_clicks * 100) if total_clicks > 0 else 0,
            'roas': (total_conversions * 50 / total_spend) if total_spend > 0 else 0  # Assuming $50 value per conversion
        }
        
        return metrics
    
    def create_performance_overview(self):
        """Create comprehensive performance overview charts"""
        charts = []
        
        if self.data is None:
            return charts
        
        # 1. Budget vs Spend Analysis with Reconciliation
        budget_data = self.data.groupby('Campaign').agg({
            'Budget': 'sum',
            'Spend': 'sum'
        }).reset_index()
        budget_data['Variance'] = budget_data['Spend'] - budget_data['Budget']
        budget_data['Utilization'] = (budget_data['Spend'] / budget_data['Budget'] * 100).round(1)
        budget_data['Variance_Pct'] = ((budget_data['Variance'] / budget_data['Budget']) * 100).round(1)
        
        # Sort by variance to show problem areas first
        budget_data = budget_data.sort_values('Variance', ascending=False)
        
        # Create grouped bar chart with variance coloring
        fig1 = go.Figure()
        
        # Add budget bars
        fig1.add_trace(go.Bar(
            name='Allocated Budget',
            x=budget_data['Campaign'],
            y=budget_data['Budget'],
            marker_color='#2196F3',  # Blue for budget
            opacity=0.7,
            text=budget_data['Budget'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        
        # Add spend bars with conditional coloring
        spend_colors = ['#F44336' if var > 0 else '#4CAF50' for var in budget_data['Variance']]
        
        fig1.add_trace(go.Bar(
            name='Actual Spend',
            x=budget_data['Campaign'],
            y=budget_data['Spend'],
            marker_color=spend_colors,
            text=budget_data['Spend'].apply(lambda x: f'${x:,.0f}'),
            textposition='outside'
        ))
        
        # Add variance annotations
        for i, row in budget_data.iterrows():
            variance_text = f"${row['Variance']:,.0f}<br>({row['Variance_Pct']:+.1f}%)"
            variance_color = 'red' if row['Variance'] > 0 else 'green'
            
            fig1.add_annotation(
                x=row['Campaign'],
                y=max(row['Budget'], row['Spend']) * 1.15,
                text=variance_text,
                showarrow=False,
                font=dict(size=11, color=variance_color, family='Arial')
            )
        
        fig1.update_layout(
            title='💰 Budget Reconciliation: Allocated vs Actual Spend',
            barmode='group',
            yaxis_title='Amount ($)',
            xaxis_title='Campaign',
            height=500
        )
        fig1 = apply_marketing_styling(fig1, 'budget')
        
        # Calculate reconciliation insights
        total_variance = budget_data['Variance'].sum()
        overspend_campaigns = budget_data[budget_data['Variance'] > 0]
        underspend_campaigns = budget_data[budget_data['Variance'] < 0]
        
        reconciliation_insight = f"""Budget Reconciliation Summary:
        • {len(overspend_campaigns)} campaigns exceeded budget (total overspend: ${overspend_campaigns['Variance'].sum():,.2f})
        • {len(underspend_campaigns)} campaigns under budget (total underspend: ${abs(underspend_campaigns['Variance'].sum()):,.2f})
        • Net variance: ${total_variance:,.2f} ({'over' if total_variance > 0 else 'under'} budget)
        • Worst offender: {overspend_campaigns.iloc[0]['Campaign'] if len(overspend_campaigns) > 0 else 'None'} ({overspend_campaigns.iloc[0]['Variance_Pct'] if len(overspend_campaigns) > 0 else 0:+.1f}%)"""
        
        charts.append({
            'title': 'Budget Reconciliation Analysis',
            'figure': fig1,
            'insight': reconciliation_insight
        })
        
        # 2. Campaign Performance Trends
        daily_performance = self.data.groupby('Date').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Conversions': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        daily_performance['CTR'] = (daily_performance['Clicks'] / daily_performance['Impressions'] * 100).round(2)
        daily_performance['CPC'] = (daily_performance['Spend'] / daily_performance['Clicks']).round(2)
        
        fig2 = make_subplots(rows=2, cols=2, 
                            subplot_titles=('Daily Impressions & Clicks', 'Click-Through Rate Trend', 
                                          'Daily Conversions', 'Daily Spend'),
                            specs=[[{'secondary_y': True}, {'secondary_y': False}],
                                   [{'secondary_y': False}, {'secondary_y': False}]])
        
        # Impressions and Clicks
        fig2.add_trace(go.Scatter(x=daily_performance['Date'], y=daily_performance['Impressions'], 
                                 name='Impressions', line=dict(color='blue')), row=1, col=1)
        fig2.add_trace(go.Scatter(x=daily_performance['Date'], y=daily_performance['Clicks'], 
                                 name='Clicks', line=dict(color='orange'), yaxis='y2'), row=1, col=1, secondary_y=True)
        
        # CTR Trend
        fig2.add_trace(go.Scatter(x=daily_performance['Date'], y=daily_performance['CTR'], 
                                 name='CTR %', line=dict(color='green')), row=1, col=2)
        
        # Conversions
        fig2.add_trace(go.Scatter(x=daily_performance['Date'], y=daily_performance['Conversions'], 
                                 name='Conversions', line=dict(color='purple')), row=2, col=1)
        
        # Spend
        fig2.add_trace(go.Scatter(x=daily_performance['Date'], y=daily_performance['Spend'], 
                                 name='Spend', line=dict(color='red')), row=2, col=2)
        
        fig2.update_layout(title='Campaign Performance Trends Over Time', height=600)
        fig2 = apply_marketing_styling(fig2, 'trend')
        
        # Calculate trend insights
        recent_ctr = daily_performance['CTR'].tail(7).mean()
        early_ctr = daily_performance['CTR'].head(7).mean()
        ctr_change = ((recent_ctr - early_ctr) / early_ctr * 100) if early_ctr > 0 else 0
        
        charts.append({
            'title': 'Performance Trends Dashboard',
            'figure': fig2,
            'insight': f"Your CTR has {'improved' if ctr_change > 0 else 'declined'} by {abs(ctr_change):.1f}% over the analysis period. Recent 7-day average CTR is {recent_ctr:.2f}%, compared to {early_ctr:.2f}% at the start."
        })
        
        # 3. Channel Performance Comparison
        channel_performance = self.data.groupby('Channel').agg({
            'Impressions': 'sum',
            'Clicks': 'sum',
            'Conversions': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        channel_performance['CTR'] = (channel_performance['Clicks'] / channel_performance['Impressions'] * 100).round(2)
        channel_performance['CPC'] = (channel_performance['Spend'] / channel_performance['Clicks']).round(2)
        channel_performance['CPA'] = (channel_performance['Spend'] / channel_performance['Conversions']).round(2)
        channel_performance['Conv_Rate'] = (channel_performance['Conversions'] / channel_performance['Clicks'] * 100).round(2)
        
        fig3 = make_subplots(rows=2, cols=2,
                            subplot_titles=('CTR by Channel', 'CPC by Channel', 
                                          'Conversion Rate by Channel', 'Total Spend by Channel'))
        
        fig3.add_trace(go.Bar(x=channel_performance['Channel'], y=channel_performance['CTR'], 
                             name='CTR %', marker_color='lightgreen'), row=1, col=1)
        fig3.add_trace(go.Bar(x=channel_performance['Channel'], y=channel_performance['CPC'], 
                             name='CPC $', marker_color='lightcoral'), row=1, col=2)
        fig3.add_trace(go.Bar(x=channel_performance['Channel'], y=channel_performance['Conv_Rate'], 
                             name='Conv Rate %', marker_color='lightblue'), row=2, col=1)
        fig3.add_trace(go.Bar(x=channel_performance['Channel'], y=channel_performance['Spend'], 
                             name='Spend $', marker_color='gold'), row=2, col=2)
        
        fig3.update_layout(title='Channel Performance Comparison', height=600, showlegend=False)
        fig3 = apply_marketing_styling(fig3, 'performance')
        
        # Find best performing channel
        best_ctr_channel = channel_performance.loc[channel_performance['CTR'].idxmax(), 'Channel']
        best_ctr_value = channel_performance['CTR'].max()
        lowest_cpc_channel = channel_performance.loc[channel_performance['CPC'].idxmin(), 'Channel']
        lowest_cpc_value = channel_performance['CPC'].min()
        
        charts.append({
            'title': 'Channel Performance Analysis',
            'figure': fig3,
            'insight': f"{best_ctr_channel} delivers your highest CTR at {best_ctr_value:.2f}%, while {lowest_cpc_channel} offers the most cost-efficient clicks at ${lowest_cpc_value:.2f} per click. This suggests different channels excel in different areas of your funnel."
        })
        
        # 4. Budget Utilization Timeline with Reconciliation Zones
        budget_timeline = self.data.groupby(['Date', 'Campaign']).agg({
            'Budget': 'sum',
            'Spend': 'sum'
        }).reset_index()
        
        budget_timeline['Utilization'] = (budget_timeline['Spend'] / budget_timeline['Budget'] * 100).round(1)
        budget_timeline_pivot = budget_timeline.pivot(index='Date', columns='Campaign', values='Utilization')
        
        fig4 = go.Figure()
        
        # Add performance zones (background shading)
        fig4.add_hrect(y0=0, y1=80, fillcolor="lightcoral", opacity=0.1, 
                      annotation_text="Under-utilized", annotation_position="left")
        fig4.add_hrect(y0=80, y1=100, fillcolor="lightgreen", opacity=0.1,
                      annotation_text="Target Zone", annotation_position="left")
        fig4.add_hrect(y0=100, y1=max(budget_timeline['Utilization'].max(), 120), fillcolor="lightyellow", opacity=0.15,
                      annotation_text="Over Budget", annotation_position="left")
        
        # Add campaign lines
        for campaign in budget_timeline_pivot.columns:
            fig4.add_trace(go.Scatter(
                x=budget_timeline_pivot.index, 
                y=budget_timeline_pivot[campaign], 
                name=campaign, 
                mode='lines',
                line=dict(width=2)
            ))
        
        # Add reference lines
        fig4.add_hline(y=100, line_dash="solid", line_color="red", line_width=2,
                      annotation_text="100% Budget Limit", annotation_position="right")
        fig4.add_hline(y=90, line_dash="dot", line_color="orange", line_width=1,
                      annotation_text="90% Efficiency Target", annotation_position="right")
        
        fig4.update_layout(
            title='📈 Daily Budget Utilization Timeline & Reconciliation', 
            yaxis_title='Budget Utilization (%)',
            xaxis_title='Date',
            height=500
        )
        fig4 = apply_marketing_styling(fig4, 'budget')
        
        # Calculate budget timeline insights
        avg_utilization = budget_timeline['Utilization'].mean()
        overspend_days = len(budget_timeline[budget_timeline['Utilization'] > 100])
        underspend_days = len(budget_timeline[budget_timeline['Utilization'] < 80])
        total_days = len(budget_timeline)
        
        timeline_insight = f"""Budget Control Analysis:
        • Average utilization: {avg_utilization:.1f}%
        • Over budget: {overspend_days} out of {total_days} campaign-days ({overspend_days/total_days*100:.1f}%)
        • Under-utilized: {underspend_days} campaign-days ({underspend_days/total_days*100:.1f}%)
        • Budget discipline: {'Excellent' if overspend_days/total_days < 0.05 else 'Good' if overspend_days/total_days < 0.15 else 'Needs Improvement'}"""
        
        charts.append({
            'title': 'Budget Utilization Timeline',
            'figure': fig4,
            'insight': timeline_insight
        })
        
        return charts
    
    def generate_executive_summary(self):
        """Generate executive summary with key insights"""
        if self.data is None:
            return "No data available for analysis."
        
        metrics = self.calculate_key_metrics()
        
        # Performance insights
        if metrics['budget_utilization'] > 105:
            budget_insight = f"Budget management needs attention - you're {metrics['budget_utilization']:.1f}% over budget (${abs(metrics['budget_variance']):,.2f} overspend)."
        elif metrics['budget_utilization'] < 85:
            budget_insight = f"You're under-utilizing your budget at {metrics['budget_utilization']:.1f}% - there may be opportunities to scale successful campaigns."
        else:
            budget_insight = f"Budget utilization is healthy at {metrics['budget_utilization']:.1f}% - you're staying close to planned spend."
        
        if metrics['overall_ctr'] > 3:
            ctr_insight = f"Your overall CTR of {metrics['overall_ctr']:.2f}% is performing well above industry averages."
        elif metrics['overall_ctr'] > 1.5:
            ctr_insight = f"Your overall CTR of {metrics['overall_ctr']:.2f}% is solid, with room for optimization."
        else:
            ctr_insight = f"Your overall CTR of {metrics['overall_ctr']:.2f}% suggests creative and targeting improvements could drive better engagement."
        
        roas_insight = f"With an estimated ROAS of {metrics['roas']:.2f}x, your campaigns are {'highly profitable' if metrics['roas'] > 4 else 'profitable' if metrics['roas'] > 2 else 'breaking even' if metrics['roas'] > 1 else 'losing money'}."
        
        summary = f"""
        CAMPAIGN PERFORMANCE EXECUTIVE SUMMARY
        
        📊 Key Metrics:
        • Total Spend: ${metrics['total_spend']:,.2f}
        • Total Budget: ${metrics['total_budget']:,.2f}  
        • Overall CTR: {metrics['overall_ctr']:.2f}%
        • Average CPC: ${metrics['overall_cpc']:.2f}
        • Average CPA: ${metrics['overall_cpa']:.2f}
        • Estimated ROAS: {metrics['roas']:.2f}x
        
        💡 Key Insights:
        {budget_insight}
        
        {ctr_insight}
        
        {roas_insight}
        
        📈 Recommendations:
        • Review campaigns exceeding budget for optimization opportunities
        • Test creative variations for campaigns with CTR below 2%
        • Scale budget allocation toward highest-performing channels
        • Implement daily spend monitoring for better budget control
        """
        
        return summary

def main():
    st.title("📈 Campaign Trends Analysis & Budget Reconciliation")
    st.markdown("**Professional Marketing Analytics Dashboard**")
    
    # Initialize analyzer
    if 'analyzer' not in st.session_state:
        st.session_state.analyzer = CampaignAnalyzer()
    
    # Sidebar controls
    st.sidebar.title("🎯 Campaign Analytics")
    
    # Data loading options
    st.sidebar.header("1. Load Campaign Data")
    data_option = st.sidebar.radio("Choose data source:", ["Upload CSV", "Use Sample Data"])
    
    if data_option == "Upload CSV":
        uploaded_file = st.sidebar.file_uploader("Upload campaign data CSV", type="csv")
        if uploaded_file is not None:
            try:
                data = pd.read_csv(uploaded_file)
                st.session_state.analyzer.load_data(data)
                st.sidebar.success(f"Loaded {len(data)} records")
            except Exception as e:
                st.sidebar.error(f"Error loading file: {e}")
    else:
        if st.sidebar.button("Generate Sample Campaign Data"):
            sample_data = generate_sample_campaign_data()
            st.session_state.analyzer.load_data(sample_data)
            st.sidebar.success("Sample data generated!")
    
    # Analysis options
    st.sidebar.header("2. Analysis Options")
    include_budget_reconciliation = st.sidebar.checkbox("Budget Reconciliation", value=True)
    include_performance_trends = st.sidebar.checkbox("Performance Trends", value=True)
    include_channel_analysis = st.sidebar.checkbox("Channel Analysis", value=True)
    
    # Main content
    if st.session_state.analyzer.data is not None:
        data = st.session_state.analyzer.data
        
        # Data overview
        st.header("📋 Campaign Data Overview")
        col1, col2, col3, col4 = st.columns(4)
        
        metrics = st.session_state.analyzer.calculate_key_metrics()
        
        with col1:
            st.metric("Total Spend", f"${metrics['total_spend']:,.2f}", 
                     delta=f"{metrics['budget_utilization']:.1f}% of budget")
        with col2:
            st.metric("Overall CTR", f"{metrics['overall_ctr']:.2f}%")
        with col3:
            st.metric("Total Conversions", f"{metrics['total_conversions']:,.0f}")
        with col4:
            st.metric("Avg CPA", f"${metrics['overall_cpa']:.2f}")
        
        # Data preview
        with st.expander("📊 View Campaign Data", expanded=False):
            st.dataframe(data.head(20), use_container_width=True)
        
        # Generate analysis
        if st.button("🚀 Generate Campaign Analysis", type="primary"):
            with st.spinner("Analyzing campaign performance and budget utilization..."):
                try:
                    charts = st.session_state.analyzer.create_performance_overview()
                    
                    # Ensure charts is a list
                    if not isinstance(charts, list):
                        st.error("Error: Chart generation returned invalid format")
                        charts = []
                    
                    st.session_state.charts = charts
                    
                    # Generate executive summary
                    summary = st.session_state.analyzer.generate_executive_summary()
                    st.session_state.executive_summary = summary
                    
                    if len(charts) > 0:
                        st.success(f"✅ Analysis complete! Generated {len(charts)} comprehensive charts.")
                    else:
                        st.warning("⚠️ No charts were generated. Please check your data format.")
                        
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.session_state.charts = []
        
        # Display charts
        if 'charts' in st.session_state and st.session_state.charts:
            st.header("📊 Campaign Performance Analysis")
            
            # Display executive summary
            if 'executive_summary' in st.session_state:
                with st.expander("📋 Executive Summary", expanded=True):
                    st.text(st.session_state.executive_summary)
            
            # Budget Reconciliation Table
            st.subheader("💰 Budget Reconciliation Summary")
            
            budget_summary = st.session_state.analyzer.data.groupby('Campaign').agg({
                'Budget': 'sum',
                'Spend': 'sum'
            }).reset_index()
            budget_summary['Variance'] = budget_summary['Spend'] - budget_summary['Budget']
            budget_summary['Variance %'] = ((budget_summary['Variance'] / budget_summary['Budget']) * 100).round(1)
            budget_summary['Status'] = budget_summary['Variance'].apply(
                lambda x: '🔴 Over Budget' if x > 0 else '🟢 Under Budget' if x < 0 else '⚪ On Target'
            )
            
            # Format currency columns
            budget_summary['Budget'] = budget_summary['Budget'].apply(lambda x: f'${x:,.2f}')
            budget_summary['Spend'] = budget_summary['Spend'].apply(lambda x: f'${x:,.2f}')
            budget_summary['Variance'] = budget_summary['Variance'].apply(lambda x: f'${x:,.2f}')
            
            # Display table
            st.dataframe(
                budget_summary[['Campaign', 'Budget', 'Spend', 'Variance', 'Variance %', 'Status']],
                use_container_width=True,
                hide_index=True
            )
            
            # Budget alerts
            overspend_data = st.session_state.analyzer.data.groupby('Campaign').agg({
                'Budget': 'sum',
                'Spend': 'sum'
            }).reset_index()
            overspend_data['Variance'] = overspend_data['Spend'] - overspend_data['Budget']
            critical_overspend = overspend_data[overspend_data['Variance'] > overspend_data['Budget'] * 0.1]
            
            if len(critical_overspend) > 0:
                st.warning(f"⚠️ **Budget Alert:** {len(critical_overspend)} campaigns have overspent by more than 10%")
                for _, row in critical_overspend.iterrows():
                    st.error(f"❌ **{row['Campaign']}** is ${row['Variance']:,.2f} over budget ({row['Variance']/row['Budget']*100:.1f}% overspend)")
            
            st.markdown("---")
            
            # Create tabs for different analyses
            tab_names = [chart['title'] for chart in st.session_state.charts]
            tabs = st.tabs(tab_names)
            
            for tab, chart in zip(tabs, st.session_state.charts):
                with tab:
                    st.plotly_chart(chart['figure'], use_container_width=True)
                    st.info(f"💡 **Insight:** {chart['insight']}")
        
        # Export options
        if 'charts' in st.session_state:
            st.header("📄 Export Reports")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Export to PowerPoint", type="primary"):
                    st.info("PowerPoint export functionality can be implemented using the same methods as the KPI dashboard.")
            
            with col2:
                if st.button("📑 Export to PDF", type="primary"):
                    st.info("PDF export functionality can be implemented using the same methods as the KPI dashboard.")
    
    else:
        # Welcome message
        st.info("👆 Load campaign data from the sidebar to get started!")
        
        st.markdown("""
        ### 🎯 Campaign Analytics Features:
        
        #### **📊 Performance Tracking**
        - CTR, CPC, CPA, and conversion rate analysis
        - Daily performance trends and patterns
        - Campaign and channel performance comparison
        - Real-time budget utilization monitoring
        
        #### **💰 Budget Reconciliation** 
        - Budget vs actual spend analysis
        - Overspend identification and alerts
        - Budget utilization timeline tracking
        - Variance analysis and recommendations
        
        #### **📈 Trend Analysis**
        - Multi-dimensional performance visualization
        - Seasonal pattern identification
        - Channel effectiveness comparison
        - ROI and ROAS calculation
        
        #### **🎨 Professional Reporting**
        - Executive-ready dashboards
        - Automated insight generation
        - PowerPoint and PDF export
        - Marketing-focused color schemes and styling
        
        ### 📋 Expected Data Format:
        
        Your CSV should include these columns:
        - **Date**: Campaign date (YYYY-MM-DD format)
        - **Campaign**: Campaign name
        - **Channel**: Marketing channel (Search, Social, Video, etc.)
        - **Impressions**: Number of impressions
        - **Clicks**: Number of clicks
        - **Conversions**: Number of conversions
        - **Budget**: Allocated daily budget
        - **Spend**: Actual spend amount
        
        Additional calculated metrics (CTR, CPC, CPA, etc.) will be computed automatically.
        
        **Start by uploading your campaign data or using the sample data generator!**
        """)

if __name__ == "__main__":
    main()