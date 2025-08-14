import os
import logging
import time
from typing import List, Dict, Any, Generator
import groq
from groq import GroqError, RateLimitError, APIError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GroqLLMClient:
    """Wrapper class for Groq LLM API with streaming support and error handling"""
    
    def __init__(self, api_key: str = None, model: str = None):
        """Initialize the Groq LLM client"""
        self.api_key = api_key or os.getenv('GROQ_API_KEY')
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        self.model = model or os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')
        self.client = groq.Groq(api_key=self.api_key)
        
        # Configuration
        self.max_retries = 3
        self.retry_delay = 1
        self.max_tokens = 4096
        self.temperature = 0.7
        
        logger.info(f"Initialized Groq LLM client with model: {self.model}")
    
    def chat_completion(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Generate a chat completion response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                stream=False
            )
            
            return self._validate_response(response)
            
        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded: {str(e)}")
            return self._handle_rate_limit(messages, **kwargs)
            
        except APIError as e:
            logger.error(f"API error: {str(e)}")
            return self._handle_api_error(e, messages, **kwargs)
            
        except Exception as e:
            logger.error(f"Unexpected error in chat completion: {str(e)}")
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def chat_completion_stream(self, messages: List[Dict[str, str]], **kwargs) -> Generator[str, None, None]:
        """Generate a streaming chat completion response"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=kwargs.get('max_tokens', self.max_tokens),
                temperature=kwargs.get('temperature', self.temperature),
                stream=True
            )
            
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except RateLimitError as e:
            logger.warning(f"Rate limit exceeded during streaming: {str(e)}")
            yield self._handle_rate_limit(messages, **kwargs)
            
        except APIError as e:
            logger.error(f"API error during streaming: {str(e)}")
            yield self._handle_api_error(e, messages, **kwargs)
            
        except Exception as e:
            logger.error(f"Unexpected error in streaming completion: {str(e)}")
            yield f"I apologize, but I encountered an error: {str(e)}"
    
    def _validate_response(self, response) -> str:
        """Validate and extract content from API response"""
        try:
            if hasattr(response, 'choices') and response.choices:
                content = response.choices[0].message.content
                if content:
                    return content.strip()
                else:
                    logger.warning("Empty response content received")
                    return "I apologize, but I received an empty response. Please try again."
            else:
                logger.error("Invalid response format")
                return "I apologize, but I received an invalid response format."
                
        except Exception as e:
            logger.error(f"Error validating response: {str(e)}")
            return "I apologize, but I encountered an error processing the response."
    
    def _handle_rate_limit(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """Handle rate limit errors with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                wait_time = self.retry_delay * (2 ** attempt)
                logger.info(f"Rate limited, waiting {wait_time} seconds before retry {attempt + 1}")
                time.sleep(wait_time)
                
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=kwargs.get('max_tokens', self.max_tokens),
                    temperature=kwargs.get('temperature', self.temperature),
                    stream=False
                )
                
                return self._validate_response(response)
                
            except RateLimitError:
                if attempt == self.max_retries - 1:
                    return "I apologize, but I'm currently experiencing high demand. Please try again in a few moments."
                continue
            except Exception as e:
                logger.error(f"Error during rate limit retry: {str(e)}")
                return f"I apologize, but I encountered an error: {str(e)}"
        
        return "I apologize, but I'm currently experiencing high demand. Please try again in a few moments."
    
    def _handle_api_error(self, error: APIError, messages: List[Dict[str, str]], **kwargs) -> str:
        """Handle API errors with appropriate responses"""
        error_code = getattr(error, 'status_code', None)
        
        if error_code == 401:
            logger.error("Authentication failed - check API key")
            return "I apologize, but there's an authentication issue. Please check your API configuration."
        
        elif error_code == 403:
            logger.error("Access forbidden - check API permissions")
            return "I apologize, but I don't have permission to access this service."
        
        elif error_code == 429:
            logger.error("Rate limit exceeded")
            return "I apologize, but I'm currently experiencing high demand. Please try again in a few moments."
        
        elif error_code >= 500:
            logger.error(f"Server error: {error_code}")
            return "I apologize, but the service is currently experiencing technical difficulties. Please try again later."
        
        else:
            logger.error(f"API error {error_code}: {str(error)}")
            return f"I apologize, but I encountered an error: {str(error)}"
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about the current model"""
        return {
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature,
            'provider': 'Groq'
        }
    
    def update_config(self, **kwargs):
        """Update client configuration"""
        if 'max_tokens' in kwargs:
            self.max_tokens = kwargs['max_tokens']
        if 'temperature' in kwargs:
            self.temperature = kwargs['temperature']
        if 'model' in kwargs:
            self.model = kwargs['model']
        
        logger.info(f"Updated configuration: {kwargs}")
    
    def test_connection(self) -> bool:
        """Test the connection to the Groq API"""
        try:
            # Simple test with minimal tokens
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
                stream=False
            )
            
            if response.choices[0].message.content:
                logger.info("Groq API connection test successful")
                return True
            else:
                logger.warning("Groq API connection test failed - empty response")
                return False
                
        except Exception as e:
            logger.error(f"Groq API connection test failed: {str(e)}")
            return False
