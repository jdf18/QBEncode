
from pygame import Vector2, Vector3, Color

from engine import Engine
from engine.cube import Cube
from engine.ui import Responsive2D, UIButton, UIText, UITextbox

COLOUR_BACKGROUND = Color("0x111111")
COLOUR_TEXT = Color("0xffffff")
COLOUR_UI_BG = Color("0x444444")

engine = Engine()
DIMS = (1280, 720)
engine.start(DIMS)

engine.camera.position = Vector3(0, 0, -10)
engine.camera.screen_dist = 100

# ===== CUBE UI =====

engine.entities.append(Cube())

# ===== ENCODE UI ======

encode_tb = UITextbox(
    Responsive2D(Vector2(0.5, 0.1), Vector2(-100, 0)),
    Responsive2D(Vector2(), Vector2(200, 50)), 
    bg_colour=COLOUR_BACKGROUND,
    text_colour=COLOUR_TEXT,
)
engine.entities.append(encode_tb)

encode_button = UIButton(
    Responsive2D(Vector2(0.5, 0.1), Vector2(100, 0)),
    Responsive2D(Vector2(), Vector2(200, 50)),
    COLOUR_UI_BG,
)
def encode():
    print("TODO Encode")
encode_button.callback = encode
encode_tb.callback = encode
engine.entities.append(encode_button)

encode_text = UIText(
    Responsive2D(Vector2(0.5, 0.1), Vector2(115, 15)),
    Responsive2D(Vector2(), Vector2()),
    colour=COLOUR_TEXT,
    text="Encode",
)
engine.entities.append(encode_text)

# ===== DECODE UI ======

decode_result = UIText(
    Responsive2D(Vector2(0.5, 0.9), Vector2(-85, 15)),
    Responsive2D(Vector2(), Vector2(200, 50)),
    COLOUR_TEXT,
    text="decode result"
)
engine.entities.append(decode_result)

decode_button = UIButton(
    Responsive2D(Vector2(0.5, 0.9), Vector2(100, 0)),
    Responsive2D(Vector2(), Vector2(200, 50)),
    COLOUR_UI_BG,
)
def decode():
    print("TODO Decode")
decode_button.callback = decode
engine.entities.append(decode_button)

decode_text = UIText(
    Responsive2D(Vector2(0.5, 0.9), Vector2(115, 15)),
    Responsive2D(Vector2(), Vector2()),
    colour=COLOUR_TEXT,
    text="Decode",
)
engine.entities.append(decode_text)
engine.run()
