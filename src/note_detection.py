import yaml

# based on current freq peaks and past information, it outputs note start and stop events. 
class NoteDetector:
    def __init__(self, config_path):
        self._notes = self._load_config(config_path)
    
    def _load_config(self, path):
        with open(path, "r") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                print("Error while loading configuration file:", e)
        return data
                
if __name__=="__main__":
    print(*NoteDetector("/home/tototmek/Projects/MidiGuitar/config/notes.yaml")._notes["notes"], sep="\n")