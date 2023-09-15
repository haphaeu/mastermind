from mastermind import response


def test_response():
    assert response('rrrr', 'gggg') == (0, 0)
    assert response('rrrb', 'rgbb') == (2, 0)
    assert response('rrbb', 'bggr') == (0, 2)
    assert response('rrcr', 'ccrc') == (0, 2)
    assert response('rrcr', 'ggrg') == (0, 1)
    assert response('cmyb', 'cmyb') == (4, 0)
    assert response('rrbb', 'bbrr') == (0, 4)
    assert response('rrcr', 'rgrg') == (1, 1)
    assert response('rrrr', 'rrrr') == (4, 0)
    assert response('rrgr', 'ggrr') == (1, 2)
