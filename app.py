import streamlit as st
import os
import uuid
from datetime import datetime
from utils.db import get_db_session, create_conversation, save_message, get_conversation_messages
from utils.llm import GroqLLMClient
from utils.document_processor import DocumentProcessor
import base64

def load_custom_css():
    """Load custom CSS styling for the application"""
    st.markdown("""
    <style>
    @import url('https://fonts.cdnfonts.com/css/tw-cen-mt-std');
    
    * {
        font-family: 'Tw Cen MT Std', sans-serif !important;
    }
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
    }
    
    .main-header {
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .chat-container {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        margin-bottom: 2rem;
    }
    
    .message {
        margin-bottom: 1rem;
        padding: 1rem;
        border-radius: 10px;
        max-width: 80%;
    }
    
    .user-message {
        background: #2563eb;
        color: white;
        margin-left: auto;
        text-align: right;
    }
    
    .assistant-message {
        background: #f3f4f6;
        color: #1f2937;
        margin-right: auto;
    }
    
    .file-upload {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 2px dashed #d1d5db;
    }
    
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e5e7eb;
        padding: 12px 16px;
        font-size: 16px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2563eb;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    .stButton > button {
        background: #2563eb;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 36px;
        height: 36px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .stButton > button:hover {
        background: #1d4ed8;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    
    .streaming-response {
        background: #f8fafc;
        border-left: 4px solid #2563eb;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 0 8px 8px 0;
        font-family: 'Courier New', monospace;
        font-size: 14px;
        line-height: 1.5;
    }
    
    .typing-indicator {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #2563eb;
        animation: blink 1s infinite;
        margin-left: 4px;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0; }
    }
    
    .file-info {
        background: #e0f2fe;
        border: 1px solid #0288d1;
        border-radius: 8px;
        padding: 0.75rem;
        margin: 0.5rem 0;
        font-size: 14px;
    }
    
    .error-message {
        background: #fef2f2;
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1rem;
        color: #dc2626;
        margin: 1rem 0;
    }
    
    .success-message {
        background: #f0fdf4;
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1rem;
        color: #16a34a;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_session_state():
    """Initialize session state variables"""
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    if 'llm_client' not in st.session_state:
        st.session_state.llm_client = GroqLLMClient()
    
    if 'document_processor' not in st.session_state:
        st.session_state.document_processor = DocumentProcessor()

def handle_file_upload(uploaded_file):
    """Process uploaded file and extract text content"""
    if uploaded_file is None:
        return None, None
    
    try:
        # Process the document
        text_content = st.session_state.document_processor.process_document(uploaded_file)
        
        if text_content:
            # Create file info for display
            file_info = f"📄 **File Uploaded**: {uploaded_file.name}\n"
            file_info += f"📊 **Size**: {uploaded_file.size} bytes\n"
            file_info += f"📝 **Extracted Text Length**: {len(text_content)} characters\n"
            
            return text_content, file_info
        else:
            return None, "❌ **Error**: Could not extract text from the uploaded file."
    
    except Exception as e:
        st.error(f"Error processing file: {str(e)}")
        return None, f"❌ **Error**: {str(e)}"

def display_chat_history():
    """Display the chat history with proper styling"""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-message">
                <strong>You:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant-message">
                <strong>Assistant:</strong><br>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)

def stream_response(prompt, file_content=None):
    """Stream the LLM response in real-time"""
    try:
        # Prepare the full prompt
        full_prompt = prompt
        if file_content:
            full_prompt += f"\n\nDocument Content:\n{file_content}"
        
        # Create a placeholder for streaming
        response_placeholder = st.empty()
        
        # Stream the response
        response_text = ""
        for chunk in st.session_state.llm_client.chat_completion_stream([
            {"role": "user", "content": full_prompt}
        ]):
            if chunk and chunk.strip():
                response_text += chunk
                # Update the placeholder with current response and typing indicator
                response_placeholder.markdown(f"""
                <div class="streaming-response">
                    {response_text}<span class="typing-indicator"></span>
                </div>
                """, unsafe_allow_html=True)
        
        # Final update without typing indicator
        response_placeholder.markdown(f"""
        <div class="streaming-response">
            {response_text}
        </div>
        """, unsafe_allow_html=True)
        
        return response_text
    
    except Exception as e:
        st.error(f"Error generating response: {str(e)}")
        return None

def main():
    """Main application function"""
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Smart Expense Agent</h1>', unsafe_allow_html=True)
    
    # Main container
    with st.container():
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        # File upload section
        st.markdown("### 📁 Upload Expense Document")
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=['pdf', 'png', 'jpg', 'jpeg', 'txt', 'csv'],
            help="Upload your expense document for analysis"
        )
        
        # Process uploaded file
        file_content = None
        if uploaded_file is not None:
            file_content, file_info = handle_file_upload(uploaded_file)
            if file_info:
                st.markdown(f'<div class="file-info">{file_info}</div>', unsafe_allow_html=True)
        
        # Chat interface
        st.markdown("### 💬 Chat with AI Assistant")
        
        # Display chat history
        if st.session_state.messages:
            display_chat_history()
        
        # Chat input
        user_input = st.text_input(
            "Ask me about your expense document or any expense-related questions:",
            key="user_input",
            placeholder="e.g., 'Analyze this expense report' or 'What are the total expenses?'"
        )
        
        # Send button
        col1, col2, col3 = st.columns([1, 0.1, 1])
        with col2:
            send_button = st.button("➤", key="send_button")
        
        # Handle user input
        if send_button and user_input:
            # Add user message to session
            st.session_state.messages.append({"role": "user", "content": user_input})
            
            # Save to database if conversation exists
            if st.session_state.conversation_id:
                try:
                    save_message(
                        st.session_state.conversation_id,
                        "user",
                        user_input,
                        uploaded_file.read() if uploaded_file else None
                    )
                except Exception as e:
                    st.warning(f"Could not save message to database: {str(e)}")
            
            # Generate and stream response
            with st.spinner("🤔 Thinking..."):
                response = stream_response(user_input, file_content)
            
            if response:
                # Add assistant response to session
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Save to database if conversation exists
                if st.session_state.conversation_id:
                    try:
                        save_message(st.session_state.conversation_id, "assistant", response)
                    except Exception as e:
                        st.warning(f"Could not save response to database: {str(e)}")
            
            # Clear input
            st.session_state.user_input = ""
            st.rerun()
        
        # Initialize conversation in database
        if st.session_state.conversation_id is None:
            try:
                st.session_state.conversation_id = create_conversation(st.session_state.session_id)
                st.success("✅ Conversation initialized successfully!")
            except Exception as e:
                st.warning(f"⚠️ Could not initialize database connection: {str(e)}")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar with information
    with st.sidebar:
        st.markdown("### ℹ️ About")
        st.markdown("""
        **Smart Expense Agent** is an AI-powered assistant that helps you:
        
        📊 **Analyze expense documents**
        💰 **Calculate totals and categories**
        ✅ **Validate expense policies**
        📝 **Generate expense reports**
        
        Upload your expense documents and chat with the AI to get insights!
        """)
        
        st.markdown("### 🔧 Features")
        st.markdown("""
        ✅ **Multi-format support**: PDF, Images, Text files
        ✅ **Real-time streaming**: Instant responses
        ✅ **Document analysis**: Intelligent text extraction
        ✅ **Conversation history**: Persistent chat sessions
        ✅ **Professional UI**: Enhanced user experience
        """)
        
        st.markdown("### 🛠️ Technical Stack")
        st.markdown("""
        - **Frontend**: Streamlit 1.38.0
        - **AI/LLM**: Groq API
        - **Database**: PostgreSQL
        - **Document Processing**: Multi-format pipeline
        """)

if __name__ == "__main__":
    main()
