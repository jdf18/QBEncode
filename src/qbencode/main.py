
from pygame import Vector2, Vector3, Color

from engine import Engine
from engine import cube
from engine.cube import Cube
from engine.ui import Responsive2D, UIButton, UIText, UITextbox
from engine.ui.rect import UIQuad

from hkociemba_twophase import face
from hkociemba_twophase.face import FaceCube
from qbencode import words
from qbencode import coding

COLOUR_BACKGROUND = Color("0x111111")
COLOUR_TEXT = Color("0xffffff")
COLOUR_UI_BG = Color("0x444444")

engine = Engine()
DIMS = (1280, 720)
engine.start(DIMS)

engine.camera.position = Vector3(0, 0, -10)
engine.camera.screen_dist = 100

# ===== CUBE UI =====

cube_obj = Cube()
engine.entities.append(cube_obj)

# ===== ENCODE UI ======

ENCODE_REL_POS = Vector2(0.5, 0.1)
DECODE_REL_POS = Vector2(0.5, 0.9)

BUTTON_RIGHT_ALIGN = Vector2(150, 0)
TEXTBOX_LEFT_ALIGN = Vector2(-300, 0)
TEXT_OFFSET = Vector2(15, 15)

BUTTON_SIZE = Responsive2D(Vector2(), Vector2(120, 50))
TEXTBOX_SIZE = Responsive2D(Vector2(), Vector2(400, 50))

encode_tb = UITextbox(
    Responsive2D(ENCODE_REL_POS, TEXTBOX_LEFT_ALIGN),
    TEXTBOX_SIZE,
    bg_colour=COLOUR_BACKGROUND,
    text_colour=COLOUR_TEXT,
)
engine.entities.append(encode_tb)

encode_button = UIButton(
    Responsive2D(ENCODE_REL_POS, BUTTON_RIGHT_ALIGN),
    BUTTON_SIZE,
    COLOUR_UI_BG,
)
def encode():
    user_text = encode_tb.text.text

    code = words.str_to_int(user_text)
    if code is None:
        print("Invalid code. Choose three words from the word list")
        return
    
    cubie = coding.decode(code)

    encode_scramble.text = ""
    encode_scramble.render()

    facecube = cubie.to_facelet_cube()
    cube_obj.facelets = facecube

encode_button.callback = encode
encode_tb.callback = encode
engine.entities.append(encode_button)

encode_text = UIText(
    Responsive2D(ENCODE_REL_POS, BUTTON_RIGHT_ALIGN + TEXT_OFFSET),
    BUTTON_SIZE,
    colour=COLOUR_TEXT,
    text="Encode",
)
engine.entities.append(encode_text)

size = 800
encode_scramble = UIText(
    Responsive2D(ENCODE_REL_POS, Vector2(int(round(-size/2)), 100)),
    Responsive2D(Vector2(), Vector2(size, 50)),
    COLOUR_TEXT,
    text="Encode scramble"
)
engine.entities.append(encode_scramble)

# ===== DECODE UI ======

decode_res_bg = UIQuad(
    Responsive2D(DECODE_REL_POS, TEXTBOX_LEFT_ALIGN),
    TEXTBOX_SIZE,
    Color("0x333333"),
)
engine.entities.append(decode_res_bg)

decode_result = UIText(
    Responsive2D(DECODE_REL_POS, TEXTBOX_LEFT_ALIGN + TEXT_OFFSET),
    TEXTBOX_SIZE,
    COLOUR_TEXT,
    text="decode result"
)
engine.entities.append(decode_result)

decode_button = UIButton(
    Responsive2D(DECODE_REL_POS, BUTTON_RIGHT_ALIGN),
    BUTTON_SIZE,
    COLOUR_UI_BG,
)
def decode():
    facecube: FaceCube = cube_obj.facelets
    cube = facecube.to_cubie_cube()

    verified = (cube.verify() == True)
    if not verified: return

    code = coding.encode(cube)
    decode_text.text = words.int_to_str(code)

decode_button.callback = decode
engine.entities.append(decode_button)

decode_text = UIText(
    Responsive2D(DECODE_REL_POS, BUTTON_RIGHT_ALIGN + TEXT_OFFSET),
    BUTTON_SIZE,
    colour=COLOUR_TEXT,
    text="Decode",
)
engine.entities.append(decode_text)
engine.run()
