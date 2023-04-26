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
    ruby_line_spacing: int = 5
    ruby_character_spacing: int = 1
    centering : bool = False

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
        if self.has_ruby:
            # ルビフォントサイズをフォントの1/2にする前提で計算
            return (
                2
                * (
                    self.size.height
                    - (self.margin.top + self.margin.bottom)
                    - self.line_spacing
                    - self.ruby_line_spacing
                )
                // 3
            )
            # return (
            #     self.size.height
            #     - (self.margin.top + self.margin.bottom)
            #     - self.line_spacing
            #     - self.ruby_line_spacing
            #     - self.ruby_font.size
            # )
        else:
            return (
                self.size.height
                - (self.margin.top + self.margin.bottom)
                - self.line_spacing
            )

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

    def change_ruby_font_size(self, size: int):
        self.ruby_font = ImageFont.truetype(self.ruby_font.path, size=int(size))

    @property
    def has_ruby(self):
        return "<ruby>" in self.text


@dataclass
class ImageCFG:
    path: str = "./sample_images/sample_bg.png"
    tl: Point = Point(x=0, y=0)


@dataclass
class CFG1:
    W: int = 1920
    H: int = 1080

    # 背景画像
    bg_cfg: ImageCFG = ImageCFG()

    # キャラクターの位置
    character_cfg_list: list[ImageCFG] = dataclasses.field(default_factory=list)

    # メッセージボックスと名前1つ、選択肢は複数
    msgbox: TextBoxCFG = TextBoxCFG()
    namebox: TextBoxCFG = TextBoxCFG()
    optionbox_list: list[TextBoxCFG] = dataclasses.field(default_factory=list)
