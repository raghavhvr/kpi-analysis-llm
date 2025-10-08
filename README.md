# 📊 KPI Insights Dashboard

A powerful Streamlit application that automatically generates business insights, creates visualizations, builds PowerPoint presentations, and provides an AI chatbot for data exploration.

## 🎯 Features

✅ **CSV Upload** - Upload your own datasets  
✅ **Kaggle Integration** - Load datasets directly from Kaggle  
✅ **Smart Charts** - Enhanced visualizations with trend lines, high/low annotations  
✅ **LLM Insights** - GPT-powered analysis and commentary  
✅ **PowerPoint Generation** - Auto-create presentations with embedded charts  
✅ **Data Chatbot** - Ask questions about your data in natural language  
✅ **Professional Reports** - Export comprehensive analysis reports  

## 🚀 Quick Start (5 minutes!)

### 1. Download Files
Save these files in a new folder:
- `app.py` (main application)
- `requirements.txt` (dependencies)
- `setup.py` (setup script)
- `sample_sales_data.csv` (test data)

### 2. Run Setup
```bash
# Navigate to your project folder
cd your-project-folder

# Run the setup script
python setup.py
```

### 3. Launch the App
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 📋 Manual Setup (Alternative)

If the setup script doesn't work:

### 1. Create Virtual Environment
```bash
# Create project folder
mkdir kpi-insights-app
cd kpi-insights-app

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)  
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install streamlit pandas plotly python-pptx kaggle requests python-dotenv openpyxl Pillow kaleido
```

### 3. Create Directory Structure
```bash
mkdir data
mkdir generated_ppts
```

## 🔑 API Keys Setup (Optional but Recommended)

### Ollama (Open Source LLM - Recommended)
1. **Install Ollama**: Download from [ollama.ai](https://ollama.ai)
2. **Start the service**: Run `ollama serve` in terminal
3. **Download a model**: Run `ollama pull llama3.1`
4. **Test in app**: Use the "Test Ollama Connection" button

### Kaggle API (for loading datasets)
1. Go to [kaggle.com](https://kaggle.com) → Account → API
2. Click "Create New API Token"
3. Download `kaggle.json`
4. Place it in: `C:\Users\YourUsername\.kaggle\kaggle.json` (Windows)

## 📊 How to Use

### Step 1: Load Data
**Option A: Upload CSV**
- Click "Upload CSV" in sidebar
- Select your CSV file
- Click "Load CSV"

**Option B: Use Kaggle Dataset**
- Enter dataset name (format: `username/dataset-name`)
- Example: `russellyates88/stock-market-data`
- Click "Load Kaggle Dataset"

**Option C: Use Sample Data**
- Upload the provided `sample_sales_data.csv`

### Step 2: Generate Analysis
- Click "🎨 Generate Smart Charts & Analysis"
- The app will:
  - Analyze your data structure
  - Generate relevant business charts
  - Create AI-powered insights

### Step 3: Set up Ollama (Optional but Recommended)
- Download from [ollama.ai](https://ollama.ai)
- Run `ollama serve` in terminal
- Download a model: `ollama pull llama3.1`
- The app will auto-detect and use Ollama for AI insights

### Step 4: Generate Analysis
- Use the chat interface to ask questions:
  - "What are the key trends?"
  - "Which region performs best?"
  - "Show me correlations between sales and satisfaction"

### Step 4: Generate Reports
- Click "🎯 Generate PowerPoint Report"
- Download your comprehensive presentation

## 📈 Example Datasets to Try

- `russellyates88/stock-market-data` - Stock market analysis
- `prasadperera/the-boston-housing-dataset` - Real estate data
- `vikramtiwari/pima-indians-diabetes-database` - Healthcare analytics

## 💡 Smart Features

### Enhanced Chart Generation
The app automatically detects and creates professional visualizations:
- **Time series data** → Line charts with trend lines and R² values
- **KPI metrics** → Histograms with mean/median annotations  
- **Category performance** → Bar charts with value labels and performance highlights
- **Correlations** → Interactive heatmaps with correlation coefficients
- **Geographic data** → Color-coded regional performance analysis

**Professional Features:**
- ⭐ **Trend lines** with statistical significance (R² values)
- 📍 **High/Low annotations** with exact values highlighted
- 🎨 **Color-coded performance** (best performers in green, needs attention in red)
- 📊 **Value labels** on all charts for precise reading
- 🔍 **Interactive hover details** with business context

### AI-Powered Business Insights
- **Human-readable analysis**: Not just technical stats, but actual business insights
- **Actionable recommendations**: Specific suggestions for business improvement
- **Pattern recognition**: Identifies trends, anomalies, and opportunities
- **Executive-ready summaries**: Insights written for business stakeholders
- **Context-aware**: Understands your specific data domain and provides relevant commentary

Example insight: *"Revenue shows strong growth in Q2, with the North region outperforming by 23%. However, customer satisfaction dipped slightly in June, suggesting we should investigate service quality during our busiest period."*

### Professional PowerPoint
- Executive summary slide
- Individual chart slides with insights
- Embedded chart images
- Business-focused commentary

## 🛠️ Troubleshooting

### Common Issues

**"Microsoft Visual C++ required" error:**
- Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
- Or use: `conda install pandas matplotlib` instead of pip

**Kaggle API not working:**
- Check `kaggle.json` is in correct location
- Windows: `C:\Users\YourUsername\.kaggle\`
- Mac/Linux: `~/.kaggle/`

**Charts not embedding in PowerPoint:**
- This is expected if kaleido package isn't installed
- The app will create descriptive text instead of chart images
- To enable chart embedding: `pip install kaleido`
- Note: kaleido can be tricky to install on some systems, but the app works fine without it

**"Chatbot doesn't work" or gives basic responses:**
- Fixed in v2.4! Chatbot now works immediately with any dataset
- Basic responses available even without Ollama setup
- For enhanced AI responses: Install Ollama and run `ollama serve`
- Try questions like "What columns are available?" or "Show me key statistics"

**"Only getting 3 charts, want more analysis:**
- Fixed in v2.4! App now generates up to 8 comprehensive chart types
- Includes time series, distributions, correlations, geographic analysis
- More comprehensive category analysis with multiple segments
- Enhanced performance indicators and annotations

**"Want more detailed insights:**
- Enable "Use Full Dataset" for complete analysis
- Set up Ollama for AI-powered insights (optional but recommended)
- Use the working chatbot to ask specific questions about your data
- Generate PowerPoint reports for comprehensive documentation

**AI insights taking forever or getting stuck:**
- Fixed in v2.3! Maximum 15-second timeout for all AI operations
- Click "Skip AI Insights" button for instant chart generation
- App never hangs - always has fallback insights ready
- Charts generate immediately, insights are optional bonus

**"Sample won't work for us" - need full dataset:**
- Fixed in v2.3! Enable "Use Full Dataset" checkbox in sidebar
- Supports datasets up to 100K+ rows with full analysis
- Adjustable sample size (500-5000 rows) when sampling is preferred
- User controls speed vs accuracy trade-off

**Charts still taking too long:**
- New in v2.3: Should never take more than 10 seconds
- Try "Skip AI Insights" for 3-second chart generation
- Check "Use Full Dataset" setting in sidebar
- Restart app if issues persist

**Missing high/low highlights:**
- Fixed in v2.3! All time series charts now show peak (📈) and trough (📉) points
- Bar charts show best performer (🏆) and needs attention (⚠️) markers
- Value annotations display exact numbers on all charts

**"Charts are too simple now":**
- This is intentional for speed! You get the key insights in 3 seconds
- High/low points, trends, and performance indicators are still included
- For more complex analysis, the AI insights provide detailed commentary

**Datetime parsing warnings (dateutil fallback):**
- This is now fixed in v2.2 - app uses smarter date detection  
- If you still see warnings, your dataset has unusual date formats
- App will still work, just may not detect time series patterns

**Charts taking too long to generate:**
- New in v2.2: Smart sampling limits data to 1000 rows for chart generation
- Progress indicators show what's happening
- Most charts now generate in 2-5 seconds
- If still slow, try smaller datasets or restart the app

**"No suitable chart opportunities found":**
- Check that you have both numeric AND categorical columns
- Ensure column names are clear (sales, amount, date, region, etc.)  
- Try the sample datasets first to verify app is working

**Plotly configuration warnings:**
- If you see warnings about keyword arguments, update packages: `pip install --upgrade plotly streamlit`
- The app uses the latest Plotly configuration standards

**Missing trend lines in charts:**
- Install scipy for statistical trend analysis: `pip install scipy`
- App works fine without it, just uses moving averages instead of regression lines

**Streamlit deprecation warnings:**
- If you see warnings about `use_container_width`, update Streamlit: `pip install --upgrade streamlit`
- The app uses the latest Streamlit parameters and should work without warnings on v1.30+

**Ollama not connecting:**
- Make sure Ollama is installed and running: `ollama serve`
- Download a model: `ollama pull llama3.1`
- Check the URL in app sidebar (default: http://localhost:11434)
- Use "Test Ollama Connection" button to verify setup
- App still works without Ollama, just with simpler insights

**Memory errors with large datasets:**
- Use smaller datasets (< 1GB)
- Or sample your data: `data.sample(10000)`

### Performance Tips

- **Comprehensive analysis**: v2.4 creates up to 8 different chart types in 10-15 seconds
- **Smart sampling**: Choose full dataset (accurate) or sampling (faster) based on your needs
- **Working chatbot**: Ask questions even without Ollama - basic responses always available
- **Multiple chart types**: Time series, distributions, correlations, geographic, category analysis
- **Never hangs**: All operations have timeout protection and smart fallbacks

**Choose Your Analysis Level:**
- **Quick Overview (5-10 secs)**: Skip AI insights, use sampling, get 6-8 visual charts
- **Standard Analysis (10-15 secs)**: Full dataset with visual charts and basic insights
- **Complete Analysis (15-25 secs)**: Full dataset + AI insights + interactive chat
- **Any dataset size**: 100 rows to 100K+ rows supported with automatic optimization

**Chart Types You'll Get:**
1. **Time Series Analysis**: Trends over time with peak/trough markers
2. **KPI Distributions**: Histogram analysis with mean/median indicators  
3. **Category Performance**: Segment analysis with best/worst highlighting
4. **Correlation Heatmaps**: Relationship analysis between metrics
5. **Geographic Analysis**: Regional/location-based performance maps
6. **Multi-dimensional Views**: Combined metric analysis
7. **Performance Rankings**: Top/bottom performer identification
8. **Trend Correlations**: Advanced pattern recognition

**Chat Features:**
- Works immediately with any dataset (no setup required)
- Basic responses available even without Ollama
- Enhanced AI responses with Ollama integration
- Instant answers to data questions
- Smart fallbacks prevent hanging or errors

**Optimal Usage:**
- **Marketing/Sales Data**: Generates campaign, regional, and performance analysis
- **Time Series Data**: Automatic trend detection with statistical significance
- **Category-Rich Data**: Comprehensive segment analysis with performance ranking
- **Multi-metric Datasets**: Correlation analysis and relationship mapping

## 📁 Project Structure

```
kpi-insights-app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies  
├── setup.py                 # Automated setup script
├── sample_sales_data.csv    # Test dataset
├── .env                     # API keys (create this)
├── data/                    # Downloaded Kaggle datasets
└── generated_ppts/          # Generated PowerPoint files
```

## 🔧 Customization

### Adding New Chart Types
Edit the `SmartChartGenerator` class in `app.py`:
```python
def identify_chart_opportunities(df):
    # Add your custom chart logic here
```

### Custom Insights
Modify the `LLMInsights` class to add domain-specific analysis:
```python
def generate_fallback_insights(df, chart_info):
    # Add your business logic here
```

### PowerPoint Templates
Update the `create_powerpoint_with_charts` method to use your company templates.

## 🚀 Advanced Features

### Multiple File Support
- Upload multiple CSVs
- Combine datasets for analysis
- Cross-dataset comparisons

### Export Options
- PowerPoint presentations
- PDF reports (coming soon)
- Excel workbooks (coming soon)

### AI Integration
- Ollama (open source LLMs)
- Local processing - your data stays private
- Multiple model support (llama3.1, mistral, codellama)
- Custom LLM endpoints (coming soon)

## 🤝 Support

### Getting Help
1. Check the troubleshooting section above
2. Try the sample dataset first
3. Verify all packages installed correctly
4. Check that your Python version is 3.8+

### Common Questions

**Q: Do I need API keys to use the app?**
A: No! The app works without API keys, but AI features are limited.

**Q: What file formats are supported?**
A: Currently CSV files. Excel support coming soon.

**Q: Can I use this with my company data?**
A: Yes! Upload your CSV files directly. Data stays local.

**Q: How large can my datasets be?**
A: Recommended: < 100MB for best performance. Larger files may work but will be slower.

## 📝 Changelog

### v2.4 (Current) - 🚀 COMPREHENSIVE ANALYSIS VERSION
- ✅ **8 Chart Types**: Time series, distributions, categories, correlations, geographic analysis
- ✅ **Working Chatbot**: Fully functional data chat with Ollama integration + smart fallbacks
- ✅ **Enhanced Visualizations**: More comprehensive charts with performance indicators
- ✅ **Smart Annotations**: Best/worst performers, peak/trough markers, exact values
- ✅ **Flexible Analysis**: Full dataset or custom sampling options
- ✅ **Timeout Protection**: Never get stuck - all operations have built-in failsafes
- ✅ **Interactive Experience**: Chat works even without Ollama (basic responses)

### v2.3 - ⚡ NEVER GET STUCK VERSION
- ✅ **AI Timeout Protection**: Never wait more than 15 seconds for insights
- ✅ **Full Dataset Support**: Analyze complete datasets (not just samples) up to 100K+ rows
- ✅ **Skip AI Option**: Generate charts instantly without waiting for AI analysis
- ✅ **Smart Sampling Control**: User-configurable sample size (500-5000 rows)
- ✅ **Zero Hang Prevention**: All operations have timeouts and fallbacks
- ✅ **High/Low Highlights**: Peak/trough markers with exact values displayed
- ✅ **Ultra-Fast Generation**: Charts in 5-10 seconds regardless of dataset size

### v2.2 
- ✅ **Performance Optimization**: 10x faster chart generation with smart sampling
- ✅ **Fixed All Warnings**: No more datetime parsing or Plotly configuration warnings
- ✅ **Progress Indicators**: Real-time feedback during chart generation
- ✅ **Better Error Handling**: Graceful fallbacks for complex datasets  
- ✅ **Smart Sampling**: Large datasets auto-sampled to 1000 rows for speed
- ✅ **Enhanced Charts**: Professional styling with trend lines and value annotations
- ✅ **Dataset Validation**: Clear feedback about data suitability

### v2.1
- ✅ **Ollama Integration**: Open source LLM support instead of OpenAI
- ✅ **Human-readable Insights**: Business-focused analysis instead of technical stats
- ✅ **Better Chart Embedding**: Graceful handling of kaleido issues
- ✅ **Enhanced Chat**: More conversational and helpful responses
- ✅ **Local AI Processing**: Your data stays private with Ollama
- ✅ **Streamlit Updates**: Fixed deprecation warnings, updated to latest parameters

### v2.0
- ✅ CSV upload functionality
- ✅ Smart chart generation
- ✅ PowerPoint with embedded charts  
- ✅ Data chatbot interface
- ✅ Improved state management
- ✅ Better error handling

### v1.0
- Basic Kaggle integration
- Simple charts
- Text-only PowerPoint
- Basic insights

## 🔮 Roadmap

- [ ] Excel file support
- [ ] PDF report generation
- [ ] Dashboard templates
- [ ] Data connection to databases
- [ ] Advanced statistical analysis
- [ ] Custom branding options

---

**Ready to analyze your data? Run `streamlit run app.py` and start exploring!** 🚀