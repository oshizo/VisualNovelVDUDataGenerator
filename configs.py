import dataclasses
from dataclasses import dataclass
from PIL import ImageFont
from utils import remove_ruby_tags


@dataclass
class Margin:
    top: int
    right: int
    bottom: int
    left: int


@dataclass
class Point:
    x: int
    y: int

    @property
    def tuple(self):
        return (self.x, self.y)


@dataclass
class Size:
    width: int
    height: int

    @property
    def tuple(self):
        return (self.width, self.height)


@dataclass
class TextBoxCFG:

    """
    (tl)
    +-------------------------------------------------+
    |                    (Margin)                     |
    |    +--------------------------------------+     |
    |    | text text text                       |     |
    |    +--------------------------------------+     |
    +-------------------------------------------------+
                                                   (br)

    ruby ruby ruby ruby ruby ruby ruby ruby ruby
    (ruby_line_spacing)
    text text text text text text text text text
    (line_spacing)
    ruby ruby ruby ruby ruby ruby ruby ruby ruby

    """

    text: str = ""
    ruby: str = ""
    # has_ruby: bool = True

    tl: Point = Point(x=0, y=0)
    br: Point = Point(x=200, y=100)
    margin: Margin = Margin(top=20, right=30, left=30, bottom=20)

    bg_hex: str = "#ffffff"
    bg_alpha: int = 255

    font_hex: str = "#000000"
    font: ImageFont = ImageFont.truetype(
        font="./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf", size=50
    )
    ruby_font: ImageFont = ImageFont.truetype(
        font="./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf", size=20
    )

    line_spacing: int = 10
    character_spacing: int = 3
    ruby_line_spacing: int = 0
    ruby_character_spacing: int = 1

    @property
    def minheight(self) -> int:
        if self.has_ruby:
            return (
                self.font.size
                + self.ruby_font.size
                + self.ruby_line_spacing
                + self.margin.top
                + self.margin.bottom
            )
        else:
            return int(self.font.size) + self.margin.top + self.margin.bottom

    @property
    def size(self):
        return Size(width=self.br.x - self.tl.x, height=self.br.y - self.tl.y)

    def max_font_size(self) -> int:
        fs = (
            self.size.height
            - (self.margin.top + self.margin.bottom)
            - self.line_spacing
        )

        if self.has_ruby:
            fs -= self.ruby_font.size + self.ruby_line_spacing
        return fs

    def max_font_size_whole_text(self) -> int:
        max_fs = -1
        nchar = len(remove_ruby_tags(self.text))
        W = self.size.width - (self.margin.left + self.margin.right)
        H = self.size.height - (self.margin.top + self.margin.bottom)
        wspace = self.character_spacing
        hspace = self.line_spacing
        if self.has_ruby:
            hspace += self.ruby_line_spacing + self.ruby_font.size
        for nrow in range(1, 5):  # 最大4行を想定
            # 幅が収まる条件と、高さが収まる条件のうち、小さい方を採用
            max_fs_nrow = min((nrow * W // nchar) - wspace, (H // nrow) - hspace)
            max_fs = max(max_fs, max_fs_nrow)
        return max_fs

    def change_font_size(self, size: int):
        self.font = ImageFont.truetype(self.font.path, size=int(size))

    @property
    def has_ruby(self):
        return "<ruby>" in self.text


@dataclass
class ImageCFG:
    path: str = "./sample_images/sample_bg.png"
    tl: Point = Point(x=0, y=0)


# @dataclass
# class CFG1:
#     text = ""
#     name_text = None
#     option_text = []
#     W = 1920
#     H = 1080
#     bg_path = "./bgimages/generated_bg-20230408T030427Z-001/generated_bg/0001.png"
#     # fg_pathlist = ["./fgimages/000000.png"]
#     # fg_tl_list = [(200, 100)]

#     # 背景画像
#     bg_cfg: ImageCFG

#     # キャラクターの位置
#     character_cfg_list: list[ImageCFG]

#     msgbox: TextBoxCFG
#     # # msgbox
#     # msgbox_tl = (35, 800)
#     # msgbox_br = (1880, 1055)
#     # # msgbox_hex = Color(hsv=(180, 1, .5)).hex
#     # msgbox_hex = Color(hsv=(223, 0.77, 0.38)).hex
#     # msgbox_alpha = 160

#     # # msg text area
#     # msg_margin = Margin(top=30, right=50, left=30, bottom=50)
#     # msg_line_spacing = 0
#     # msg_character_spacing = 5
#     # msg_font_size = 50
#     # msg_ruby_font_size = 20
#     # msg_ruby_line_spacing = 2
#     # msg_ruby_character_spacing = 1
#     # msg_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
#     # msg_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
#     # msg_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"

#     # namebox
#     namebox: TextBoxCFG
#     # namebox_tl = (15, 735)
#     # namebox_br = (600, 820)
#     # namebox_hex = Color(hsv=(220, 0.6, 0.3)).hex
#     # namebox_alpha = 180

#     # # name text area
#     # name_margin = Margin(top=2, right=0, left=30, bottom=2)
#     # name_line_spacing = 0
#     # name_character_spacing = 5
#     # name_font_size = 44
#     # name_ruby_font_size = 16
#     # name_ruby_line_spacing = 2
#     # name_ruby_character_spacing = 0
#     # name_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
#     # name_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
#     # name_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"

#     # option box
#     optionbox_cfg_list: list[TextBoxCFG]
#     # optionbox_tl_list = [(230, 250), (230, 435)]
#     # optionbox_br_list = [(1680, 385), (1680, 570)]
#     # optionbox_hex = Color(hsv=(0, 0.0, 0.05)).hex
#     # optionbox_alpha = 255

#     # # option text area
#     # option_margin = Margin(top=20, right=0, left=30, bottom=0)
#     # option_line_spacing = 0
#     # option_character_spacing = 5
#     # option_font_size = 50
#     # option_ruby_font_size = 20
#     # option_ruby_line_spacing = 2
#     # option_ruby_character_spacing = 1
#     # option_font_color = tuple([int(c) for c in Color(hsv=(0, 0, 1)).rgb])
#     # option_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Medium.otf"
#     # option_ruby_font_path = "./fonts/SourceHanSansJP/SourceHanSansJP-Bold.otf"


@dataclass
class CFG1:
    W: int = 1920
    H: int = 1080

    # 背景画像
    bg_cfg: ImageCFG = ImageCFG()

    # キャラクターの位置
    character_cfg_list: list[ImageCFG] = dataclasses.field(default_factory=list)

    msgbox: TextBoxCFG = TextBoxCFG()
    namebox: TextBoxCFG = TextBoxCFG()
    optionbox_list: list[TextBoxCFG] = dataclasses.field(default_factory=list)
