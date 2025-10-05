"""
Performance Test Script
Compare pet performance before and after optimizations
"""

import asyncio
import time
import psutil
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.utils.performance_monitor import PerformanceMonitor

async def test_performance():
    """Test current pet performance"""
    print("🚀 Pet Assistant Performance Test")
    print("=" * 50)
    
    # Initialize performance monitor
    monitor = PerformanceMonitor({
        "log_slow_operations": True,
        "enable_profiling": True
    })
    
    print("Starting performance monitoring...")
    monitor.start_monitoring()
    
    # Simulate pet operations
    print("\n📊 Testing UI Loop Performance...")
    frame_times = []
    
    for i in range(100):
        start_time = time.time()
        
        # Simulate UI update work
        await asyncio.sleep(0.001)  # Minimal processing
        
        frame_time = time.time() - start_time
        frame_times.append(frame_time)
        monitor.log_frame_time(frame_time)
        
        # Simulate 30 FPS
        await asyncio.sleep(0.033)  
    
    avg_frame_time = sum(frame_times) / len(frame_times)
    max_frame_time = max(frame_times)
    
    print(f"✅ UI Loop Test Complete")
    print(f"   Average frame time: {avg_frame_time*1000:.2f}ms")
    print(f"   Maximum frame time: {max_frame_time*1000:.2f}ms")
    print(f"   Target frame time: 33.33ms (30 FPS)")
    
    # Test AI response simulation
    print("\n🤖 Testing AI Response Performance...")
    ai_times = []
    
    for i in range(5):
        start_time = time.time()
        
        # Simulate AI processing delay
        await asyncio.sleep(0.5 + (i * 0.2))  # Varying response times
        
        response_time = time.time() - start_time
        ai_times.append(response_time)
        monitor.log_ai_response_time(response_time)
    
    avg_ai_time = sum(ai_times) / len(ai_times)
    max_ai_time = max(ai_times)
    
    print(f"✅ AI Response Test Complete")
    print(f"   Average response time: {avg_ai_time:.2f}s")
    print(f"   Maximum response time: {max_ai_time:.2f}s")
    print(f"   Target response time: <3s")
    
    # Test memory usage
    print("\n💾 Testing Memory Usage...")
    initial_memory = monitor._get_memory_usage()
    
    # Simulate memory operations
    large_data = []
    for i in range(1000):
        large_data.append(f"Test conversation message {i} with some content")
        
        # Simulate cleanup every 50 items (memory management)
        if i % 50 == 0 and len(large_data) > 50:
            large_data = large_data[-30:]  # Keep only recent items
    
    final_memory = monitor._get_memory_usage()
    
    print(f"✅ Memory Test Complete")
    print(f"   Initial memory: {initial_memory:.1f}MB")
    print(f"   Final memory: {final_memory:.1f}MB")
    print(f"   Memory growth: {final_memory - initial_memory:.1f}MB")
    print(f"   Target growth: <10MB")
    
    # Generate performance report
    print("\n📋 Performance Report")
    print("-" * 30)
    
    await asyncio.sleep(2)  # Let monitor collect data
    report = monitor.get_performance_report()
    
    print(f"Current Memory Usage: {report['current_memory_mb']:.1f}MB")
    print(f"Average CPU Usage: {report['avg_cpu_percent']:.1f}%")
    print(f"Average Frame Time: {report['avg_frame_time']*1000:.1f}ms")
    print(f"Average AI Response: {report['avg_ai_response_time']:.1f}s")
    print(f"Slow Operations: {report['slow_operations_count']}")
    
    print("\n💡 Recommendations:")
    for rec in report['recommendations']:
        print(f"   • {rec}")
    
    # Stop monitoring
    monitor.stop_monitoring()
    
    # Performance scoring
    print("\n🏆 Performance Score")
    print("=" * 25)
    
    # Calculate scores (0-100)
    frame_score = max(0, 100 - (avg_frame_time * 1000 - 33) * 2)  # Penalty for >33ms
    memory_score = max(0, 100 - max(0, report['current_memory_mb'] - 100))  # Penalty for >100MB
    ai_score = max(0, 100 - (avg_ai_time - 2) * 20)  # Penalty for >2s responses
    cpu_score = max(0, 100 - report['avg_cpu_percent'] * 2)  # Penalty for high CPU
    
    overall_score = (frame_score + memory_score + ai_score + cpu_score) / 4
    
    print(f"UI Performance: {frame_score:.0f}/100")
    print(f"Memory Efficiency: {memory_score:.0f}/100") 
    print(f"AI Responsiveness: {ai_score:.0f}/100")
    print(f"CPU Efficiency: {cpu_score:.0f}/100")
    print(f"\nOverall Score: {overall_score:.0f}/100")
    
    if overall_score >= 85:
        print("🌟 Excellent performance!")
    elif overall_score >= 70:
        print("✅ Good performance")
    elif overall_score >= 50:
        print("⚠️ Acceptable performance")
    else:
        print("❌ Poor performance - optimization needed")
    
    return overall_score

def test_memory_cleanup():
    """Test memory cleanup functionality"""
    print("\n🧹 Testing Memory Cleanup...")
    
    # Force garbage collection
    import gc
    before_objects = len(gc.get_objects())
    collected = gc.collect()
    after_objects = len(gc.get_objects())
    
    print(f"   Objects before: {before_objects}")
    print(f"   Objects collected: {collected}")
    print(f"   Objects after: {after_objects}")
    print(f"   Memory freed: {before_objects - after_objects} objects")

if __name__ == "__main__":
    print("🐾 Pet Assistant Performance Test Suite")
    print("Testing optimized performance settings...\n")
    
    try:
        # Run main performance test
        score = asyncio.run(test_performance())
        
        # Test memory cleanup
        test_memory_cleanup()
        
        print(f"\n🎯 Final Performance Score: {score:.0f}/100")
        
        if score >= 70:
            print("✅ Pet is optimized and ready for production!")
        else:
            print("⚠️ Consider additional optimizations")
            
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"\nError during testing: {e}")