import time
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

def main():
    # Create a Profiler instance
    profiler = Profiler()

    # Start profiling
    profiler.start()

    # Run the code we want to performance_profiles
    slow_function()

    # Stop profiling
    profiler.stop()

    # Print a simple console transformed
    print("\nProfiling Results (Console Output):")
    print(profiler.output_text(unicode=True, color=True))

    # Save results in Speedscope format
    with open('performance_profiles.speedscope.json', 'w') as f:
        f.write(profiler.output(renderer=SpeedscopeRenderer()))
    print("\nSpeedscope JSON saved to 'performance_profiles.speedscope.json'")

if __name__ == "__main__":
    main()
