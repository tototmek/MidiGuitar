import yaml
import logger
import math

# based on current freq peaks and past information, it outputs note start and stop events. 
class NoteDetector:
    def __init__(self, config_path):
        self._data = self._load_config(config_path)
    
    def _load_config(self, path):

        # Read configuration from file
        logger.log_info("Loading configuration from " + path)
        with open(path, "r") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as e:
                logger.log_error("Error while parsing configuration file:\n"+str(e))
                exit(1)

        # Calculate other features based on the data
        if not "note_averaging_coefficient" in data:
            logger.log_error("Expected key 'note_averaging_coefficient' in config file")
            exit(1)
        if data["note_averaging_coefficient"] > 1:
            logger.log_warn("'note_averaging_coefficient' value should be between 0 and 1. Clamping.")
            data["note_averaging_coefficient"] = 1
        if data["note_averaging_coefficient"] < 0:
            logger.log_warn("'note_averaging_coefficient' value should be between 0 and 1. Clamping.")
            data["note_averaging_coefficient"] = 0
        data["1-note_averaging_coefficient"] = 1 - data["note_averaging_coefficient"]
        if "notes" not in data:
            logger.log_error("Expected key 'notes' in config file")
            exit(1)
        notes = data["notes"]

        # Set default values to missing fields, check if needed keys are present, add keys
        default_values = data.get("default", {})
        for note in notes:
            if not ('name' in note and 'frequency' in note):
                logger.log_error("Expected notes element to have keys 'name' and 'frequency'")
                exit(1)
            for key in default_values:
                if not key in note:
                    note[key] = default_values[key]
            note["on"] = False
            note["amplitude"] = 0
        
        # Find frequency ranges for each note
        middle_frequency = 0
        for i in range(len(notes)-1):
            notes[i]["min_frequency"] = middle_frequency
            middle_frequency = math.sqrt(notes[i]["frequency"] * notes[i+1]["frequency"])
        notes[-1]["min_frequency"] = middle_frequency
            
        if "name" in data:
            logger.log_ok("Loaded config: " + data["name"])
        else:
            logger.log_ok("Loaded unnamed config")
        return data
    
    def frequency_to_note(self, frequency):
        for note in reversed(self._data["notes"]):
            if frequency > note["min_frequency"]:
                return note
    
    def get_notes_from_peaks(self, peaks):
        result_notes = []
        peak_note_names = []
        i1 = self._data["note_averaging_coefficient"]
        i2 = self._data["1-note_averaging_coefficient"]

        # Set note aplitudes to peak amplitudes (with LP filtering applied)
        for frequency, amplitude in peaks:
            note = self.frequency_to_note(frequency)
            peak_note_names.append(note["name"])
            note["amplitude"] = i1 * amplitude  + i2 * note["amplitude"]
        
        for note in self._data["notes"]:
            # Set non-peak amplitudes to zero (with LP)
            if not note["name"] in peak_note_names:
                note["amplitude"] = i2 * note["amplitude"]
            
            # Check if note is triggered
            if note["on"]:
                if note["amplitude"] < note["off_threshold"]:
                    note["on"] = False
                    result_notes.append((note["name"], False))
            else:
                if note["amplitude"] > note["on_threshold"]:
                    note["on"] = True
                    result_notes.append((note["name"], True))

        return result_notes

if __name__=="__main__":
    note_detector = NoteDetector("/home/tototmek/Projects/MidiGuitar/config/notes.yaml")
    # Print loaded config
    for note in note_detector._data["notes"]:
        logger.log_info(note["name"] + ":")
        for key in note:
            if key == "name":
                continue
            logger.log_info("  " + str(key) + ": " + str(note[key]))
    
    # Test freq -> note conversion
    frequency = 89
    note = note_detector.frequency_to_note(frequency)
    logger.log_info(str(frequency) + " -> " + note["name"])
