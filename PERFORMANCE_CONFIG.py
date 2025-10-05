# 🚀 Pet Performance Optimization Settings

# Optimal settings for best performance vs functionality balance
PERFORMANCE_CONFIG = {
    # UI Performance
    "ui_frame_rate": 30,           # FPS for UI updates (30 is smooth, 60 is excessive)
    "ui_update_interval": 0.033,   # 1/30 seconds per frame
    
    # Screen Monitoring
    "screen_capture_interval": 5.0,  # Screenshot every 5 seconds (vs 2 seconds)
    "screen_resize_threshold": 0.8,  # Resize screenshots to 80% for memory
    
    # Memory Management  
    "max_conversation_history": 50,  # Limit chat history
    "max_activity_history": 20,      # Limit activity tracking
    "max_screenshot_cache": 5,       # Keep only 5 recent screenshots
    
    # AI/API Optimization
    "ai_response_timeout": 15,       # 15 second timeout for AI responses
    "ai_context_limit": 1000,        # Limit AI context tokens
    "rate_limit_calls": 10,          # Max 10 AI calls per minute
    
    # Background Tasks
    "spontaneous_check_interval": 60,  # Check every 60 seconds (vs 30)
    "idle_sleep_multiplier": 2,        # Sleep 2x longer when user idle
    "voice_processing_timeout": 10,     # Voice processing timeout
    
    # Resource Cleanup
    "temp_file_cleanup_interval": 300,  # Clean temp files every 5 minutes
    "memory_cleanup_threshold": 0.8,    # Clean memory at 80% usage
    "gc_collection_interval": 120,      # Force garbage collection every 2 minutes
}

# Theme-specific optimizations
THEME_PERFORMANCE = {
    "cardboard": {
        "animation_steps": 8,      # Reduced animation steps for cardboard theme
        "wobble_duration": 200,    # Shorter wobble animations
        "texture_quality": "low",  # Lower quality textures
    },
    "modern": {
        "animation_steps": 12,     # Smooth animations for modern theme
        "fade_duration": 150,      # Quick fades
        "blur_quality": "medium",  # Balanced blur effects
    }
}

# Memory usage targets
MEMORY_TARGETS = {
    "conversation_history": "2 MB",    # Target memory for chat history
    "activity_tracking": "1 MB",       # Target memory for activity data
    "screenshot_cache": "10 MB",       # Target memory for screenshots
    "ui_elements": "5 MB",             # Target memory for UI components
}

# Performance monitoring flags
PERFORMANCE_MONITORING = {
    "enable_profiling": False,         # Enable detailed performance profiling
    "log_slow_operations": True,       # Log operations taking >1 second
    "memory_usage_warnings": True,     # Warn when memory usage is high
    "fps_monitoring": False,           # Monitor actual UI frame rate
}