import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent

class RealTimeProcessHandler(PatternMatchingEventHandler):

    patterns = ["*.xml"]
    counter = 1;

    def on_modified(self, event):
        if type(event) == FileModifiedEvent:
            if self.counter == 1:
                print(f"Counter: [{self.counter}] [File is Flushed, IF Read is Performed NO Data can be Read], [Process: Don't Read the File]")
                self.counter = self.counter + 1;
            elif self.counter == 2:
                print(f"Counter: [{self.counter}] [File is Closed, Perform Read Data can be Read Now], [Process: Read the File]")
                
                with open(event.src_path, 'r') as xml_source:
                    xml_string = xml_source.read()

                print(f"Counter: [{self.counter}] [File Content: Process XML CONFIG]: \n ${xml_string}")
                
                """ Code your Processing Here : do_something() """
                self.counter = 1 # Set Counter Back to 1

if __name__ == '__main__':
    
    observer = Observer()
    observer.schedule(RealTimeProcessHandler(), path='.')
    observer.start()
    
    # Intentionally written indicating the program is doing something, It is important for this code to run individually but not for the snippet
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()