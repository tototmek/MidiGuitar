#!/bin/bash
RED='\033[0;31m'
GREEN='\033[1;33m'
NC='\033[0m' # No Color


echo -e "${GREEN}Starting JACK server...${NC}"
echo -e "jack_control start"
jack_control start
echo -e "Opening GUI"
qjackctl & sleep 1
echo -e "${GREEN}Mapping PulseAudio to use JACK...${NC}"
echo -e "Loading modules..."
pactl load-module module-jack-source channels=2
pactl load-module module-jack-sink channels=2
echo -e "Setting default source and sink"
pactl set-default-source jack_in
pactl set-default-sink jack_out
echo -e "${GREEN}Mapping ALSA MIDI signals...${NC}"
sleep 1
a2j_control --start
echo -e "${GREEN}Ready to jam!${NC}"