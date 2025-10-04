#!/usr/bin/env python3
"""
Virtual Pet AI Assistant
Main application entry point
"""

import sys
import os

# Suppress Google/gRPC warnings BEFORE any other imports
os.environ['GRPC_VERBOSITY'] = 'ERROR'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import asyncio
import logging
from pathlib import Path
import warnings

# Suppress specific warnings
warnings.filterwarnings('ignore', category=UserWarning, module='google')
warnings.filterwarnings('ignore', message='.*ALTS.*')

# Suppress absl logging before it initializes (if available)
try:
    import absl.logging
    absl.logging.set_verbosity(absl.logging.ERROR)
    absl.logging.set_stderrthreshold(absl.logging.ERROR)
except ImportError:
    pass

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.pet.pet_manager import PetManager
from src.ai.gemini_client import GeminiClient
from src.screen.screen_monitor import ScreenMonitor
from src.utils.config_manager import ConfigManager
from src.utils.logger import setup_logging

def main():
    """Main application entry point"""
    try:
        # Setup logging
        setup_logging()
        logger = logging.getLogger(__name__)
        logger.info("Starting Virtual Pet AI Assistant...")

        # Load configuration
        config_manager = ConfigManager()
        config = config_manager.load_config()
        
        # Initialize components
        gemini_client = GeminiClient()
        screen_monitor = ScreenMonitor()
        
        # Create and start the pet manager
        pet_manager = PetManager(
            gemini_client=gemini_client,
            screen_monitor=screen_monitor,
            config=config
        )
        
        # Start the application
        asyncio.run(pet_manager.run())
        
    except KeyboardInterrupt:
        logger.info("Application interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())