#!/usr/bin/env python
import sys
import time
import pysrt
import googletrans


def translate_srt(file_path):
    """
    given an srt file path, translate it to arabic using google translate
    """
    translator = googletrans.Translator()
    sub_file = pysrt.open(file_path)
    trans_ok = True
    for sub in sub_file:
        print(sub.text)
        sub.text = sub.text.replace('\n', ' ')
        while trans_ok:
            try:
                trans_ok = True
                trans = translator.translate(sub.text, src='en', dest='ar')
                trans_ok = False
            except Exception:
                print('FAILED!\nwaiting on server')
                time.sleep(120)
        sub.text = trans.text
        print(trans.text)
        trans_ok = True


if __name__ == '__main__':
    if len(sys.argv) > 1:
        for fp in sys.argv[1:]:
            translate_srt(fp)
    else:
        print('Please provide path to one srt file at least.')
