from pyinstrument import Profiler

profile = Profiler()
if not profile.is_running:
    profile.start()

from main import main
main()

profile.stop()
print(profile.output_text())