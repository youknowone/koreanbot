
# -*- coding: utf-8 -*-
import naver

def test_naver():
    result = naver.naver(u'오렌지')
    assert result.split(' ')[0] == 'orange'

if __name__ == '__main__':
    test_naver()
