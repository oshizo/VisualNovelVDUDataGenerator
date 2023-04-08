from generation_utils import create_textarea, create_textbox
from PIL import Image, ImageFont
from configs import CFG1

from dataclasses import dataclass
from colorutils import Color


@dataclass
class Outputs:
    image = None
    text = None
    name_text = None
    option_texts: list


def create_image(cfg: CFG1) -> Outputs:
    output = Outputs(option_texts=[])

    # bg
    bg = Image.open(cfg.bg_path).resize((cfg.W, cfg.H))
    img = bg.copy()

    # character
    for path, fg_tl in zip(cfg.fg_pathlist, cfg.fg_tl_list):
        fg = Image.open(path)
        fg = fg.resize((int(fg.width * (cfg.H / fg.height)), cfg.H))
        img.paste(fg, fg_tl, fg)

    # message
    msgbox_size = (
        cfg.msgbox_br[0] - cfg.msgbox_tl[0],
        cfg.msgbox_br[1] - cfg.msgbox_tl[1],
    )
    msgbox = create_textbox(
        w=msgbox_size[0], h=msgbox_size[1], hex=cfg.msgbox_hex, alpha=cfg.msgbox_alpha
    )

    add_ruby = "<ruby>" in cfg.text
    msg_font = ImageFont.truetype(font=cfg.msg_font_path, size=cfg.msg_font_size)
    msg_ruby_font = ImageFont.truetype(
        font=cfg.msg_ruby_font_path, size=cfg.msg_ruby_font_size
    )
    msg_text_img, rendered_msg = create_textarea(
        cfg.text,
        w=msgbox_size[0] - (cfg.msg_margin.left + cfg.msg_margin.right),
        h=msgbox_size[1] - (cfg.msg_margin.top + cfg.msg_margin.bottom),
        margin=cfg.msg_margin,
        font=msg_font,
        font_color=cfg.msg_font_color,
        character_spacing=cfg.msg_character_spacing,
        line_spacing=cfg.msg_line_spacing,
        add_ruby=add_ruby,
        ruby_font=msg_ruby_font,
        ruby_font_color=cfg.msg_font_color,
        ruby_character_spacing=cfg.msg_ruby_character_spacing,
        ruby_line_spacing=cfg.msg_ruby_line_spacing,
    )

    msgbox.paste(msg_text_img, (0, 0), msg_text_img)
    img.paste(msgbox, cfg.msgbox_tl, msgbox)
    output.text = rendered_msg

    # name
    if cfg.name_text is not None:
        namebox_size = (
            cfg.namebox_br[0] - cfg.namebox_tl[0],
            cfg.namebox_br[1] - cfg.namebox_tl[1],
        )
        namebox = create_textbox(
            w=namebox_size[0],
            h=namebox_size[1],
            hex=cfg.namebox_hex,
            alpha=cfg.namebox_alpha,
        )

        add_ruby = "<ruby>" in cfg.name_text
        name_font = ImageFont.truetype(font=cfg.name_font_path, size=cfg.name_font_size)
        name_ruby_font = ImageFont.truetype(
            font=cfg.name_ruby_font_path, size=cfg.name_ruby_font_size
        )
        name_text_img, rendered_name = create_textarea(
            cfg.name_text,
            w=namebox_size[0] - (cfg.name_margin.left + cfg.name_margin.right),
            h=namebox_size[1] - (cfg.name_margin.top + cfg.name_margin.bottom),
            margin=cfg.name_margin,
            font=name_font,
            font_color=cfg.name_font_color,
            character_spacing=cfg.name_character_spacing,
            line_spacing=cfg.name_line_spacing,
            add_ruby=add_ruby,
            ruby_font=name_ruby_font,
            ruby_font_color=cfg.name_font_color,
            ruby_character_spacing=cfg.name_ruby_character_spacing,
            ruby_line_spacing=cfg.name_ruby_line_spacing,
        )
        namebox.paste(name_text_img, (0, 0), name_text_img)
        img.paste(namebox, cfg.namebox_tl, namebox)
        output.name_text = rendered_name

    # options
    if len(cfg.option_texts) > 0:
        optionbox_size = (
            cfg.optionbox_br[0] - cfg.optionbox_tl[0],
            cfg.optionbox_br[1] - cfg.optionbox_tl[1],
        )
        optionbox = create_textbox(
            w=optionbox_size[0],
            h=optionbox_size[1],
            hex=cfg.optionbox_hex,
            alpha=cfg.optionbox_alpha,
        )

        add_ruby = "<ruby>" in cfg.option_texts[0]
        option_font = ImageFont.truetype(
            font=cfg.option_font_path, size=cfg.name_font_size
        )
        option_ruby_font = ImageFont.truetype(
            font=cfg.option_ruby_font_path, size=cfg.name_ruby_font_size
        )
        option_text_img, rendered_option = create_textarea(
            cfg.option_texts[0],
            w=optionbox_size[0] - (cfg.option_margin.left + cfg.option_margin.right),
            h=optionbox_size[1] - (cfg.option_margin.top + cfg.option_margin.bottom),
            margin=cfg.option_margin,
            font=option_font,
            font_color=cfg.option_font_color,
            character_spacing=cfg.option_character_spacing,
            line_spacing=cfg.option_line_spacing,
            add_ruby=add_ruby,
            ruby_font=option_ruby_font,
            ruby_font_color=cfg.option_font_color,
            ruby_character_spacing=cfg.option_ruby_character_spacing,
            ruby_line_spacing=cfg.option_ruby_line_spacing,
        )
        optionbox.paste(option_text_img, (0, 0), option_text_img)
        img.paste(optionbox, cfg.optionbox_tl, optionbox)
        output.option_texts.append(rendered_option)

    # option2
    if len(cfg.option_texts) > 1:
        optionbox2 = create_textbox(
            w=optionbox_size[0],
            h=optionbox_size[1],
            hex=cfg.optionbox_hex,
            alpha=cfg.optionbox_alpha,
        )

        add_ruby = "<ruby>" in cfg.option_texts[1]
        option2_text_img, rendered_option2 = create_textarea(
            cfg.option_texts[1],
            w=optionbox_size[0] - (cfg.option_margin.left + cfg.option_margin.right),
            h=optionbox_size[1] - (cfg.option_margin.top + cfg.option_margin.bottom),
            margin=cfg.option_margin,
            font=option_font,
            font_color=cfg.option_font_color,
            character_spacing=cfg.option_character_spacing,
            line_spacing=cfg.option_line_spacing,
            add_ruby=add_ruby,
            ruby_font=option_ruby_font,
            ruby_font_color=cfg.option_font_color,
            ruby_character_spacing=cfg.option_ruby_character_spacing,
            ruby_line_spacing=cfg.option_ruby_line_spacing,
        )
        optionbox2.paste(option2_text_img, (0, 0), option2_text_img)
        img.paste(optionbox2, cfg.optionbox2_tl, optionbox2)
        output.option_texts.append(rendered_option2)
    output.image = img
    return output
