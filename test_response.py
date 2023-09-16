from mastermind import PEGS
from mastermind import response


def test_response():
    PEGS = 'rgbymc'
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


def test_cpp():
    """Benchmark using
    https://github.com/NathanDuran/Mastermind-Five-Guess-Algorithm/blob/master/Five-Guess-Algorithm.cpp
    """
    PEGS = '123456'
    fn = r"\\wsl.localhost\Ubuntu\home\rafros\git\Mastermind-Five-Guess-Algorithm\tests.txt"
    with open(fn) as f:
        games = [[i.strip() for i in g ] 
             for g in [line.split(',') 
             for line in f.readlines()]] 

    for guess, code, r in games:
        r0 = r.count('B'), r.count('W')
        r1 = response(guess, code)
        #print(guess, code, r0, r1, end='\r')
        assert r0 == r1

if __name__ == '__main__':
    test_response()
    test_cpp()