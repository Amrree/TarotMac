"""
Mock Ollama module for testing when ollama is not available.
"""

class Client:
    """Mock Ollama client for testing."""
    
    def __init__(self, host="http://localhost:11434"):
        self.host = host
        self.models = [
            {"name": "llama3.2:3b"},
            {"name": "llama3.2:1b"},
            {"name": "llama3.1:8b"}
        ]
    
    def list(self):
        """Mock list models."""
        return {"models": self.models}
    
    def generate(self, model, prompt, options=None):
        """Mock generate response."""
        return {
            "response": '{"reading_id": "test", "summary": "Test summary", "cards": [], "advice": [], "follow_up_questions": []}'
        }
    
    def chat(self, model, messages, stream=False, options=None):
        """Mock chat response."""
        if stream:
            # Return a generator for streaming
            def stream_generator():
                chunks = ["Test ", "response ", "from ", "mock ", "Ollama"]
                for chunk in chunks:
                    yield {"message": {"content": chunk}}
            return stream_generator()
        else:
            return {"message": {"content": "Test response from mock Ollama"}}
    
    def pull(self, model_name):
        """Mock pull model."""
        pass


# Mock the ollama module
import sys
ollama_module = type(sys)('ollama')
ollama_module.Client = Client
sys.modules['ollama'] = ollama_module

# Export the module
__all__ = ['Client']