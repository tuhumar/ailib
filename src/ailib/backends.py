import abc
import json
import sys
import time
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, Optional, List, TypeVar, Union

# --- Logging Configuration with Rotation ---
logger = logging.getLogger("ailib")

def _setup_logging():
    if logger.handlers:
        return

    # Log level (default INFO)
    log_level = os.getenv("AILIB_LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))

    formatter = logging.Formatter('[%(asctime)s][%(name)s] %(levelname)s: %(message)s')

    # If the user defined a log file
    log_file = os.getenv("AILIB_LOG_FILE")
    if log_file:
        # Rotation settings via environment variables
        max_bytes = int(os.getenv("AILIB_LOG_MAX_BYTES", 5 * 1024 * 1024)) # Default 5MB
        backup_count = int(os.getenv("AILIB_LOG_BACKUP_COUNT", 3))         # Keep 3 old files
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=max_bytes, 
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # Always keep StreamHandler for stderr for immediate visibility
    if os.getenv("AILIB_LOG_STDERR", "true").lower() == "true":
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

_setup_logging()

T = TypeVar('T')

class AILibError(Exception):
    """Base exception for ailib."""
    pass

class AILibTimeoutError(AILibError):
    """Raised when the AI agent takes too long to respond."""
    pass

class Backend(abc.ABC):
    """Abstract base class for ailib communication backends."""
    
    @abc.abstractmethod
    def request(self, prompt: str, context: Optional[Any] = None, options: Optional[List[str]] = None) -> str:
        """Send a request to the AI Agent and wait for the response."""
        pass

class StdinBackend(Backend):
    """
    Standard input/output backend.
    Writes structured markers to stderr and reads response from stdin.
    """
    
    def request(self, prompt: str, context: Optional[Any] = None, options: Optional[List[str]] = None) -> str:
        request_data = {
            "prompt": prompt,
            "context": context,
            "options": options
        }
        
        # Structured markers for automation via stderr
        sys.stderr.write("\n<<<AILIB_REQUEST_START>>>\n")
        sys.stderr.write(json.dumps(request_data, indent=2))
        sys.stderr.write("\n<<<AILIB_REQUEST_END>>>\n")
        sys.stderr.flush()
        
        message = f"AI Action Required: {prompt}"
        if options:
            message += f" (Options: {', '.join(options)})"
        
        logger.info(message)
        
        try:
            # Block and wait for response from stdin
            response = input("> ").strip()
            return response
        except EOFError:
            logger.error("stdin closed before receiving response.")
            return ""

class FileBackend(Backend):
    """
    File-based polling backend with timeout support.
    Useful in environments where stdin/stderr are not interactive.
    """
    def __init__(
        self, 
        request_path: Optional[str] = None, 
        response_path: Optional[str] = None, 
        poll_interval: float = 0.5,
        default_timeout: Optional[float] = None
    ):
        self.request_path = request_path or os.getenv("AILIB_FILE_REQUEST", "ailib_request.json")
        self.response_path = response_path or os.getenv("AILIB_FILE_RESPONSE", "ailib_response.json")
        self.poll_interval = poll_interval
        
        env_timeout = os.getenv("AILIB_TIMEOUT")
        self.default_timeout = default_timeout or (float(env_timeout) if env_timeout else 60.0)

    def request(
        self, 
        prompt: str, 
        context: Optional[Any] = None, 
        options: Optional[List[str]] = None,
        timeout: Optional[float] = None
    ) -> str:
        timeout = timeout or self.default_timeout
        start_time = time.time()
        
        request_data = {
            "prompt": prompt, 
            "context": context, 
            "options": options,
            "timestamp": start_time
        }
        
        if os.path.exists(self.response_path):
            os.remove(self.response_path)
            
        with open(self.request_path, "w") as f:
            json.dump(request_data, f, indent=2)
            
        logger.debug(f"Polling {self.response_path} (timeout={timeout}s)...")
        
        try:
            while not os.path.exists(self.response_path):
                if time.time() - start_time > timeout:
                    raise AILibTimeoutError(f"AI Agent failed to respond within {timeout} seconds.")
                time.sleep(self.poll_interval)
                
            with open(self.response_path, "r") as f:
                content = f.read().strip()
                try:
                    response_data = json.loads(content)
                    if isinstance(response_data, dict):
                        return response_data.get("response", content)
                    return str(response_data)
                except json.JSONDecodeError:
                    return content
        finally:
            if os.path.exists(self.request_path):
                os.remove(self.request_path)
