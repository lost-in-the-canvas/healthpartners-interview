import os
from functools import wraps
from pyinstrument import Profiler
import pyinstrument

def profile_function(output_dir="./performance_profiles"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with Profiler() as profiler:
                result = func(*args, **kwargs)

            # Ensure the output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Generate filenames
            base_filename = f"profiler_output_{func.__name__}"
            speedscope_filename = os.path.join(output_dir, f"{base_filename}.speedscope.json")
            html_filename = os.path.join(output_dir, f"{base_filename}.html")

            # Write Speedscope output
            with open(speedscope_filename, "w") as f:
                f.write(profiler.output(pyinstrument.renderers.SpeedscopeRenderer(
                    show_all=True, timeline=True, processor_options={'show_native': True}
                )))

            # Write HTML output
            with open(html_filename, "w") as f:
                f.write(profiler.output_html())

            return result
        return wrapper
    return decorator
