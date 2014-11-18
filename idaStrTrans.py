# -*- coding: utf-8 -*-  
# Translate current string in IDA Pro
# author : fuyzen@gmail.com

# install:
# easy_install goslate
# easy_install chardet

import struct
import re

def read_string(ea, coding=''):
    bytes = []
    if coding == 'utf-16':
        # Read UCS-2LE in Windows
        while Word(ea) != 0:
            bytes.append(struct.pack('H', Word(ea)))
            ea += 2
    else:
        # Read ANSI or UTF-8
        while Byte(ea) != 0:
            bytes.append(struct.pack('B', Byte(ea)))
            ea += 1
            
    s = ''.join(bytes)
    print 'processing:', [s]
    
    # if codepage is not given manually, anto detect
    if coding == '':
        # detect codepage
        import chardet
        codepage = chardet.detect(s)
        print 'codepage may', codepage['encoding'], \
               'confidence', codepage['confidence']
        if codepage['confidence'] < 0.6:
            print 'Auto detect may not precise enough. Please give manually.'
            return
        coding = codepage['encoding']
        
    return s.decode(coding)
    
# call Google Translate
# sometime it would fail, try again
def google_trans(u, dstLan, dstCoding):
    s = ''
    if u:
        try:
            #call Google Translate
            import goslate
            gs = goslate.Goslate()
            s = gs.translate(u, dstLan).encode(dstCoding)
        except:
            print 'translate error, try again!'
    return s
 
def is_utf16_has_chinese(u):
    # have chinese?
    return re.match(u'[\u4e00-\u9fa5]+', u)
    
# arg0: current address in IDA
# arg1: soutce coding, can be auto detected. If detect result is wrong, can be set manually. 
#       it can be utf-8/utf-16/gb2312/big5/euc-kr etc...
# arg2: dest language，default 'zh-cn'
# arg3: dest coding，default 'gbk'
def translate(ea, srcCoding='', dstLan='zh-cn', dstCoding='gbk'):
    u = read_string(ea, srcCoding)
    s = None
    if u:
        if is_utf16_has_chinese(u) and dstLan.lower() == 'zh-cn':
            # if the string contain Chinese, direct encode to gbk
            s = u.encode('gbk')
        else:
            s = google_trans(u, dstLan, dstCoding)
            
        if s:
            Message(dstLan + ' result: ' + s + '\n')
    return s

# ------------translate funcitons------------
# ANSI、UTF-8 to Chinese
def trans2cn():
    s = translate(ScreenEA())
    if s : MakeRptCmt(ScreenEA(), s)
    
# ANSI、UTF-8 to English
def trans2en():
    s = translate(ScreenEA(), dstLan='en', dstCoding='ascii')
    if s : MakeRptCmt(ScreenEA(), s)
    
# euc-kr to Chinese 
def trans_kr2cn():
    s = translate(ScreenEA(), 'euc-kr')
    if s : MakeRptCmt(ScreenEA(), s)
    
# euc-kr to English
def trans_kr2en():
    s = translate(ScreenEA(), 'euc-kr', 'en', 'ascii')
    if s : MakeRptCmt(ScreenEA(), s)
    
# Windows Unicode(UTF-16LE) to Chinese 
def trans2cn_u():
    s = translate(ScreenEA(), 'utf-16')
    if s : MakeRptCmt(ScreenEA(), s)
    
# Windows Unicode(UTF-16LE) to English
def trans2en_u():
    s = translate(ScreenEA(), 'utf-16', 'en', 'ascii')
    if s : MakeRptCmt(ScreenEA(), s)
#-------------------------------------

def add_hot_key(key, str_func):
    idaapi.CompileLine('static %s() { RunPythonStatement("%s()"); }'%(str_func, str_func))
    AddHotkey(key, str_func)
    
if __name__ == '__main__':
    
    # set hotkeys
    add_hot_key('F3', 'trans2cn');
    add_hot_key('F4', 'trans2en');
    add_hot_key('Ctrl-F3', 'trans_kr2cn');
    add_hot_key('Ctrl-F4', 'trans_kr2en');
    add_hot_key('Shift-F3', 'trans2cn_u');
    add_hot_key('Shift-F4', 'trans2en_u');
    
    print '-----------------------------------------'
    print 'Use F3 translate ANSI/UTF-8 to Chinese'
    print 'Use F4 translate ANSI/UTF-8 to English'
    print 'Use Ctrl-F3 translate Korea to Chinese'
    print 'Use Ctrl-F4 translate Korea to English'
    print 'Use Shift-F3 translate Unicode to Chinese'
    print 'Use Shift-F4 translate Unicode to English'
    print '-----------------------------------------'
    
    # if auto detect is wrong, temporary manually given here 
    # s = translate(ScreenEA(), 'euc-kr')
    # if s : MakeRptCmt(ScreenEA(), s)