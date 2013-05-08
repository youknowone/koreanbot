
# -*- coding: utf-8 -*-
import trans

def test_trans():
    res = trans.trans('Hello', 'en', 'ko')
    print res
    assert res == u'여보세요'
