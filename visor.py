#!/usr/bin/env python3
#So i put all of these up here for easy accses but i cant do the pins becouse we need to first import the other librarys so here we are

mouth_len = 3
eye_len = 3
nose_len = 3

#Should make these like actully work or something idk, gotta make hardware first. imagen the number represent an LED string (its like 12 at night cut me some slack)
mouths = {
     'normal': [1, 0, 0],
     'happy': [0, 1, 0],
     'angry': [1, 1, 0],
     'sad': [0, 0, 1],
     'worried': [1, 0, 1],
     'shocked': [0, 1, 1],
     'xxx': [1, 1, 1]
     }

eyes= {
     'normal': [1, 0, 0],
     'happy': [0, 1, 0],
     'angry': [1, 1, 0],
     'sad': [0, 0, 1],
     'worried': [1, 0, 1],
     'shocked': [0, 1, 1],
     'xxx': [1, 1, 1]
     }

noses= {
     'normal': [1, 0, 0],
     'happy': [0, 1, 0],
     'angry': [1, 1, 0],
     'sad': [0, 0, 1],
     'worried': [1, 0, 1],
     'shocked': [0, 1, 1],
     'xxx': [1, 1, 1]
     }

import warnings
from pi5neo import Pi5Neo

eye_starting_led = 0
mouth_starting_led = eye_starting_led + eye_len
nose_starting_led = mouth_starting_led + mouth_len



def emotion_len_checker(prin=False): #checks to ensure the emotions are the correct length for there led string
    ok = True
    if prin:
        print("Running self check")
    for emotion, lisst in mouths.items():
        if len(lisst) != mouth_len:
            warnings.warn(f"\033[95m Mouth emotion '{emotion}' has incorrect size: expected {mouth_len}, got {len(lisst)} \033[0m")
            ok = False
    for emotion, lisst in eyes.items():
        if len(lisst) != eye_len:
            warnings.warn(f"\033[95m Eye emotion '{emotion}' has incorrect size: expected {eye_len}, got {len(lisst)} \033[0m")
            ok = False
    for emotion, lisst in noses.items():
        if len(lisst) != nose_len:
            warnings.warn(f"\033[95m Nose emotion '{emotion}' has incorrect size: expected {nose_len}, got {len(lisst)} \033[0m")
            ok = False
    if ok and prin:
        print("Self check passed with no errors")
    return ok


def load_class():
    class ProtogenFaceRenderer:
            def __init__(self):
                self.neo = Pi5Neo('/dev/spidev0.0', (eye_len + mouth_len + nose_len), 800)

            def _render(self, starting_led, mask, color): #loops over the LED's checks if the should be lit and if so sets them to the provided color
                for i, active in enumerate(mask):
                    self.neo.set_led_color((i + starting_led),
                                            color[0] if active else 0,
                                            color[1] if active else 0,
                                            color[2] if active else 0)
                self.neo.update_strip()

            def render_mouth(self, Red, Green, Blue, Emotion='normal'):
                """Renders mouth LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'mouths' dictionary. (use list_mouth_emotions() to get a list of emotions)"""
                self._render(mouth_starting_led, mouths[Emotion], (Red, Green, Blue))
            
            def render_eye(self, Red, Green, Blue, Emotion='normal'):
                """Renders eye LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'eyes' dictionary. (use list_eye_emotions() to get a list of emotions)"""
                self._render(eye_starting_led, eyes[Emotion], (Red, Green, Blue))
            
            def render_nose(self, Red, Green, Blue, Emotion='normal'):
                """Renders nose LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'noses' dictionary. (use list_nose_emotions() to get a list of emotions)"""
                self._render(nose_starting_led, noses[Emotion], (Red, Green, Blue))
            
            def render_face(self, Red, Green, Blue, Emotion='normal'):
                """Renders all LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the dictionary's."""
                self._render(mouth_starting_led, mouths[Emotion], (Red, Green, Blue))
                self._render(eye_starting_led, eyes[Emotion], (Red, Green, Blue))
                self._render(nose_starting_led, noses[Emotion], (Red, Green, Blue))
            
            def list_mouth_emotions(self): #lists the emotions
                """Returns list of mouth emotions"""
                return list(mouths.keys())
            
            def list_eye_emotions(self):
                """Returns list of eye emotions"""
                return list(eyes.keys())
            
            def list_nose_emotions(self):
                """Returns list of nose emotions"""
                return list(noses.keys())
            
            def self_check(self):
                """Returns True if emotions are correct length"""
                return emotion_len_checker()
                
    return ProtogenFaceRenderer

if __name__ == '__main__': #if its imported it just acts like a library, but if its run it dose self checks yay
    emotion_len_checker(True)
else:
    ProtogenFaceRenderer = load_class()
