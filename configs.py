from dataclasses import dataclass
from colorutils import Color


@dataclass
class Margin:
    top: int
    right: int
    bottom: int
    left: int


@dataclass
class CFG1:
    text = ""
    name_text = None
    option_text = []
    W = 1920
    H = 1080
    bg_path = "./bgimages/generated_bg-20230408T030427Z-001/generated_bg/0001.png"
    fg_pathlist = ["./fgimages/000000.png"]
    # キャラクターの位置
    fg_tl_list = [(200, 100)]

    # msgbox
    msgbox_tl = (35, 800)
    msgbox_br = (1880, 1055)
    # msgbox_hex = Color(hsv=(180, 1, .5)).hex
    msgbox_hex = Color(hsv=(223, 0.77, 0.38)).hex
    msgbox_alpha = 160

    # msg text area
    msg_margin = Margin(top=30, right=50, left=30, bottom=50)
    msg_line_spacing = 0
    msg_character_spacing = 5
    msg_font_size = 50
    msg_ruby_font_size = 20
    msg_ruby_line_spacing = -15
    msg_ruby_character_spacing = 1
    msg_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
    msg_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
    msg_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"

    # namebox
    namebox_tl = (15, 735)
    namebox_br = (600, 820)
    namebox_hex = Color(hsv=(220, 0.6, 0.3)).hex
    namebox_alpha = 180

    # name text area
    name_margin = Margin(top=2, right=0, left=30, bottom=2)
    name_line_spacing = 0
    name_character_spacing = 5
    name_font_size = 44
    name_ruby_font_size = 16
    name_ruby_line_spacing = -10
    name_ruby_character_spacing = 0
    name_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
    name_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
    name_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"

    # option box
    optionbox_tl = (230, 250)
    optionbox_br = (1680, 385)
    optionbox_hex = Color(hsv=(0, 0.0, 0.05)).hex
    optionbox_alpha = 255

    optionbox2_tl = (230, 435)
    optionbox2_br = (1680, 570)

    # option text area
    option_margin = Margin(top=20, right=0, left=30, bottom=0)
    option_line_spacing = 0
    option_character_spacing = 5
    option_font_size = 50
    option_ruby_font_size = 20
    option_ruby_line_spacing = -15
    option_ruby_character_spacing = 1
    option_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
    option_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
    option_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"
