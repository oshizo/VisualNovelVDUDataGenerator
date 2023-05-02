import random
from PIL import Image, ImageDraw
from configs import Point, TextBoxCFG
from colorutils import Color
from fontTools.ttLib import TTFont


def get_random_color_pair(s: float = None):
    is_dark_font = random.random() > 0.5
    font = Color(
        hsv=(
            random.uniform(0, 360),
            s if s is not None else random.uniform(0.0, 0.5),
            random.uniform(0, 0.3) if is_dark_font else random.uniform(0.7, 1),
        )
    )
    bg = Color(
        hsv=(
            random.uniform(0, 360),
            s if s is not None else random.uniform(0.0, 0.5),
            random.uniform(0.7, 1) if is_dark_font else random.uniform(0, 0.3),
        )
    )
    return font.hex, bg.hex


def create_box(w: int, h: int, hex: str, alpha: int = 255):
    shape = [(0, 0), (w, h)]
    img = Image.new("RGB", (w, h))
    img1 = ImageDraw.Draw(img)
    img1.rectangle(shape, fill=hex, outline=None)
    img.putalpha(alpha)
    return img


def get_height(font):
    return font.size
    # baselineからascentとdescentの合計を返す
    # フォントによっては行間が大きくなりすぎるので、やめてフォントサイズを返すことにした
    # return font.getmetrics()[0] + font.getmetrics()[1]


def get_tiled_option_cfgs(
    nrow: int,
    ncol: int,
    tl: Point,
    br: Point,
    cfgs: list[TextBoxCFG],
    fit_font: bool = True,
    nowrap: bool = False,
    margin_h=20,
    margin_w=50,
):
    """
    nrow: 縦方向に並べる画像の数
    ncol: 横方向に並べる画像の数
    tl: 左上の座標
    br: 右下の座標
    base_cfg: 画像の基本情報
    fit_font: textから予想される行数が収まるようにフォントサイズを調整するかどうか（最大3行）

    入力されたcfgsの位置.tl,.brをタイル上のレイアウトに配置する。
    tlとbrの間に入りきらない場合は、サイズを調整する。
    フォントサイズをtextboxのサイズに合わせて調整する。
    """
    assert len(cfgs) <= nrow * ncol

    max_h = ((br.y - tl.y) // nrow) - margin_h
    h = min(max_h, cfgs[0].size.height)
    if nowrap:
        # 1行レイアウトの場合は、テキストの高さに合わせてサイズを調整する
        h = min(h, cfgs[0].minheight)

    max_w = ((br.x - tl.x) // ncol) - margin_w
    w = min(max_w, cfgs[0].size.width)

    # tl.yとbr.yの中心周りに配置する
    starty = int(tl.y + (br.y - tl.y) // 2 - (h * nrow + margin_h * (nrow - 1)) // 2)

    for irow in range(nrow):
        for icol in range(ncol):
            i = irow * ncol + icol
            if i == len(cfgs):
                break
            # 引数のcfgを上書き
            cfg = cfgs[i]
            cfg.tl = Point(tl.x + icol * (w + margin_w), starty + irow * (h + margin_h))
            cfg.br = Point(cfg.tl.x + w, cfg.tl.y + h)

            if fit_font:
                # テキストの長さに応じてフォントサイズを調節
                max_font_size_nrows = cfg.max_font_size_whole_text()

                # 28より小さくなる場合は、1行レイアウトの最大サイズcfg.max_font_size()にする
                cfg.change_font_size(
                    min(cfg.max_font_size(), max(max_font_size_nrows, 28))
                )
                # cfg.change_font_size(max_font_size_nrows)  # 28未満にはしない

            else:
                # 1行で高さがはみ出す場合にフォントサイズを調節
                cfg.change_font_size(min(cfg.max_font_size(), cfg.font.size))

            # ルビはfontサイズの1/4～1/2にする
            cfg.change_ruby_font_size(min(cfg.ruby_font.size, cfg.font.size // 2))
            cfg.change_ruby_font_size(max(cfg.ruby_font.size, cfg.font.size // 4))

    return cfgs


def ttfont_has_glyph(ttfont, glyph):
    for table in ttfont["cmap"].tables:
        if ord(glyph) in table.cmap.keys():
            return True
    return False


def char_in_font(font, ttfont, char):
    # has_glyphがTrueでも、代替文字を設定していない場合なにもレンダリングされない場合がある
    # その場合、getmask(char).size[1]が0になることがある。
    # スペースなどの一部の文字も0になるが、それらをフォールバックフォントで描画しても問題ないため、
    # 0の場合は一律フォールバックフォントを使うことにする
    if font.getmask(char).size[1] == 0:
        return False

    if ttfont is None:
        return True
    else:
        # フォントによっては代替文字（四角にバツ印など）を用意しているので、TTFontで確認する
        return ttfont_has_glyph(ttfont, char)


def create_textbox(cfg: TextBoxCFG) -> tuple[Image.Image, str]:
    box = create_box(*cfg.size.tuple, hex=cfg.bg_hex, alpha=cfg.bg_alpha)
    textarea, rendered_text, max_x = create_textarea(cfg)

    textarea_tl = (0, 0)
    if cfg.centering:
        textarea_tl = (int((cfg.size.width - max_x - cfg.margin.left) // 2), 0)
    box.paste(textarea, textarea_tl, textarea)
    return box, rendered_text


def create_textarea(cfg: TextBoxCFG) -> tuple[Image.Image, str, int]:
    rendered_text = ""  # 描画済みのテキスト（改行ではみ出す場合は描画したところまでを返却する）

    text = cfg.text
    ruby = cfg.ruby
    has_ruby = cfg.has_ruby
    size = cfg.size
    margin = cfg.margin
    line_spacing = cfg.line_spacing
    character_spacing = cfg.character_spacing
    ruby_line_spacing = cfg.ruby_line_spacing
    ruby_character_spacing = cfg.ruby_character_spacing
    font_hex = cfg.font_hex

    font = cfg.font
    # ttfontは文字があるかを判定するために使う
    try:
        ttfont = TTFont(font.path)
    except:
        ttfont = None
    fallback_font = cfg.fallback_font  # 文字がない場合のフォールバック先

    ruby_font = cfg.ruby_font
    try:
        ruby_ttfont = TTFont(font.path)
    except:
        ruby_ttfont = None
    fallback_ruby_font = cfg.fallback_ruby_font

    # テキストはw, hの範囲に描画する
    # ルビのはみ出しはmarginまで許容し、それ以上はみ出すと描画されない
    text_img = Image.new(
        "RGBA",
        (
            size.width,  # + margin.right + margin.left,
            size.height,  # + margin.top + margin.bottom,
        ),
        (0, 0, 0, 0),  # 背景色（透明）
    )
    text_img_draw = ImageDraw.Draw(text_img)

    # centeringのためにテキストの右端を記憶する
    text_max_x = -1

    # テキスト描画の開始位置
    x = margin.left
    y = margin.top

    if has_ruby:
        # ルビの描画位置を確保するために、ルビの高さをyに加算
        y += get_height(ruby_font) + ruby_line_spacing

    # テキストを1文字ずつ描画する際の一時情報
    in_ruby_target = False

    ruby = ""
    ruby_target = ""
    ruby_target_x = {"left": -1, "right": -1}
    ruby_newline_checked = False

    # テキストを1文字ずつ描画
    # <ruby>漢字<rt>かんじ</rt></ruby> の形式を想定
    # 一つの<ruby>タグに複数の<rt>は含められない（rubyタグ自体を複数使って記述する必要がある）
    next_i = -1
    for i, c in enumerate(text):
        # タグの読み飛ばし
        if next_i > i:
            continue

        if c == "<":  # タグ記述の開始時
            tag = text[i : i + text[i:].index(">") + 1]  # <ruby>の場合、tag = "<ruby>"

            if tag == "<ruby>":
                ruby_newline_checked = False  # このループで文字描画前にルビ対象文字中に改行があるかを判定する
                ruby_target = text[i + 6 : i + 6 + text[i + 6 :].index("<")]  # ルビ対象文字列
                ruby_target_x["left"] = x  # ruby対象文字列の開始x
                in_ruby_target = True
                next_i = i + 6  # タグが終わるまで読み飛ばす（次の文字はルビ対象文字列の1文字目）

            elif tag == "</ruby>":
                in_ruby_target = False
                next_i = i + 7  # タグが終わるまで読み飛ばす

            elif tag == "<rt>":
                ruby = text[i + 4 : i + 4 + text[i + 4 :].index("<")]  # ルビ文字列
                ruby_target_x["right"] = x - character_spacing  # ruby対象文字列の右端のx座標
                next_i = i + 4 + text[i + 4 :].index("<")  # ルビの最期まで読み飛ばす（次の文字は</rt>の<）

            elif tag == "</rt>":
                if has_ruby:
                    # ルビを一括で描画する
                    ruby_target_width = ruby_target_x["right"] - ruby_target_x["left"]
                    ruby_center_x = (ruby_target_x["left"] + ruby_target_x["right"]) / 2

                    # ルビ対象文字列の幅と、ルビを普通に配置した時の幅を両方計算して比較する
                    ruby_characters_width = sum(
                        [ruby_font.getlength(rc) for rc in ruby]
                    )
                    ruby_calcled_width = ruby_characters_width + (
                        ruby_character_spacing * (len(ruby) + 1)
                    )
                    if ruby_target_width > ruby_calcled_width and len(ruby) > 1:
                        # ルビ対象文字列の幅が広い場合は、ruby_target_xの間に均等割り付け
                        _ruby_character_spacing = (
                            ruby_target_width - ruby_characters_width
                        ) / (len(ruby) + 1)
                        ruby_x = ruby_target_x["left"] + _ruby_character_spacing
                    else:
                        # 幅が足りない場合（私（わたくし）など）は、ruby_center_x周りにruby_character_spacingで配置
                        ruby_x = ruby_center_x - ruby_calcled_width / 2
                        _ruby_character_spacing = ruby_character_spacing

                        if ruby_x < 0:
                            # 一文字目に長いrubyがある場合描画範囲からはみ出すことがあるため、エラーを上げる
                            raise ValueError(
                                f"Ruby overflowed from the left of the text area. {ruby_x}"
                            )

                    # 高さ計算
                    ruby_y = y - (get_height(ruby_font) + ruby_line_spacing)

                    # ルビを1文字ずつ描画
                    for rc in ruby:
                        text_img_draw.text(
                            (ruby_x, ruby_y),
                            rc,
                            fill=font_hex,
                            font=ruby_font
                            if char_in_font(ruby_font, ruby_ttfont, rc)
                            else fallback_ruby_font,
                        )
                        ruby_x += ruby_font.getlength(rc) + _ruby_character_spacing
                        text_max_x = max(text_max_x, ruby_x - _ruby_character_spacing)
                        if ruby_x - _ruby_character_spacing > size.width:
                            # 右側にはみ出した場合は描画されないため、エラーを上げる
                            raise ValueError(
                                f"Ruby overflowed from the right of the text area. {ruby_x - _ruby_character_spacing} > {size.width}"
                            )
                rendered_text = text[: i + 1]

                # ルビ情報リセット
                ruby_target_x = {"left": -1, "right": -1}
                ruby = ""
                ruby_target = ""
                next_i = i + 5  # タグが終わるまで読み飛ばす

            else:
                raise ValueError(f"Invalid tag: {tag}")
            continue

        # 改行判定
        insert_new_line = False
        if in_ruby_target:
            if not ruby_newline_checked:
                # ルビ対象中は改行しない
                # ルビ対象文字の1文字目にルビ終了までの長さを先読みして改行判定
                insert_new_line = x + sum(
                    [font.getlength(_c) + character_spacing for _c in ruby_target]
                ) > (size.width - margin.right)
                if insert_new_line:
                    ruby_target_x["left"] = margin.left
                ruby_newline_checked = True
        else:
            insert_new_line = x + font.getlength(c) > (size.width - margin.right)

        # 改行処理
        if insert_new_line:
            y += get_height(font) + line_spacing
            if has_ruby:
                y += get_height(ruby_font) + ruby_line_spacing
            x = margin.left

            # 改行した行が入りきるか判定
            next_line_bottom_y = y + get_height(font)
            if has_ruby:
                next_line_bottom_y += get_height(ruby_font) + ruby_line_spacing
            if next_line_bottom_y > text_img.size[1]:
                return text_img, rendered_text, text_max_x  # 改行までに描画した文字列を返す

        # draw character
        text_img_draw.text(
            (x, y),
            c,
            fill=font_hex,
            font=font if char_in_font(font, ttfont, c) else fallback_font,
        )  # , anchor="lt")
        rendered_text = text[: i + 1]

        x += font.getlength(c) + character_spacing
        text_max_x = max(text_max_x, x - character_spacing)

    return text_img, text, text_max_x
