#! /usr/bin/env python

import markdown
import argparse
import re
import qrcode
import frontmatter
from os import path

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--input-file", dest="input_file", help="A markdown file", metavar="LOCAL")
parser.add_argument("-m", "--mode", dest="mode", help="Mode")
parser.add_argument("-t", "--output-type", dest="output_type", help="Output: default or wx.")
options = parser.parse_args()

OUT_HTML_FILE_HEAD = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title></title>
</head>

<body class="view" lang="zh">
  <p style="white-space: normal;"></p>
  <p style="white-space: normal;"></p>
  <section style="white-space: normal;background-color: rgb(255, 255, 255);max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;">
    <section style="max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;">
      <section style="padding-right: 20px;padding-left: 20px;line-height: 1.8;max-width: 100%;box-sizing: border-box !important;word-wrap: break-word !important;">
'''

OUT_HTML_FILE_FOOT = '''
      </section>
    </section>
  </section>
</body>

</html>
'''

FONT_FAMILY = 'font-family: inhert;'
FONT_FAMILY_ALT = 'font-family:Optima-Regular, PingFangTC-light'

STY_P = 'color:#3f3f3f; font-size: 100%; ' + FONT_FAMILY + '; margin: 0.4em 0 1em 0;'
STY_PRE = 'background: #2e2e2e; border-radius: 4px; padding: 10px; color:#fff; font-size: 70%; font-family:menlo,monospace; margin: 0.4em 0 1em 0;'
STY_TABLE = 'color:#3f3f3f; font-size: 80%; ' + FONT_FAMILY + '; margin: 0.4em 0 1em 0;'
STY_CODE = 'font-size: 80%;font-family: \'Operator Mono\', Consolas, Monaco, Menlo, monospace;background: #f8f5ec;padding: 3px 5px;border-radius: 4px;color: #c7254e;'
STY_H2 = 'font-size: 120%; color:#3f3f3f;' + FONT_FAMILY + '; margin: 3em 0 2em 0; font-weight: normal; text-align: center'
STY_H3 = 'font-size: 100%; color:#3f3f3f;' + FONT_FAMILY + '; margin: 2em 0 0.5em 0; font-weight: bold'
STY_UL = 'color:#3f3f3f; font-size: 100%; ' + FONT_FAMILY + '; margin: 0.4em 0 1em 0; padding-left: 1.4em; list-style-type: circle;'
STY_OL = 'color:#3f3f3f; font-size: 100%; ' + FONT_FAMILY + '; margin: 0.4em 0 1em 0; padding-left: 1.4em;'
STY_HR = 'padding: 0;border: none;border-bottom: 1px solid #333;color: #333;text-align: center;margin: 40px 0;font-size: 12px;line-height: 1.2;opacity: 0.2;'
STY_HR_SYMBOL = 'display: inline-block;     margin-bottom: -2em;vertical-align: top;font-size: 1.5em;padding: 0px 0.25em;background: white;'
STY_LI = 'color:#3f3f3f; font-size: 100%; ' + FONT_FAMILY + '; margin: 0.2em 0 0.2em 0;'
STY_IMG = 'border-radius: 4px; display: block; margin: 0 auto; width: 100%;'
STY_IMG_FIXED = 'border: 1px solid #000; display: block; margin: 0 auto; height: 120px; width: 120px; max-height: 120px; max-width: 120px;'
DIV_FOOTNOTE = 'color:#666; font-size: 80%; ' + FONT_FAMILY + '; margin: 0.4em 0 1em 0;'

wx_html_styles = [
    ('<pre>', STY_PRE),
    ('<p>', STY_P),
    ('<table>', STY_TABLE),
    ('<h2>', STY_H2),
    ('<h3>', STY_H3),
    ('<ul>', STY_UL),
    ('<ol>', STY_OL),
    ('<li>', STY_LI),
    ('<code>', STY_CODE),
    ('<div class="hr"', STY_HR),
    ('<span class="hr-symbol"', STY_HR_SYMBOL),
    ('<div class="footnote"', DIV_FOOTNOTE),
    # ('<img', STY_IMG_FIXED),
    ('<img', STY_IMG),
]

def load_markdown_file(input_file):
    with open(input_file) as fd:
        post = frontmatter.load(fd)
    return post

def to_html(text):
    html = markdown.markdown(text,  ['markdown.extensions.extra'], output_format="html5")
    return html

def add_styles(html):
    for st_key, st_content in wx_html_styles:
        if st_key.endswith('>'):
            html = html.replace(st_key, st_key[0:-1] + ' style="' + st_content + '"' + '>')
        else:
            html = html.replace(st_key, st_key + ' style="' + st_content + '"')
    return html

def write_file(outpath, html):
    fd = open(outpath, 'w')
    fd.write(OUT_HTML_FILE_HEAD)
    fd.write(html)
    fd.write(OUT_HTML_FILE_FOOT)
    fd.close()

# get links from source. all links are start a line.
def get_links_from_markdown(md):
    ret = []
    for line in md.splitlines():
        if line.startswith('http://') or line.startswith('https://'):
            ret.append(line)
    return ret

# entry
def process_file(options):
    post = load_markdown_file(options.input_file)
    outpath = './dist/'
    if options.mode == 'qr':
        # generate qrcode from markdown file.
        links = get_links_from_markdown(post.content)
        print(links)
        for i, link in enumerate(links):
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(link)
            qr.make(fit=True)
            img = qr.make_image()
            _, prefix = path.split(options.input_file)
            prefix = prefix[2:10]
            img.save('%s/%s-%s.jpg' % (outpath, prefix, (i + 1)))
    else:
        # generate html file.
        html = to_html(post.content)
        if options.output_type == 'wx':
            # replace all external links
            html = re.sub(r'<a (\S+?) href', r'<a href', html)
            html = re.sub(r'<a href="(?!https://mp.weixin).+?">(.+?)</a>', r'<span>\1</span>', html)
            # stylish hr
            html = html.replace('<hr>', '<div class="hr"><span class="hr-symbol">§</span></div>')
            # stylish 
            # apply style to other tags
            html = add_styles(html)
        write_file(outpath + '/index.html', html)

if __name__ == '__main__':
    if options.input_file:
        process_file(options)
    else:
        print('usage: ./process.py -t [Output Type] -m [Run Mode] -f [Markdown File]')
        print('\tRun Mode:')
        print('\t\tqr\t extract links and generate qrcode file.')
        print('\Output Type:')
        print('\t\twx\t generate a html file for wechat official account.')
        print('\t\thtml\t generate a regular html file.')
