import os
import logging
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, LargeBinary, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.exc import SQLAlchemyError, OperationalError
import time
import ssl

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

Base = declarative_base()

class Conversation(Base):
    """Database model for storing conversation sessions"""
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    metadata = Column(JSON)
    
    # Relationship to messages
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    """Database model for storing individual chat messages"""
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    file_data = Column(LargeBinary)  # For storing uploaded file data
    
    # Relationship to conversation
    conversation = relationship("Conversation", back_populates="messages")

def get_database_url():
    """Get database connection URL from environment variables"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return database_url

def create_engine_with_retry(max_retries=3, retry_delay=1):
    """Create SQLAlchemy engine with retry logic for connection issues"""
    database_url = get_database_url()
    
    # Configure SSL for PostgreSQL connections
    ssl_args = {}
    if database_url.startswith('postgresql://'):
        ssl_args = {
            'connect_args': {
                'sslmode': 'require',
                'ssl_cert': None,
                'ssl_key': None,
                'ssl_ca': None
            }
        }
    
    for attempt in range(max_retries):
        try:
            engine = create_engine(
                database_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                **ssl_args
            )
            
            # Test the connection
            with engine.connect() as conn:
                conn.execute("SELECT 1")
            
            logger.info("Database connection established successfully")
            return engine
            
        except (OperationalError, SQLAlchemyError) as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay * (2 ** attempt))  # Exponential backoff
            else:
                logger.error("Failed to establish database connection after all retries")
                raise

def get_db_session():
    """Get database session with connection pooling"""
    try:
        engine = create_engine_with_retry()
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        return SessionLocal()
    except Exception as e:
        logger.error(f"Error creating database session: {str(e)}")
        raise

def create_tables():
    """Create database tables if they don't exist"""
    try:
        engine = create_engine_with_retry()
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {str(e)}")
        raise

def create_conversation(session_id, metadata=None):
    """Create a new conversation record"""
    try:
        db = get_db_session()
        conversation = Conversation(
            session_id=session_id,
            metadata=metadata or {}
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        logger.info(f"Created conversation with ID: {conversation.id}")
        return conversation.id
    except Exception as e:
        logger.error(f"Error creating conversation: {str(e)}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close()

def save_message(conversation_id, role, content, file_data=None):
    """Save a message to the database"""
    try:
        db = get_db_session()
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            file_data=file_data
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        logger.info(f"Saved message with ID: {message.id}")
        return message.id
    except Exception as e:
        logger.error(f"Error saving message: {str(e)}")
        if db:
            db.rollback()
        raise
    finally:
        if db:
            db.close()

def get_conversation_messages(conversation_id, limit=50):
    """Retrieve messages for a conversation"""
    try:
        db = get_db_session()
        messages = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit).all()
        
        return [
            {
                'id': msg.id,
                'role': msg.role,
                'content': msg.content,
                'created_at': msg.created_at.isoformat(),
                'file_data': msg.file_data
            }
            for msg in messages
        ]
    except Exception as e:
        logger.error(f"Error retrieving conversation messages: {str(e)}")
        return []
    finally:
        if db:
            db.close()

def get_conversation_by_session_id(session_id):
    """Get conversation by session ID"""
    try:
        db = get_db_session()
        conversation = db.query(Conversation).filter(
            Conversation.session_id == session_id
        ).first()
        
        if conversation:
            return {
                'id': conversation.id,
                'session_id': conversation.session_id,
                'created_at': conversation.created_at.isoformat(),
                'updated_at': conversation.updated_at.isoformat(),
                'metadata': conversation.metadata
            }
        return None
    except Exception as e:
        logger.error(f"Error retrieving conversation: {str(e)}")
        return None
    finally:
        if db:
            db.close()

def update_conversation_metadata(conversation_id, metadata):
    """Update conversation metadata"""
    try:
        db = get_db_session()
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if conversation:
            conversation.metadata = metadata
            conversation.updated_at = datetime.utcnow()
            db.commit()
            logger.info(f"Updated conversation metadata for ID: {conversation_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error updating conversation metadata: {str(e)}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            db.close()

def delete_conversation(conversation_id):
    """Delete a conversation and all its messages"""
    try:
        db = get_db_session()
        conversation = db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        if conversation:
            db.delete(conversation)
            db.commit()
            logger.info(f"Deleted conversation with ID: {conversation_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        if db:
            db.rollback()
        return False
    finally:
        if db:
            db.close()

def get_conversation_stats(conversation_id):
    """Get statistics for a conversation"""
    try:
        db = get_db_session()
        message_count = db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).count()
        
        user_messages = db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.role == 'user'
        ).count()
        
        assistant_messages = db.query(Message).filter(
            Message.conversation_id == conversation_id,
            Message.role == 'assistant'
        ).count()
        
        return {
            'total_messages': message_count,
            'user_messages': user_messages,
            'assistant_messages': assistant_messages
        }
    except Exception as e:
        logger.error(f"Error getting conversation stats: {str(e)}")
        return None
    finally:
        if db:
            db.close()

# Initialize database tables on module import
try:
    create_tables()
except Exception as e:
    logger.warning(f"Could not initialize database tables: {str(e)}")
