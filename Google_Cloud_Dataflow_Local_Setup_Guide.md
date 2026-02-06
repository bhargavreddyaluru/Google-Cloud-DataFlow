# Google Cloud Dataflow Local Development Setup Guide

This comprehensive guide will walk you through setting up a complete local development environment for Google Cloud Dataflow pipeline development.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Prerequisites](#prerequisites)
3. [Google Cloud SDK Installation](#google-cloud-sdk-installation)
4. [Python Environment Setup](#python-environment-setup)
5. [Apache Beam Installation](#apache-beam-installation)
6. [IDE Configuration](#ide-configuration)
7. [Authentication Setup](#authentication-setup)
8. [Development Tools](#development-tools)
9. [Testing Your Setup](#testing-your-setup)
10. [Common Issues and Solutions](#common-issues-and-solutions)
11. [Next Steps](#next-steps)

---

## System Requirements

### Hardware Requirements
- **RAM**: Minimum 8GB, Recommended 16GB or more
- **Storage**: At least 10GB free space for tools and dependencies
- **Processor**: 64-bit processor (x86_64)

### Operating System Support
- Windows 10/11 (64-bit)
- macOS 10.15+ (Catalina or later)
- Linux (Ubuntu 18.04+, CentOS 7+, Debian 9+)

---

## Prerequisites

### 1. Administrative Privileges
You'll need administrator/sudo privileges to install:
- Google Cloud SDK
- Python packages globally (if needed)
- Development tools

### 2. Internet Connection
Stable internet connection for:
- Downloading installation packages
- Cloud authentication
- Accessing Google Cloud services

### 3. Google Cloud Account
- Active Google Cloud account with billing enabled
- Project created in Google Cloud Console

---

## Google Cloud SDK Installation

### Windows Installation

#### Option 1: Interactive Installer (Recommended)
1. Download the Google Cloud SDK installer:
   ```
   https://dl.google.com/dl/cloudsdk/channels/rapid/GoogleCloudSDKInstaller.exe
   ```

2. Run the installer with administrator privileges
3. Follow the installation wizard:
   - Choose installation directory (default: `C:\Program Files\Google\Cloud SDK`)
   - Select components to install (keep defaults)
   - Enable "Add gcloud to PATH" option
   - Choose to use Google Cloud SDK shell

#### Option 2: Package Manager (Chocolatey)
```powershell
# Install Chocolatey if not already installed
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Google Cloud SDK
choco install gcloudsdk
```

### macOS Installation

#### Option 1: Homebrew (Recommended)
```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Google Cloud SDK
brew install google-cloud-sdk
```

#### Option 2: Interactive Installer
```bash
# Download and run the installer
curl https://sdk.cloud.google.com | bash
exec -l $SHELL
```

### Linux Installation

#### Debian/Ubuntu
```bash
# Add the Cloud SDK distribution URI as a package source
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list

# Import the Google Cloud public key
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

# Update and install
sudo apt-get update
sudo apt-get install google-cloud-sdk
```

#### CentOS/RHEL/Fedora
```bash
# Create repo file
sudo tee /etc/yum.repos.d/google-cloud-sdk.repo << EOM
[google-cloud-sdk]
name=Google Cloud SDK
baseurl=https://packages.cloud.google.com/yum/repos/cloud-sdk-el7-x86_64
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg
       https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg
EOM

# Install
sudo yum install google-cloud-sdk
```

### Verify Google Cloud SDK Installation
```bash
gcloud version
```

You should see output similar to:
```
Google Cloud SDK 447.0.0
bq 2.0.98
core 447.0.0
gcloud-crc32c 1.0.0
gsutil 5.26
```

---

## Python Environment Setup

### Install Python
Dataflow pipelines are typically written in Python. We recommend Python 3.8-3.11.

#### Windows
1. Download Python from https://www.python.org/downloads/
2. Run installer with administrator privileges
3. Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   pip --version
   ```

#### macOS
```bash
# Install using Homebrew
brew install python@3.11

# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-venv

# Verify installation
python3.11 --version
pip3.11 --version
```

### Create Virtual Environment
```bash
# Navigate to your project directory
cd "e:\DataFlow Learning"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Upgrade pip and Essential Tools
```bash
# Activate virtual environment first
.venv\Scripts\activate

# Upgrade pip and essential packages
pip install --upgrade pip setuptools wheel
```

## Current Installation Progress

### ✅ Completed Steps
1. **Virtual Environment Created**: `.venv` has been created successfully
2. **Requirements File Created**: `requirements.txt` has been created with all necessary packages

### 🔄 Next Steps
Run these commands in your terminal (from `e:\DataFlow Learning` directory):

```bash
# Activate virtual environment
.venv\Scripts\activate

# Install all packages from requirements.txt (numpy compatibility fixed)
pip install -r requirements.txt

# Verify Apache Beam installation
python -c "import apache_beam as beam; print(f'Apache Beam version: {beam.__version__}')"
```

### 📋 Current Status
- Virtual environment: ✅ Created (`.venv`)
- Requirements file: ✅ Created (numpy compatibility fixed)
- Package installation: ⏳ Ready to install
- Apache Beam verification: ⏳ Pending

### 🔧 Recent Fix
**Issue**: Apache Beam 2.53.0 requires `numpy<1.25.0` but we had `numpy==1.26.2`
**Solution**: Updated to `numpy==1.24.4` for compatibility

---

## Apache Beam Installation

### Install Apache Beam SDK
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate

# Install Apache Beam with Google Cloud Dataflow runner
pip install apache-beam[gcp]

# For additional features (optional)
pip install apache-beam[gcp,test]
```

### Verify Apache Beam Installation
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate

python -c "import apache_beam as beam; print(f'Apache Beam version: {beam.__version__}')"
```

### Additional Useful Packages
```bash
# Make sure virtual environment is activated
.venv\Scripts\activate

# For data manipulation
pip install pandas numpy

# For logging and debugging
pip install python-dotenv

# For testing
pip install pytest pytest-mock

# For development
pip install black flake8 mypy
```

---

## IDE Configuration

### Visual Studio Code (Recommended)

#### Installation
1. Download and install VS Code from https://code.visualstudio.com/

#### Essential Extensions
Install these extensions from the VS Code marketplace:
- **Python** (Microsoft)
- **Google Cloud Code** (Google)
- **Docker** (Microsoft)
- **GitLens** (GitKraken)
- **Python Docstring Generator** (Nils Werner)
- **Better Comments** (Aaron Bond)

#### VS Code Configuration
Create `.vscode/settings.json` in your project:
```json
{
    "python.defaultInterpreterPath": "./.venv/Scripts/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    },
    "googleCloudCode.projectId": "your-project-id"
}
```

### PyCharm Professional
1. Install PyCharm Professional
2. Configure Python interpreter to use your virtual environment
3. Install Google Cloud plugin
4. Configure deployment configurations

---

## Authentication Setup

### Initialize Google Cloud SDK
```bash
gcloud init
```

Follow the prompts:
1. Login to your Google Account
2. Select or create a project
3. Choose default region and zone

### Set Default Project
```bash
# Replace YOUR_PROJECT_ID with your actual project ID
gcloud config set project YOUR_PROJECT_ID
```

### Application Default Credentials
```bash
gcloud auth application-default login
```

This will open a browser window for authentication.

### Verify Authentication
```bash
# Check current account
gcloud auth list

# Test access to Google Cloud Storage
gsutil ls
```

### Service Account (Optional but Recommended for Production)
```bash
# Create service account
gcloud iam service-accounts create dataflow-developer \
    --display-name="Dataflow Developer" \
    --description="Service account for Dataflow development"

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:dataflow-developer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/dataflow.developer"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:dataflow-developer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/storage.admin"

# Download service account key
gcloud iam service-accounts keys create ~/dataflow-key.json \
    --iam-account=dataflow-developer@YOUR_PROJECT_ID.iam.gserviceaccount.com

# Set environment variable for service account
set GOOGLE_APPLICATION_CREDENTIALS=~/dataflow-key.json  # Windows
export GOOGLE_APPLICATION_CREDENTIALS=~/dataflow-key.json  # macOS/Linux
```

---

## Development Tools

### Docker Installation
Dataflow pipelines can be tested locally using Docker.

#### Windows
1. Install Docker Desktop from https://www.docker.com/products/docker-desktop
2. Enable WSL 2 integration
3. Restart Docker Desktop

#### macOS
```bash
brew install --cask docker
```

#### Linux (Ubuntu)
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
newgrp docker
```

### Git Configuration
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

### Additional Tools
```bash
# For monitoring and debugging
pip install google-cloud-logging
pip install google-cloud-monitoring

# For data validation
pip install great-expectations

# For pipeline visualization
pip install apache-beam[interactive]
```

---

## Testing Your Setup

### Create a Test Pipeline
Create a file `test_pipeline.py`:

```python
import apache_beam as beam
import logging

def run():
    logging.basicConfig(level=logging.INFO)
    
    with beam.Pipeline() as pipeline:
        (
            pipeline
            | 'Create numbers' >> beam.Create([1, 2, 3, 4, 5])
            | 'Multiply by 2' >> beam.Map(lambda x: x * 2)
            | 'Print results' >> beam.Map(print)
        )

if __name__ == '__main__':
    run()
```

### Run Test Pipeline
```bash
python test_pipeline.py
```

Expected output:
```
2
4
6
8
10
```

### Test with DirectRunner
```bash
python -m apache_beam.examples.wordcount --output ./wordcount_output --runner DirectRunner
```

### Test Dataflow Runner (Requires Cloud Project)
```bash
python -m apache_beam.examples.wordcount \
    --output gs://YOUR_BUCKET/wordcount_output \
    --runner DataflowRunner \
    --project YOUR_PROJECT_ID \
    --region us-central1 \
    --temp_location gs://YOUR_BUCKET/temp/
```

---

## Common Issues and Solutions

### Python Path Issues
**Problem**: `python` command not found
**Solution**: 
- Windows: Add Python to PATH during installation
- macOS/Linux: Create aliases or use `python3`

### Virtual Environment Issues
**Problem**: Activation fails
**Solution**:
- Windows: Run PowerShell as administrator
- macOS/Linux: Check script permissions: `chmod +x dataflow-env/bin/activate`

### Authentication Issues
**Problem**: `Permission denied` errors
**Solution**:
- Run `gcloud auth application-default login`
- Check service account permissions
- Verify project ID is correct

### Memory Issues
**Problem**: Out of memory errors
**Solution**:
- Increase JVM memory: `--direct_runner_use_stacked_bundle=true`
- Use smaller datasets for testing
- Increase system RAM

### Dependency Conflicts
**Problem**: Package version conflicts
**Solution**:
- Use fresh virtual environment
- Pin specific versions in requirements.txt
- Use `pip check` to identify conflicts

### Network Issues
**Problem**: Connection timeouts
**Solution**:
- Check internet connection
- Configure proxy settings if needed
- Use `gcloud config set proxy/...` for corporate networks

---

## Environment Variables Configuration

Create a `.env` file in your project root:
```env
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Dataflow Configuration
DATAFLOW_TEMP_LOCATION=gs://your-bucket/temp/
DATAFLOW_STAGING_LOCATION=gs://your-bucket/staging/

# Python Configuration
PYTHONPATH=./src
```

Load environment variables in Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Project Structure Best Practices

```
your-dataflow-project/
├── src/
│   ├── __init__.py
│   ├── pipelines/
│   │   ├── __init__.py
│   │   ├── example_pipeline.py
│   │   └── utils.py
│   └── tests/
│       ├── __init__.py
│       ├── test_example_pipeline.py
│       └── test_utils.py
├── .venv/
├── requirements.txt
├── setup.py
├── .env
├── .gitignore
├── README.md
└── .vscode/
    └── settings.json
```

### requirements.txt Template
```txt
apache-beam[gcp]==2.53.0
pandas==2.1.4
numpy==1.24.4
python-dotenv==1.0.0
pytest==7.4.3
pytest-mock==3.12.0
black==23.12.1
flake8==7.0.0
mypy==1.8.0
google-cloud-logging==3.8.0
google-cloud-monitoring==2.19.0
```

**Note**: Apache Beam 2.53.0 requires numpy<1.25.0, so we use numpy==1.24.4 for compatibility.

### .gitignore Template
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Environment Variables
.env
service-account-key.json

# Data
*.csv
*.json
*.parquet
!data/sample.*

# Logs
*.log
logs/

# Beam
beam_output/
wordcount_output/
```

---

## Next Steps

### 1. Learn Apache Beam Basics
- Read the [Apache Beam Programming Guide](https://beam.apache.org/documentation/programming-guide/)
- Understand transforms, PCollections, and pipeline concepts

### 2. Explore Dataflow Examples
- Clone Apache Beam examples: `git clone https://github.com/apache/beam.git`
- Study the examples in `sdks/python/apache_beam/examples/`

### 3. Set Up Monitoring
- Configure Cloud Logging
- Set up Cloud Monitoring dashboards
- Learn to use Dataflow monitoring interface

### 4. Best Practices
- Implement proper error handling
- Use appropriate windowing strategies
- Optimize for performance and cost
- Implement testing strategies

### 5. Advanced Topics
- Custom transforms
- Side inputs and outputs
- State and timers
- Streaming pipelines
- ML model integration

---

## Troubleshooting Resources

### Official Documentation
- [Google Cloud Dataflow Documentation](https://cloud.google.com/dataflow/docs)
- [Apache Beam Documentation](https://beam.apache.org/documentation/)
- [Google Cloud SDK Documentation](https://cloud.google.com/sdk/docs)

### Community Support
- [Stack Overflow - Google Cloud Dataflow](https://stackoverflow.com/questions/tagged/google-cloud-dataflow)
- [Apache Beam Slack](https://s.apache.org/beam-slack)
- [Google Cloud Community](https://cloud.google.com/community)

### Debugging Tools
- Cloud Console: Dataflow Jobs page
- Cloud Logging: Filter by Dataflow job ID
- Cloud Monitoring: Dataflow metrics
- Local debugging with DirectRunner

---

## Quick Reference Commands

### Google Cloud SDK
```bash
# List projects
gcloud projects list

# Set project
gcloud config set project PROJECT_ID

# List services
gcloud services list

# Enable Dataflow API
gcloud services enable dataflow.googleapis.com

# Create storage bucket
gsutil mb gs://your-unique-bucket-name
```

### Python Virtual Environment
```bash
# Create environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate

# Activate (macOS/Linux)
source .venv/bin/activate

# Deactivate
deactivate

# Save dependencies
pip freeze > requirements.txt

# Install from requirements
pip install -r requirements.txt
```

### Dataflow Pipeline Execution
```bash
# Local execution
python your_pipeline.py --runner DirectRunner

# Cloud execution
python your_pipeline.py \
    --runner DataflowRunner \
    --project YOUR_PROJECT_ID \
    --region YOUR_REGION \
    --temp_location gs://YOUR_BUCKET/temp/ \
    --staging_location gs://YOUR_BUCKET/staging/
```

---

Congratulations! You now have a fully configured local development environment for Google Cloud Dataflow. You can start building and testing Apache Beam pipelines locally before deploying them to Google Cloud Dataflow for production use.

Remember to:
1. Always test with the DirectRunner first
2. Use appropriate service accounts with minimal required permissions
3. Monitor your pipeline execution and costs
4. Follow best practices for pipeline design and error handling

Happy coding with Apache Beam and Google Cloud Dataflow! 🚀
