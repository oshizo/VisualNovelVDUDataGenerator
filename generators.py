import dataclasses
from dataclasses import dataclass
from PIL import Image
from utils import remove_ruby_tags
from configs import CFG1
from generation_utils import create_textarea, create_textbox


@dataclass
class Outputs:
    image: Image = None

    text_ruby: str = None
    name_text_ruby: str = None
    option_texts_ruby: list = dataclasses.field(default_factory=list)

    @property
    def text(self):
        return remove_ruby_tags(self.text_ruby) if self.text_ruby else None

    @property
    def name_text(self):
        return remove_ruby_tags(self.name_text_ruby) if self.name_text_ruby else None

    @property
    def option_texts(self):
        return [remove_ruby_tags(option) for option in self.option_texts_ruby]

    def to_gt_parse(self):
        # ルビ情報なし
        gt_parse = {}
        gt_parse["options"] = (
            [self.option_texts] if self.option_texts is not None else []
        )
        gt_parse["names"] = [self.name_text] if self.name_text is not None else []
        gt_parse["messages"] = [self.text] if self.text is not None else []
        return gt_parse

    def to_gt_parse_ruby(self):
        # ルビ情報付き
        gt_parse_ruby = {}
        gt_parse_ruby["options"] = (
            [self.option_texts_ruby] if self.option_texts_ruby else []
        )
        gt_parse_ruby["names"] = (
            [self.name_text_ruby] if self.name_text_ruby is not None else []
        )
        gt_parse_ruby["messages"] = (
            [self.text_ruby] if self.text_ruby is not None else []
        )
        return gt_parse_ruby


# CFG1用の画像生成関数
# メッセージボックス1つ、名前ボックス0～1個、選択肢0～N個
def generate_data(cfg: CFG1) -> Outputs:
    output = Outputs()

    # bg
    bg = Image.open(cfg.bg_cfg.path).resize((cfg.W, cfg.H))
    img = bg.copy()

    # characters
    for ch_cfg in cfg.character_cfg_list:
        fg = Image.open(ch_cfg.path)
        fg = fg.resize((int(fg.width * (cfg.H / fg.height)), cfg.H))
        img.paste(fg, ch_cfg.tl.tuple, fg)

    # UI要素
    for noocr_cfg in cfg.noocrbox_list:
        noocrbox_img, _ = create_textbox(noocr_cfg)
        img.paste(noocrbox_img, noocr_cfg.tl.tuple, noocrbox_img)
        # ★OCR対象ではないため、outputに追加しない

    # message
    if cfg.msgbox is not None:
        msgbox_img, rendered_msg = create_textbox(cfg.msgbox)
        img.paste(msgbox_img, cfg.msgbox.tl.tuple, msgbox_img)
        output.text_ruby = rendered_msg

    # name
    if cfg.namebox is not None:
        namebox_img, rendered_name = create_textbox(cfg.namebox)
        img.paste(namebox_img, cfg.namebox.tl.tuple, namebox_img)
        output.name_text_ruby = rendered_name

    # options
    for option_cfg in cfg.optionbox_list:
        optionbox_img, rendered_option = create_textbox(option_cfg)
        img.paste(optionbox_img, option_cfg.tl.tuple, optionbox_img)
        output.option_texts_ruby.append(rendered_option)

    output.image = img
    return output
