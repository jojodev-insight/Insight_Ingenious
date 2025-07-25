---
title: "Installation Guide"
layout: single
permalink: /getting-started/installation/
sidebar:
  nav: "docs"
toc: true
toc_label: "Installation Steps"
toc_icon: "download"
---

# Installation Guide

This guide covers the complete installation process for Insight Ingenious, including optional dependencies for advanced features.

## Prerequisites

Before installing Insight Ingenious, ensure you have:

1. **Python 3.13 or higher** installed on your system
2. **Git** for cloning the repository
3. **uv** package manager (recommended) or pip

### Installing uv (Recommended)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Basic Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Insight-Services-APAC/ingenious.git
cd ingenious
```

### 2. Install Core Framework

```bash
# Using uv (recommended)
uv pip install -e .

# Or using pip
pip install -e .
```

This installs the core Insight Ingenious framework with basic functionality.

## Optional Dependencies

Some advanced features require additional dependencies. Install these extras based on your needs:

### Data Preparation and Web Crawling

For web scraping and data collection capabilities:

```bash
# Basic dataprep functionality
uv pip install -e ".[dataprep]"

# With testing capabilities
uv pip install -e ".[dataprep,tests]"
```

**Use cases:**
- Web scraping with Scrapfly integration
- Data collection from various web sources
- Automated content gathering

**Documentation:** [Data Preparation Guide](../guides/data-preparation/)

### Document Processing

For extracting content from various document formats:

```bash
# Core document processing (PyMuPDF + Azure Document Intelligence)
uv pip install -e ".[document-processing]"

# With additional engines and testing
uv pip install -e ".[document-processing,pdfminer,unstructured,tests]"
```

**Supported formats:**
- PDF, DOCX, PPTX
- PNG, JPG, JPEG, TIFF, TIF
- Rich text documents

**Engines included:**

| Extra name            | Purpose                                       | Packages                                   |
| --------------------- | --------------------------------------------- | ------------------------------------------ |
| `document-processing` | PyMuPDF extractor, Azure DI client & CLI     | `pymupdf`, `azure-ai-documentintelligence` |
| `pdfminer`            | Pure-Python PDF extractor (no native libs)   | `pdfminer.six`                             |
| `unstructured`        | DOCX/PPTX/rich-text extractor                | `unstructured[all-docs]`                   |

**Documentation:** [Document Processing Guide](../guides/document-processing/)

### Azure SQL Database Support

For production deployments using Azure SQL Database for chat history storage:

```bash
# Core Azure SQL support (pyodbc is included in base installation)
uv pip install -e .

# Required dependency for environment variable loading
uv add python-dotenv
```

**System Dependencies Required:**

On **macOS**:
```bash
# Install Microsoft ODBC Driver 18 for SQL Server
brew tap microsoft/mssql-release
brew install msodbcsql18 mssql-tools18

# Verify installation
odbcinst -q -d
```

On **Ubuntu/Debian**:
```bash
# Install Microsoft ODBC Driver 18 for SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install msodbcsql18
```

On **Windows**:
Download and install the ODBC Driver 18 for SQL Server from the [Microsoft website](https://docs.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server).

**Use cases:**
- Production chat history storage
- Enterprise-grade conversation persistence
- Multi-user conversation management
- Scalable message storage

**Additional Requirements:**
- Environment variable support via python-dotenv
- LOCAL_SQL_CSV_PATH configuration for sample data

**Documentation:** [Azure SQL Configuration Guide](../configuration/#chat-history)

### Complete Installation

To install all optional dependencies:

```bash
uv pip install -e ".[dataprep,document-processing,pdfminer,unstructured,tests]"
```

## Verification

After installation, verify that Insight Ingenious is working:

```bash
# Check CLI is available
ingen --help

# Verify installation
python -c "import ingenious; print('Insight Ingenious installed successfully')"
```

## Next Steps

1. **Configure the system** - See [Configuration Guide](../configuration/README.md)
2. **Understand workflows** - See [Workflows Guide](../workflows/README.md)
3. **Try the quick start** - See [Quick Start Guide](./README.md)

## Troubleshooting Installation

### Common Issues

**ImportError or missing dependencies:**
- Ensure you're using the correct Python environment
- Try reinstalling with the `--force-reinstall` flag
- Check that all required system dependencies are installed

**Permission errors:**
- Use a virtual environment instead of system-wide installation
- On macOS/Linux, avoid using `sudo` with pip

**Network issues:**
- Check your internet connection
- If behind a corporate firewall, configure proxy settings

For more troubleshooting help, see the [Troubleshooting Guide](/troubleshooting/).

## Development Installation

If you plan to contribute to Insight Ingenious:

```bash
# Install in development mode with all dependencies
uv pip install -e ".[dataprep,document-processing,pdfminer,unstructured,tests,dev]"

# Install pre-commit hooks
pre-commit install
```

See the [Development Guide](../development/README.md) for more details.
