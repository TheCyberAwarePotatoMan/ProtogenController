#!/usr/bin/env python3

mouth_len = 3
eye_len = 3
nose_len = 3

# Need to add more emotions and make them better later
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
     'blink' : [0, 0, 0],
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

def emotion_len_checker(verbose=False): #checks if all emotions are correct length
    ok = True
    if verbose:
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
    if ok and verbose:
        print("Self check passed with no errors")
    return ok


def load_class():
    class ProtogenFaceRenderer:
            def __init__(self):
                try:
                    self.neo = Pi5Neo('/dev/spidev0.0', (eye_len + mouth_len + nose_len), 800)
                except Exception as e:
                    raise RuntimeError(f"Failed to initialize Pi5Neo: {e}") from e

            def _validate_color(self, color):
                """Validates RGB color values are in 0-255 range"""
                if not isinstance(color, (tuple, list)) or len(color) != 3:
                    raise ValueError("Color must be a tuple/list of 3 values (R, G, B)")
                for i, value in enumerate(color):
                    if not isinstance(value, int) or not (0 <= value <= 255):
                        raise ValueError(f"Color channel {['R', 'G', 'B'][i]} must be int 0-255, got {value}")
            
            def _validate_emotion(self, emotion, emotion_dict, emotion_name):
                """Validates emotion exists in the given emotion dictionary"""
                if emotion not in emotion_dict:
                    valid = list(emotion_dict.keys())
                    raise ValueError(f"Invalid {emotion_name} emotion '{emotion}'. Valid options: {valid}")

            def _render(self, starting_led, mask, color): #internal render function
                self._validate_color(color)
                for i, active in enumerate(mask):
                    self.neo.set_led_color((i + starting_led),
                                            color[0] if active else 0,
                                            color[1] if active else 0,
                                            color[2] if active else 0)
                self.neo.update_strip()

            def render_mouth(self, red, green, blue, emotion='normal'):
                """Renders mouth LED's based on emotion mask

                    Args:
                    red (int): Red channel (0-255)
                    green (int): Green channel (0-255)
                    blue (int): Blue channel (0-255)
                    emotion (str): Emotion key from the 'mouths' dictionary. (use list_mouth_emotions() to get a list of emotions)
                    
                    Raises:
                    ValueError: If emotion is invalid or color values out of range"""
                self._validate_emotion(emotion, mouths, 'mouth')
                self._render(mouth_starting_led, mouths[emotion], (red, green, blue))
            
            def render_eye(self, red, green, blue, emotion='normal'):
                """Renders eye LED's based on emotion mask

                    Args:
                    red (int): Red channel (0-255)
                    green (int): Green channel (0-255)
                    blue (int): Blue channel (0-255)
                    emotion (str): Emotion key from the 'eyes' dictionary. (use list_eye_emotions() to get a list of emotions)
                    
                    Raises:
                    ValueError: If emotion is invalid or color values out of range"""
                self._validate_emotion(emotion, eyes, 'eye')
                self._render(eye_starting_led, eyes[emotion], (red, green, blue))
            
            def render_nose(self, red, green, blue, emotion='normal'):
                """Renders nose LED's based on emotion mask

                    Args:
                    red (int): Red channel (0-255)
                    green (int): Green channel (0-255)
                    blue (int): Blue channel (0-255)
                    emotion (str): Emotion key from the 'noses' dictionary. (use list_nose_emotions() to get a list of emotions)
                    
                    Raises:
                    ValueError: If emotion is invalid or color values out of range"""
                self._validate_emotion(emotion, noses, 'nose')
                self._render(nose_starting_led, noses[emotion], (red, green, blue))
            
            def render_face(self, red, green, blue, emotion='normal'):
                """Renders all LED's based on emotion mask

                    Args:
                    red (int): Red channel (0-255)
                    green (int): Green channel (0-255)
                    blue (int): Blue channel (0-255)
                    emotion (str): Emotion key from the dictionaries.
                    
                    Raises:
                    ValueError: If emotion is invalid or color values out of range"""
                self._validate_emotion(emotion, mouths, 'mouth')
                self._validate_emotion(emotion, eyes, 'eye')
                self._validate_emotion(emotion, noses, 'nose')
                self._render(mouth_starting_led, mouths[emotion], (red, green, blue))
                self._render(eye_starting_led, eyes[emotion], (red, green, blue))
                self._render(nose_starting_led, noses[emotion], (red, green, blue))
            
            def list_mouth_emotions(self): #lists available emotions
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

if __name__ == '__main__': #self test if run directly
    emotion_len_checker(True)
else:
    ProtogenFaceRenderer = load_class()
