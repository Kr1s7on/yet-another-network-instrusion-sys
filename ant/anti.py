import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pylnk3

class StartupProgramsHandler(FileSystemEventHandler):
    """Handles file creation/modification events by searching for a pattern."""
    def on_modified(self, event):
        """Search for the pattern in the newly created file."""
        time.sleep(1)
        # logic here

        # use watchdog src_path to determine the path of this new file
        src_path = event.src_path

        # use os.path.splitext to obtain the extension (use print to determine what the output is!)
        file, ext = os.path.splitext(src_path)

        # if file != '.lnk' return
        if ext.lower() != '.lnk':
            return

        # use pylnk3 to parse the filepath
        try:
            lnk = pylnk3.parse(src_path)
            thetarget = lnk.path
            print(f"new s prog detected: {thetarget}")
        except Exception as e:
            print(f"error mb: {e}")

def main():
     # Create an instance of your custom event handler class (which handles .lnk file changes)
    event_handler = StartupProgramsHandler()

    # Create a Watchdog observer that will monitor file system events
    observer = Observer()

    # Replace environment variables in a string with the actual value https://www.geeksforgeeks.org/python/python-os-path-expandvars-method/
    startup_path = os.path.expandvars(r"C:\Users\%username%\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup")

    # Tell the observer to watch the startup folder using your handler, non-recursively (only top-level)
    observer.schedule(event_handler, startup_path, recursive=True)
    observer.start()
    print(f"Monitoring new startup programs...")
    observer.join()

if '__main__' == __name__:
    main()