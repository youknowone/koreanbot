
# -*- coding: utf-8 -*-
import daum

def test_daum():
    ko = daum.daum('dinctionary')
    assert ko == u'사전,  딕셔너리'

    en = daum.daum(u'사전')
    assert en == u'a dictionary,  a wordbook,  a lexicon'
