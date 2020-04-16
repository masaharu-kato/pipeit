import os
import subprocess

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__) + '/..')
os.chdir(PROJECT_ROOT)

def test_pipeit():
    os.chdir('samples/project01')

    # clear cache
    subprocess.call(['tests/clear_cache.sh'])

    # load result
    result_answer = open('tests/test01.result.txt', mode='r').read()

    print('subprocess pwd:', subprocess.check_output(['pwd']))

    # test (without cache)
    assert result_answer == subprocess.check_output(['tests/test01.sh']).decode('utf-8')

    # test (with cache)
    assert result_answer == subprocess.check_output(['tests/test01.sh']).decode('utf-8')

