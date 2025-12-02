DEV_MODE = True

import warnings

def color_format_warning(msg, category, filename, lineno, line=None):
    color = color_map.get(category, "\033[0m")
    return f"{color}{category.__name__}: {msg}{"\033[0m"}\n"

warnings.formatwarning = color_format_warning

class SevereWarning(Warning):
    pass

class InfoWarning(Warning):
    pass

class MismatchWarning(Warning):
    pass


color_map = {
    SevereWarning: "\033[91m",
    InfoWarning: "\033[93m",
    MismatchWarning: "\033[95m"
}

lib_avb = False

try:
    import neopixel as np
    import board as bd
    lib_avb = True
except ImportError:
    if DEV_MODE:
        warnings.warn("NeoPixels library or board library couldn't be imported — but dev mode is enabled", InfoWarning)

        # Fake NeoPixel class
        class FakeNeoPixelStrip(list):
            def __init__(self, pin, length):
                super().__init__([(0, 0, 0)] * length)
            def show(self):
                pass  # does nothing

        # Fake module to mimic 'neopixel'
        class FakeNeoPixelModule:
            NeoPixel = FakeNeoPixelStrip

        # Fake board pins
        class FakeBoard:
            D1 = "D1"
            D2 = "D2"
            D3 = "D3"

        np = FakeNeoPixelModule
        bd = FakeBoard
        lib_avb = True
    else:
        lib_avb = False
        warnings.warn("NeoPixels library or board library couldn't be imported — and dev mode is NOT enabled", SevereWarning)
mouth_pin = bd.D1
eye_pin = bd.D2
nose_pin = bd.D3

mouth_len = 3
eye_len = 3
nose_len = 3

#please update emotion looks when ready
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


def emotion_len_checker(prin=False):
    ok = True
    if prin:
        print("Running self check")
    for emotion, lisst in mouths.items():
        if len(lisst) != mouth_len:
            warnings.warn(f"Mouth emotion '{emotion}' has incorrect size: expected {mouth_len}, got {len(lisst)}", MismatchWarning)
            ok = False
    for emotion, lisst in eyes.items():
        if len(lisst) != eye_len:
            warnings.warn(f"Eye emotion '{emotion}' has incorrect size: expected {eye_len}, got {len(lisst)}", MismatchWarning)
            ok = False
    for emotion, lisst in noses.items():
        if len(lisst) != nose_len:
            warnings.warn(f"Nose emotion '{emotion}' has incorrect size: expected {nose_len}, got {len(lisst)}", MismatchWarning)
            ok = False
    if ok and prin:
        print("Self check passed with no errors")
    return ok


def load_class():
    class ProtogenFaceRenderer:
            def __init__(self):
                self.mouth=np.NeoPixel(mouth_pin, mouth_len)
                self.eye=np.NeoPixel(eye_pin, eye_len)
                self.nose=np.NeoPixel(nose_pin, nose_len)

            def _render(self, strip, mask, color):
                for i, active in enumerate(mask):
                    strip[i] = color if active else (0, 0, 0)
                strip.show()

            def render_mouth(self, Red, Green, Blue, Emotion='normal'):
                """Renders mouth LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'mouths' dictionary. (use list_mouth_emotions() to get a list of emotions)"""
                self._render(self.mouth, mouths[Emotion], (Red, Green, Blue))
            
            def render_eye(self, Red, Green, Blue, Emotion='normal'):
                """Renders eye LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'eyes' dictionary. (use list_eye_emotions() to get a list of emotions)"""
                self._render(self.eye, eyes[Emotion], (Red, Green, Blue))
            
            def render_nose(self, Red, Green, Blue, Emotion='normal'):
                """Renders nose LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the 'noses' dictionary. (use list_nose_emotions() to get a list of emotions)"""
                self._render(self.nose, noses[Emotion], (Red, Green, Blue))
            
            def render_face(self, Red, Green, Blue, Emotion='normal'):
                """Renders all LED's bassed on emotion mask

                    Args:
                    Red (int): Red channel (0-255)
                    Green (int): Green channel (0-255)
                    Blue (int): Blue channel (0-255)
                    Emotion (str): Emotion key from the dictionary's."""
                self._render(self.mouth, mouths[Emotion], (Red, Green, Blue))
                self._render(self.eye, eyes[Emotion], (Red, Green, Blue))
                self._render(self.nose, noses[Emotion], (Red, Green, Blue))
            
            def list_mouth_emotions(self):
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

if __name__ == '__main__':
    emotion_len_checker(True)
else:
    if lib_avb:
        ProtogenFaceRenderer = load_class()
    else:
        raise ImportError("ProtogenFaceRenderer not loaded because neopixel/board unavailable and dev mode is off.")