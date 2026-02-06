# Google Cloud Dataflow Development Environment

🚀 A comprehensive local development environment for building and testing Apache Beam pipelines with Google Cloud Dataflow.

## 📋 Overview

This repository provides a complete setup for developing Apache Beam pipelines locally and deploying them to Google Cloud Dataflow. It includes all necessary configurations, dependencies, and best practices for Dataflow development.

## 🛠️ Features

- ✅ **Virtual Environment Setup**: Isolated Python environment with `.venv`
- ✅ **Apache Beam SDK**: Latest stable version with Google Cloud integration
- ✅ **Development Tools**: Pre-configured linting, formatting, and testing
- ✅ **IDE Integration**: VS Code configuration with Python and Cloud extensions
- ✅ **Dependency Management**: Version-locked requirements for reproducibility
- ✅ **Project Structure**: Best practice directory layout
- ✅ **Documentation**: Comprehensive setup and troubleshooting guide

## 🏗️ Project Structure

```
dataflow-learning/
├── src/                          # Source code
│   ├── pipelines/                # Dataflow pipelines
│   │   ├── __init__.py
│   │   ├── example_pipeline.py  # Example pipeline
│   │   └── utils.py             # Utility functions
│   └── tests/                    # Test files
│       ├── __init__.py
│       ├── test_example_pipeline.py
│       └── test_utils.py
├── .venv/                        # Virtual environment
├── .vscode/                      # VS Code configuration
│   └── settings.json
├── requirements.txt              # Python dependencies
├── setup.py                      # Package setup
├── .env.example                  # Environment variables template
├── .gitignore                    # Git ignore rules
├── Google_Cloud_Dataflow_Local_Setup_Guide.md  # Setup guide
└── README.md                     # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+ (recommended 3.11)
- Google Cloud account with billing enabled
- Git installed

### Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd dataflow-learning
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Google Cloud**
   ```bash
   gcloud init
   gcloud auth application-default login
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your project details
   ```

### Run Your First Pipeline

```bash
# Local execution
python src/pipelines/example_pipeline.py --runner DirectRunner

# Cloud execution
python src/pipelines/example_pipeline.py \
    --runner DataflowRunner \
    --project YOUR_PROJECT_ID \
    --region us-central1 \
    --temp_location gs://YOUR_BUCKET/temp/
```

## 📚 Documentation

- 📖 [Complete Setup Guide](./Google_Cloud_Dataflow_Local_Setup_Guide.md)
- 🔧 [Configuration Guide](#configuration)
- 🧪 [Testing Guide](#testing)
- 🚀 [Deployment Guide](#deployment)

## 🛠️ Development

### Code Quality Tools

- **Black**: Code formatting
- **Flake8**: Linting
- **MyPy**: Type checking
- **Pytest**: Testing framework

### Common Commands

```bash
# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/

# Run tests
pytest src/tests/

# Install development dependencies
pip install -r requirements.txt
```

## 🐳 Docker Support

Optional Docker configuration for containerized development:

```bash
# Build Docker image
docker build -t dataflow-dev .

# Run container
docker run -it dataflow-dev
```

## 🌐 Cloud Integration

### Required Google Cloud APIs

- Dataflow API
- Cloud Storage API
- Cloud Logging API
- Cloud Monitoring API

### Service Account Setup

```bash
# Create service account
gcloud iam service-accounts create dataflow-developer

# Grant necessary roles
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:dataflow-developer@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/dataflow.developer"
```

## 🧪 Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest src/tests/test_example_pipeline.py
```

### Test Structure

```
src/tests/
├── test_example_pipeline.py  # Pipeline integration tests
├── test_utils.py            # Utility function tests
└── fixtures/                # Test data files
```

## 📊 Monitoring

### Local Monitoring

- Pipeline logs via console output
- Local file system for intermediate results

### Cloud Monitoring

- Google Cloud Console: Dataflow Jobs
- Cloud Logging: Structured logs
- Cloud Monitoring: Metrics and alerts

## 🔧 Configuration

### Environment Variables

Create `.env` file from `.env.example`:

```env
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_REGION=us-central1
DATAFLOW_TEMP_LOCATION=gs://your-bucket/temp/
DATAFLOW_STAGING_LOCATION=gs://your-bucket/staging/
```

### VS Code Settings

The `.vscode/settings.json` file provides:
- Python interpreter configuration
- Linting and formatting settings
- Test discovery configuration
- Google Cloud integration

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Workflow

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -r requirements.txt

# Run pre-commit checks
black src/
flake8 src/
mypy src/
pytest src/tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Google Cloud Dataflow Documentation](https://cloud.google.com/dataflow/docs)
- 📖 [Apache Beam Documentation](https://beam.apache.org/documentation/)
- 🐛 [Issues](https://github.com/your-username/dataflow-learning/issues)
- 💬 [Discussions](https://github.com/your-username/dataflow-learning/discussions)

## 🙏 Acknowledgments

- [Apache Beam](https://beam.apache.org/) - Unified programming model
- [Google Cloud Dataflow](https://cloud.google.com/dataflow) - Managed service
- [VS Code](https://code.visualstudio.com/) - Development environment

---

**Happy Dataflow Development! 🎉**

Built with ❤️ for the Apache Beam and Google Cloud community.
