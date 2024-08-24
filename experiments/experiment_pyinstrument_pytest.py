import time
import pytest
from pyinstrument import Profiler
from pyinstrument.renderers import SpeedscopeRenderer

def slow_function():
    """A function with deliberate delays to demonstrate profiling."""
    print("Starting slow function...")
    time.sleep(1)  # Simulate some work

    for i in range(3):
        print(f"Iteration {i+1}")
        time.sleep(0.5)  # More simulated work

    print("Slow function completed.")
    return True

def test_slow_function():
    """Test case for slow_function using pytest and pyinstrument."""
    profiler = Profiler()
    profiler.start()

    # Run the function we want to test and performance_profiles
    result = slow_function()

    profiler.stop()

    # Print console transformed
    print("\nProfiling Results (Console Output):")
    print(profiler.output_text(unicode=True, color=True))

    # Save results in Speedscope format
    with open('test_profile.speedscope.json', 'w') as f:
        f.write(profiler.output(renderer=SpeedscopeRenderer()))
    print("\nSpeedscope JSON saved to 'test_profile.speedscope.json'")

    # Assert the result of the function
    assert result == True

if __name__ == "__main__":
    pytest.main([__file__])
