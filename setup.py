#!/usr/bin/env python3
"""
Setup script for KPI Insights Dashboard
Run this to set up everything you need!
"""

import os
import subprocess
import sys
import urllib.request

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} failed: {str(e)}")
        return False

def create_directory_structure():
    """Create necessary directories"""
    directories = ['data', 'generated_ppts']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")

def create_env_file():
    """Create .env file template"""
    env_content = """# Kaggle API Credentials
KAGGLE_USERNAME=your_kaggle_username
KAGGLE_KEY=your_kaggle_key

# Ollama Configuration (Local Open Source LLM)
OLLAMA_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1

# Note: Ollama runs locally, no API key needed!
# Setup: 
# 1. Install from https://ollama.ai
# 2. Run: ollama serve
# 3. Download model: ollama pull llama3.1
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("📝 Created .env template file")
    else:
        print("📝 .env file already exists")

def download_sample_data():
    """Create sample data file"""
    sample_data = """Date,Region,Product,Sales_Amount,Units_Sold,Customer_Satisfaction,Marketing_Spend
2024-01-15,North,Laptop,45000,50,4.2,8000
2024-01-20,South,Desktop,32000,40,3.8,6000
2024-01-25,East,Laptop,52000,58,4.5,9000
2024-02-10,West,Tablet,28000,70,4.1,5500
2024-02-15,North,Desktop,38000,45,3.9,7000
2024-02-20,South,Laptop,48000,55,4.3,8500
2024-03-05,East,Tablet,31000,78,4.0,6000
2024-03-10,West,Desktop,41000,48,4.1,7500
2024-03-15,North,Laptop,55000,62,4.6,10000
2024-03-20,South,Tablet,29000,72,3.9,5800"""
    
    with open('sample_sales_data.csv', 'w') as f:
        f.write(sample_data)
    print("📊 Created sample_sales_data.csv for testing")

def main():
    print("🚀 Setting up KPI Insights Dashboard")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Create directory structure
    print("\n📁 Creating directory structure...")
    create_directory_structure()
    
    # Upgrade pip
    run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip")
    
    # Install requirements
    install_success = run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                                 "Installing Python packages")
    
    if not install_success:
        print("\n⚠️  Some packages failed to install. Trying alternative approach...")
        
        # Try installing packages one by one
        packages = [
            "streamlit>=1.30.0", "pandas", "plotly", "python-pptx", 
            "kaggle", "requests", "python-dotenv", "openpyxl", "Pillow",
            "numpy", "scipy"
        ]
        
        for package in packages:
            run_command(f"{sys.executable} -m pip install {package}", f"Installing {package}")
        
        # Try kaleido separately (optional for chart embedding)
        print("\n🖼️  Installing chart export capability (optional)...")
        kaleido_success = run_command(f"{sys.executable} -m pip install kaleido", "Installing kaleido")
        if not kaleido_success:
            print("⚠️  kaleido failed to install. Chart export to PowerPoint will use text descriptions instead.")
            print("   The app will still work perfectly - just charts won't be embedded as images in PPT.")
            print("   To try again later: pip install kaleido")
    
    # Create env file
    create_env_file()
    
    # Create sample data
    download_sample_data()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    print("\n📝 Next Steps:")
    print("1. Edit .env file with your API keys (optional)")
    print("2. For Kaggle datasets: Set up Kaggle API credentials")
    print("3. Run the app: streamlit run app.py")
    print("4. Test with sample_sales_data.csv or try: julialy900/marketing-campaign-analysis")
    
    print("\n⚡ Performance Notes:")
    print("• App optimized for datasets up to 10K rows (larger ones auto-sampled)")
    print("• Chart generation typically takes 2-5 seconds")  
    print("• Progress bars show real-time generation status")
    print("• Works offline once Ollama models are downloaded")
    
    print("\n🔑 AI Setup (Optional but Recommended):")
    print("• Ollama (Open Source): https://ollama.ai")
    print("  - Download and install Ollama")
    print("  - Run: ollama serve")
    print("  - Download model: ollama pull llama3.1")
    print("• Kaggle: https://www.kaggle.com/settings/account -> API -> Create New API Token")
    
    print("\n🚀 Ready to launch!")
    print("Run: streamlit run app.py")

if __name__ == "__main__":
    main()