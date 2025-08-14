# 🤖 Smart Expense Agent

An AI-powered expense processing application built with Streamlit and PostgreSQL. Upload expense documents and chat with an intelligent AI assistant to analyze, categorize, and process your expenses.

## ✨ Features

- **📄 Multi-format Document Support**: Upload PDFs, images, and text files
- **💬 Intelligent Chat Interface**: Real-time streaming responses with professional UI
- **🔍 Advanced Document Analysis**: AI-powered text extraction and analysis
- **💾 Persistent Storage**: PostgreSQL database for conversation history
- **🎨 Professional UI**: Enhanced styling with Tw Cen MT font and modern design
- **⚡ Real-time Streaming**: Token-by-token response generation
- **🛡️ Robust Error Handling**: Comprehensive error recovery and fallback mechanisms

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Groq API key

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/valonys/smart_agent.git
   cd smart_agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Create .env file
   echo "DATABASE_URL=postgresql://username:password@localhost:5432/database_name" > .env
   echo "GROQ_API_KEY=your_groq_api_key_here" >> .env
   echo "GROQ_MODEL=llama-3.3-70b-versatile" >> .env
   ```

4. **Run the application**
   ```bash
   streamlit run app.py
   ```

5. **Open your browser**
   Navigate to `http://localhost:8501`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Yes | - |
| `GROQ_API_KEY` | Groq API authentication key | Yes | - |
| `GROQ_MODEL` | LLM model to use | No | `llama-3.3-70b-versatile` |

### Database Setup

1. **Create PostgreSQL database**
   ```sql
   CREATE DATABASE smart_expense_agent;
   ```

2. **Tables are created automatically** when the application starts

## 📖 Usage

### Uploading Documents

1. **Supported Formats**:
   - PDF files (`.pdf`)
   - Images (`.png`, `.jpg`, `.jpeg`)
   - Text files (`.txt`, `.csv`)

2. **File Size Limit**: 50MB maximum

### Chat Interface

- **Ask questions** about your uploaded documents
- **Get expense analysis** and categorization
- **Validate expense policies** against company rules
- **Generate expense reports** automatically

### Example Queries

- "What are the total expenses in this document?"
- "Categorize these expenses by type"
- "Are there any policy violations in this expense report?"
- "Generate a summary of travel expenses"

## 🏗️ Architecture

### Core Components

- **Frontend**: Streamlit 1.38.0 with custom CSS styling
- **Backend**: Python with modular utility packages
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: Groq LLM API for document analysis
- **Document Processing**: Multi-format support with fallback mechanisms

### Directory Structure

```
smart-expense-agent/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── LICENSE                  # MIT License
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── utils/
    ├── __init__.py          # Package initialization
    ├── db.py                # Database models and operations
    ├── llm.py               # LLM wrapper and completions
    └── document_processor.py # Document processing pipeline
```

## 🛠️ Development

### Setting up Development Environment

1. **Clone and install dependencies**
   ```bash
   git clone https://github.com/valonys/smart_agent.git
   cd smart_agent
   pip install -r requirements.txt
   ```

2. **Run tests**
   ```bash
   pytest
   ```

3. **Code formatting**
   ```bash
   black .
   ```

4. **Type checking**
   ```bash
   mypy .
   ```

### Adding New Features

1. **Document Processing**: Extend `utils/document_processor.py`
2. **Database Models**: Add to `utils/db.py`
3. **UI Components**: Modify `app.py`
4. **LLM Integration**: Update `utils/llm.py`

## 🚀 Deployment

### Local Deployment

```bash
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

### Production Deployment

1. **Set up PostgreSQL database**
2. **Configure environment variables**
3. **Use process manager (PM2, systemd)**
4. **Set up reverse proxy (nginx)**

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -e .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/valonys/smart_agent/issues)
- **Documentation**: [Wiki](https://github.com/valonys/smart_agent/wiki)
- **Email**: team@smartexpenseagent.com

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the web framework
- [Groq](https://groq.com/) for the LLM API
- [PostgreSQL](https://www.postgresql.org/) for the database
- [SQLAlchemy](https://www.sqlalchemy.org/) for the ORM

---

**Made with ❤️ by the Smart Expense Agent Team**
