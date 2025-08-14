# Smart Expense Agent - Codebase Documentation

## Overview

The Smart Expense Agent is a sophisticated AI-powered expense processing application built with Streamlit and PostgreSQL. It provides an intelligent conversational interface for employees to submit and process expense documents through advanced document analysis and policy validation.

## Architecture Summary

- **Frontend**: Streamlit 1.38.0 with custom CSS styling and real-time streaming
- **Backend**: Python with modular utility packages
- **Database**: PostgreSQL with SQLAlchemy ORM
- **AI/ML**: Groq LLM API for document analysis and chat completions
- **Document Processing**: Multi-format support with fallback mechanisms

## Directory Structure

```
smart-expense-agent/
├── app.py                    # Main Streamlit application (407 lines)
├── pyproject.toml           # Python dependencies and project configuration
├── uv.lock                  # Dependency lock file
├── replit.md                # Project documentation and user preferences
├── README.md                # Project documentation and installation guide
├── DEPLOYMENT_GUIDE.md      # GitHub deployment instructions
├── LICENSE                  # MIT License
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── config.toml          # Streamlit server configuration
└── utils/
    ├── __init__.py          # Package initialization (1 line)
    ├── db.py                # Database models and connections (141 lines)
    ├── llm.py               # LLM wrapper and completions (98 lines)
    └── document_processor.py # Document processing pipeline (86 lines)
```

## Core Components

### 1. Main Application (`app.py` - 407 lines)

**Purpose**: Primary Streamlit application with enhanced UI and chat interface

**Key Features**:
- Custom CSS styling with Tw Cen MT font throughout application
- Professional chat input with rounded corners and blue send button (36x36px)
- Real-time token streaming with typing indicators
- File upload interface supporting PDFs, images, and spreadsheets
- Session state management for conversation persistence
- Database integration for storing conversations and messages

**Main Functions**:
- `load_custom_css()`: Applies comprehensive CSS styling
- `initialize_session_state()`: Sets up session variables
- `handle_file_upload()`: Processes uploaded documents
- `display_chat_history()`: Renders conversation messages
- `stream_response()`: Handles real-time token streaming
- Main execution loop with Streamlit interface

**Dependencies**:
- `streamlit`: Web framework
- `utils.db`: Database operations
- `utils.llm`: LLM integration
- `utils.document_processor`: Document processing

### 2. Database Layer (`utils/db.py` - 141 lines)

**Purpose**: Database models, connections, and ORM operations

**Key Components**:

**Models**:
- `Conversation`: Tracks user sessions with metadata
  - `id`: Primary key
  - `session_id`: Unique session identifier
  - `created_at`: Timestamp
  - `updated_at`: Timestamp
  - `metadata`: JSON field for additional data

- `Message`: Stores individual chat messages
  - `id`: Primary key
  - `conversation_id`: Foreign key to Conversation
  - `role`: User or assistant
  - `content`: Message text
  - `created_at`: Timestamp
  - `file_data`: Binary field for uploaded files

**Connection Management**:
- `get_database_url()`: Retrieves connection string from environment
- `create_engine_with_retry()`: Creates SQLAlchemy engine with retry logic
- `get_db_session()`: Provides database session with connection pooling
- SSL connection support with certificate verification

**Operations**:
- `create_conversation()`: Creates new conversation record
- `save_message()`: Stores chat messages with file data
- `get_conversation_messages()`: Retrieves message history

**Error Handling**:
- Connection retry logic with exponential backoff
- Comprehensive error logging
- Graceful degradation for database failures

### 3. LLM Integration (`utils/llm.py` - 98 lines)

**Purpose**: Groq API wrapper with streaming support and error handling

**Key Components**:

**Classes**:
- `GroqLLMClient`: Main wrapper for Groq API interactions
  - Initialization with API key validation
  - Model configuration (defaults to llama-3.3-70b-versatile)
  - Error handling and retry mechanisms

**Methods**:
- `chat_completion()`: Standard chat completions
- `chat_completion_stream()`: Real-time token streaming
- `_validate_response()`: Response validation and error checking
- `_handle_api_error()`: Comprehensive error handling

**Features**:
- Environment variable configuration
- Token-by-token streaming for real-time responses
- Comprehensive error handling for API failures
- Rate limiting and retry logic
- Response validation and sanitization

**Error Handling**:
- API key validation
- Network error recovery
- Rate limit handling
- Response format validation

### 4. Document Processing (`utils/document_processor.py` - 86 lines)

**Purpose**: Multi-format document text extraction with fallback mechanisms

**Key Components**:

**Classes**:
- `DocumentProcessor`: Main document processing class
  - PDF processing with pdfplumber and PyPDF2 fallback
  - Image processing with Pillow
  - Text file handling
  - Error handling for various document formats

**Methods**:
- `process_document()`: Main entry point for document processing
- `extract_text_from_pdf()`: PDF text extraction with fallback
- `extract_text_from_image()`: Image text extraction (placeholder)
- `extract_text_from_file()`: General file handling
- `_validate_file()`: File validation and security checks

**Supported Formats**:
- PDF files (pdfplumber primary, PyPDF2 fallback)
- Images (PNG, JPEG, JPG)
- Text files (TXT, CSV)
- Spreadsheets (preparation for future enhancement)

**Error Handling**:
- File format validation
- Corruption detection
- Fallback mechanisms for failed extractions
- Security validation for uploaded files

## Configuration Files

### Streamlit Configuration (`.streamlit/config.toml`)

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
base = "light"
```

**Purpose**: Optimizes Streamlit for deployment and user experience

### Dependencies (`pyproject.toml`)

**Core Dependencies**:
- `streamlit==1.38.0`: Latest version with enhanced features
- `sqlalchemy>=2.0.43`: Modern ORM with async support
- `psycopg2-binary>=2.9.10`: PostgreSQL adapter
- `groq>=0.31.0`: AI/LLM integration
- `pdfplumber>=0.11.7`: Primary PDF text extraction
- `pypdf2>=3.0.1`: Fallback PDF processing
- `pillow==10.4.0`: Image processing (compatible with Streamlit 1.38.0)
- `python-dotenv>=1.1.1`: Environment variable management
- `numpy>=2.3.2`: Numerical computing support

## UI/UX Features

### Custom CSS Styling

**Font Integration**:
- Tw Cen MT Std font loaded from CDNFonts
- Applied consistently across entire application
- Professional appearance with brand consistency

**Chat Interface**:
- Professional chat input with 900px max width
- Rounded corners (12px border-radius)
- Enhanced focus states with blue accent (#2563eb)
- Smooth transitions and animations

**Send Button**:
- Blue background (#2563eb) with hover effects
- Reduced size (36x36px) for professional appearance
- Rounded corners (8px) with centered icon
- Transition effects for user feedback

**Real-Time Streaming**:
- Token-by-token response display
- Typing cursor animation with blinking effect
- Streaming response container with proper spacing
- Visual feedback during response generation

## Database Schema

### Conversations Table
```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB
);
```

### Messages Table
```sql
CREATE TABLE messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER REFERENCES conversations(id),
    role VARCHAR(20) NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    file_data BYTEA
);
```

## Environment Variables

**Required**:
- `DATABASE_URL`: PostgreSQL connection string
- `GROQ_API_KEY`: Authentication for Groq LLM service

**Optional**:
- `GROQ_MODEL`: Model specification (defaults to llama-3.3-70b-versatile)

## Error Handling Strategy

### Database Errors
- Connection retry with exponential backoff
- Graceful degradation when database unavailable
- Transaction rollback on failures
- Comprehensive error logging

### API Errors
- Groq API key validation
- Rate limit handling with backoff
- Network error recovery
- Response validation and sanitization

### File Processing Errors
- File format validation
- Corruption detection and handling
- Fallback extraction mechanisms
- Security validation for uploads

### UI/UX Error Handling
- User-friendly error messages
- Graceful degradation of features
- Progress indicators during processing
- Clear feedback for failed operations

## Security Considerations

### Environment Variables
- Sensitive data stored in environment variables
- No hardcoded API keys or database credentials
- Proper .gitignore to exclude sensitive files

### Database Security
- SSL connections with certificate verification
- Parameterized queries to prevent SQL injection
- Input validation and sanitization
- Connection pooling with proper cleanup

### File Upload Security
- File type validation
- Size limitations
- Content validation
- Binary data storage in database

## Performance Optimizations

### Database
- Connection pooling for efficient resource usage
- Indexed queries for conversation retrieval
- Lazy loading of message history
- Efficient binary data storage

### Streaming
- Real-time token streaming for better UX
- Efficient memory usage during streaming
- Progressive response building
- Client-side rendering optimizations

### Caching
- Session state management
- CSS caching for faster load times
- Font loading optimization
- Static asset optimization

## Development Guidelines

### Code Style
- Consistent indentation and formatting
- Comprehensive docstrings for all functions
- Type hints where appropriate
- Clear variable and function naming

### Testing Strategy
- Unit tests for utility functions
- Integration tests for database operations
- Mock testing for external API calls
- End-to-end testing for complete workflows

### Documentation
- Inline code comments for complex logic
- README with installation instructions
- API documentation for utility functions
- Architecture documentation (this file)

## Deployment Configuration

### Replit Deployment
- Pre-configured workflow for automatic startup
- Environment variable integration
- Port configuration (5000) for Replit infrastructure
- Optimized for Replit's container environment

### General Deployment
- Docker-ready configuration
- Environment variable configuration
- Health check endpoints
- Logging configuration for production

## Future Enhancements

### Planned Features
- Advanced OCR for image text extraction
- Excel/CSV processing capabilities
- Multi-language support
- Advanced policy validation rules
- Email integration for expense reports
- Mobile-responsive design improvements

### Technical Improvements
- Async database operations
- Enhanced caching strategies
- Performance monitoring
- Advanced error tracking
- Automated testing pipeline

## Maintenance Notes

### Regular Updates
- Dependency updates and security patches
- Database schema migrations
- Performance monitoring and optimization
- User feedback integration

### Monitoring
- Application performance metrics
- Database connection health
- API response times
- Error rate tracking

This codebase represents a production-ready application with comprehensive features, robust error handling, and professional UI design optimized for expense processing workflows.