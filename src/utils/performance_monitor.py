"""
Performance Monitor for Pet Assistant
Tracks memory usage, CPU performance, and optimization opportunities
"""

import time
import psutil
import gc
import threading
from typing import Dict, List, Optional
import logging

class PerformanceMonitor:
    """Monitor and optimize pet assistant performance"""
    
    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        
        # Performance metrics
        self.metrics = {
            "memory_usage": [],
            "cpu_usage": [],
            "frame_times": [],
            "ai_response_times": [],
            "slow_operations": []
        }
        
        # Performance thresholds
        self.thresholds = {
            "memory_warning": 200 * 1024 * 1024,  # 200MB
            "cpu_warning": 15.0,                   # 15% CPU
            "frame_time_warning": 0.1,             # 100ms per frame
            "ai_response_warning": 10.0            # 10 second AI responses
        }
        
        # Monitoring flags
        self.monitoring_active = False
        self.monitor_thread = None
        
    def start_monitoring(self):
        """Start performance monitoring"""
        if self.monitoring_active:
            return
            
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop_monitoring(self):
        """Stop performance monitoring"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2)
        self.logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Check memory usage
                memory_mb = self._get_memory_usage()
                self.metrics["memory_usage"].append({
                    "timestamp": time.time(),
                    "value": memory_mb
                })
                
                # Check CPU usage
                cpu_percent = psutil.cpu_percent(interval=1)
                self.metrics["cpu_usage"].append({
                    "timestamp": time.time(),
                    "value": cpu_percent
                })
                
                # Warn if thresholds exceeded
                if memory_mb > self.thresholds["memory_warning"] / (1024*1024):
                    self.logger.warning(f"High memory usage: {memory_mb:.1f}MB")
                
                if cpu_percent > self.thresholds["cpu_warning"]:
                    self.logger.warning(f"High CPU usage: {cpu_percent:.1f}%")
                
                # Clean old metrics (keep last 100 entries)
                for metric_name in self.metrics:
                    if len(self.metrics[metric_name]) > 100:
                        self.metrics[metric_name] = self.metrics[metric_name][-100:]
                
                time.sleep(5)  # Monitor every 5 seconds
                
            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
                time.sleep(5)
    
    def _get_memory_usage(self) -> float:
        """Get current memory usage in MB"""
        try:
            process = psutil.Process()
            memory_info = process.memory_info()
            return memory_info.rss / (1024 * 1024)  # Convert to MB
        except:
            return 0.0
    
    def log_frame_time(self, frame_time: float):
        """Log UI frame rendering time"""
        self.metrics["frame_times"].append({
            "timestamp": time.time(),
            "value": frame_time
        })
        
        if frame_time > self.thresholds["frame_time_warning"]:
            self.logger.warning(f"Slow frame render: {frame_time:.3f}s")
    
    def log_ai_response_time(self, response_time: float):
        """Log AI response time"""
        self.metrics["ai_response_times"].append({
            "timestamp": time.time(),
            "value": response_time
        })
        
        if response_time > self.thresholds["ai_response_warning"]:
            self.logger.warning(f"Slow AI response: {response_time:.1f}s")
    
    def log_slow_operation(self, operation_name: str, duration: float):
        """Log operations that are slower than expected"""
        self.metrics["slow_operations"].append({
            "timestamp": time.time(),
            "operation": operation_name,
            "duration": duration
        })
        
        if self.config.get("log_slow_operations", True):
            self.logger.warning(f"Slow operation [{operation_name}]: {duration:.3f}s")
    
    def force_garbage_collection(self):
        """Force Python garbage collection"""
        try:
            before_count = len(gc.get_objects())
            collected = gc.collect()
            after_count = len(gc.get_objects())
            
            if collected > 0:
                self.logger.info(f"Garbage collection: freed {collected} objects, "
                               f"objects: {before_count} -> {after_count}")
        except Exception as e:
            self.logger.error(f"Error in garbage collection: {e}")
    
    def get_performance_report(self) -> Dict:
        """Generate performance report"""
        current_memory = self._get_memory_usage()
        
        # Calculate averages for recent metrics
        recent_cpu = [m["value"] for m in self.metrics["cpu_usage"][-20:]]
        recent_frames = [m["value"] for m in self.metrics["frame_times"][-50:]]
        recent_ai = [m["value"] for m in self.metrics["ai_response_times"][-10:]]
        
        report = {
            "current_memory_mb": current_memory,
            "avg_cpu_percent": sum(recent_cpu) / len(recent_cpu) if recent_cpu else 0,
            "avg_frame_time": sum(recent_frames) / len(recent_frames) if recent_frames else 0,
            "avg_ai_response_time": sum(recent_ai) / len(recent_ai) if recent_ai else 0,
            "slow_operations_count": len(self.metrics["slow_operations"]),
            "recommendations": self._generate_recommendations()
        }
        
        return report
    
    def _generate_recommendations(self) -> List[str]:
        """Generate performance improvement recommendations"""
        recommendations = []
        current_memory = self._get_memory_usage()
        
        # Memory recommendations
        if current_memory > 150:  # Over 150MB
            recommendations.append("High memory usage detected. Consider reducing conversation history limit.")
        
        # CPU recommendations  
        recent_cpu = [m["value"] for m in self.metrics["cpu_usage"][-10:]]
        if recent_cpu and sum(recent_cpu) / len(recent_cpu) > 10:
            recommendations.append("High CPU usage. Consider reducing screen capture frequency.")
        
        # Frame rate recommendations
        recent_frames = [m["value"] for m in self.metrics["frame_times"][-20:]]
        if recent_frames and sum(recent_frames) / len(recent_frames) > 0.05:
            recommendations.append("Slow UI rendering. Consider reducing UI update frequency.")
        
        # AI response recommendations
        recent_ai = [m["value"] for m in self.metrics["ai_response_times"][-5:]]
        if recent_ai and sum(recent_ai) / len(recent_ai) > 8:
            recommendations.append("Slow AI responses. Check API connection and reduce context size.")
        
        if not recommendations:
            recommendations.append("Performance is optimal!")
        
        return recommendations
    
    def optimize_memory(self, max_conversation_history: int = 30, max_activity_history: int = 15):
        """Optimize memory usage by cleaning up data structures"""
        try:
            # This would be called by the pet manager to clean up its data
            self.force_garbage_collection()
            self.logger.info("Memory optimization completed")
            
        except Exception as e:
            self.logger.error(f"Error in memory optimization: {e}")

# Performance decorator for timing operations
def measure_performance(monitor: Optional[PerformanceMonitor] = None, operation_name: str = ""):
    """Decorator to measure and log operation performance"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            
            duration = end_time - start_time
            
            if monitor and duration > 1.0:  # Log operations taking >1 second
                monitor.log_slow_operation(operation_name or func.__name__, duration)
            
            return result
        return wrapper
    return decorator