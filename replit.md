# Smart Expense Agent - Replit Configuration

## Project Overview

This is an AI-powered expense processing application built with Streamlit and PostgreSQL. The application provides an intelligent conversational interface for employees to submit and process expense documents through advanced document analysis and policy validation.

## Features

- **Multi-format Document Support**: Upload PDFs, images, and text files
- **Real-time Streaming**: Token-by-token response generation
- **Professional UI**: Enhanced styling with Tw Cen MT font
- **Database Integration**: PostgreSQL with SQLAlchemy ORM
- **AI/LLM Integration**: Groq API for intelligent document analysis
- **Robust Error Handling**: Comprehensive error recovery mechanisms

## User Preferences

### Development Environment
- **Language**: Python 3.11
- **Framework**: Streamlit 1.38.0
- **Database**: PostgreSQL
- **AI Provider**: Groq LLM API

### UI/UX Preferences
- **Font**: Tw Cen MT Std (professional appearance)
- **Color Scheme**: Blue gradient background (#667eea to #764ba2)
- **Chat Interface**: Professional styling with rounded corners
- **Real-time Streaming**: Token-by-token response display
- **File Upload**: Drag-and-drop interface with format validation

### Technical Preferences
- **Error Handling**: Comprehensive logging and user-friendly error messages
- **Security**: Environment variable configuration, file validation
- **Performance**: Connection pooling, caching, optimized queries
- **Documentation**: Comprehensive inline comments and external guides

## Configuration

### Environment Variables Required
```bash
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### Dependencies
- streamlit==1.38.0
- sqlalchemy>=2.0.43
- psycopg2-binary>=2.9.10
- groq>=0.31.0
- pdfplumber>=0.11.7
- pypdf2>=3.0.1
- pillow==10.4.0
- python-dotenv>=1.1.1
- numpy>=2.3.2

## Project Structure

```
smart-expense-agent/
├── app.py                    # Main Streamlit application (407 lines)
├── pyproject.toml           # Python dependencies
├── replit.md                # This file
├── README.md                # Project documentation
├── DEPLOYMENT_GUIDE.md      # Deployment instructions
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── config.toml          # Streamlit configuration
└── utils/
    ├── __init__.py          # Package initialization
    ├── db.py                # Database models (141 lines)
    ├── llm.py               # LLM wrapper (98 lines)
    └── document_processor.py # Document processing (86 lines)
```

## Development Notes

### Code Quality
- Comprehensive error handling throughout
- Type hints where appropriate
- Detailed docstrings for all functions
- Consistent code formatting with Black
- Modular architecture for maintainability

### Security Considerations
- Environment variable configuration
- File upload validation
- SQL injection prevention
- Input sanitization
- Secure database connections

### Performance Optimizations
- Database connection pooling
- Efficient file processing
- Streaming responses
- Caching strategies
- Optimized queries

## Deployment

The application is designed to be deployed on various platforms:
- **Local Development**: Streamlit run
- **Docker**: Containerized deployment
- **Cloud Platforms**: Heroku, Railway, DigitalOcean
- **Production**: Full security and monitoring setup

## Support

For technical support or questions:
- **Documentation**: README.md and DEPLOYMENT_GUIDE.md
- **Issues**: GitHub repository issues
- **Contact**: team@smartexpenseagent.com

---

**Smart Expense Agent Team** - Building intelligent expense processing solutions
