import argparse

def init():
    print 'init'

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--init' ,type=init)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if __name__ == '__main__':
    init()