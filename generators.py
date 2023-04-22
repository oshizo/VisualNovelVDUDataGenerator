import dataclasses
from dataclasses import dataclass
from PIL import Image
from utils import remove_ruby_tags
from configs import CFG1
from generation_utils import create_textarea, create_box


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
        gt_parse["options"] = self.option_texts    
        gt_parse["names"] = [self.name_text] if self.name_text is not None else []
        gt_parse["messages"] = [self.text] if self.text is not None else []
        return gt_parse
    
    def to_gt_parse_ruby(self):
        # ルビ情報付き
        gt_parse_ruby = {}
        gt_parse_ruby["options"] = self.option_texts_ruby
        gt_parse_ruby["names"] = [self.name_text_ruby] if self.name_text_ruby is not None else []
        gt_parse_ruby["messages"] = [self.text_ruby] if self.text_ruby is not None else []
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

    # message
    msgbox_img = create_box(
        *cfg.msgbox.size.tuple, hex=cfg.msgbox.bg_hex, alpha=cfg.msgbox.bg_alpha
    )
    msg_text_img, rendered_msg = create_textarea(cfg.msgbox)
    msgbox_img.paste(msg_text_img, (0, 0), msg_text_img)
    img.paste(msgbox_img, cfg.msgbox.tl.tuple, msgbox_img)
    output.text_ruby = rendered_msg

    # name
    if cfg.namebox is not None:
        namebox_img = create_box(
            *cfg.namebox.size.tuple,
            hex=cfg.namebox.bg_hex,
            alpha=cfg.namebox.bg_alpha,
        )
        name_text_img, rendered_name = create_textarea(cfg.namebox)
        namebox_img.paste(name_text_img, (0, 0), name_text_img)
        img.paste(namebox_img, cfg.namebox.tl.tuple, namebox_img)
        output.name_text_ruby = rendered_name

    # options
    for option_cfg in cfg.optionbox_list:
        optionbox_img = create_box(
            *option_cfg.size.tuple,
            hex=option_cfg.bg_hex,
            alpha=option_cfg.bg_alpha,
        )
        option_text_img, rendered_option = create_textarea(option_cfg)
        optionbox_img.paste(option_text_img, (0, 0), option_text_img)
        img.paste(optionbox_img, option_cfg.tl.tuple, optionbox_img)
        output.option_texts_ruby.append(rendered_option)

    output.image = img
    return output
