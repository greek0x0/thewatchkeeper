import sys
import colorama
from watchkeeper.watchkeeper import watch
if __name__ == "__main__":
    colorama.init()
    if len(sys.argv) < 3:
        print("Please specify data path folder and opml filename as arguments")
        print("usage: python3 run.py feeds subscriptions.xml")
        exit(1)
    reader = watch(data_path=sys.argv[1], opml_filename=sys.argv[2])
    reader.run()
