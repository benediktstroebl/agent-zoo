import logging
import logging.handlers
import os
from pathlib import Path

def setup_logging(log_dir: str = "logs"):
    Path(log_dir).mkdir(exist_ok=True)
    
    # Main logger
    main_logger = logging.getLogger('agent_zoo')
    main_logger.setLevel(logging.INFO)
    
    # File handler for all logs
    main_handler = logging.handlers.RotatingFileHandler(
        os.path.join(log_dir, 'agent_zoo.log'),
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    
    # Formatters
    main_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    container_formatter = logging.Formatter('%(asctime)s - %(message)s')
    
    main_handler.setFormatter(main_formatter)
    console_handler.setFormatter(main_formatter)
    
    main_logger.addHandler(main_handler)
    main_logger.addHandler(console_handler)
    
    def get_container_handler(container_name):
        container_logger = logging.getLogger(f'agent_zoo.containers.{container_name}')
        container_logger.setLevel(logging.INFO)
        container_logger.propagate = False
        
        file_handler = logging.handlers.RotatingFileHandler(
            os.path.join(log_dir, f'{container_name}.log'),
            maxBytes=10*1024*1024,
            backupCount=5
        )
        container_console_handler = logging.StreamHandler()
        
        file_handler.setFormatter(container_formatter)
        container_console_handler.setFormatter(container_formatter)
        
        container_logger.addHandler(file_handler)
        container_logger.addHandler(container_console_handler)
        return container_logger
    
    return main_logger, get_container_handler 