import argparse

def init():
    print 'init'

parser = argparse.ArgumentParser(prog='KYP')
parser.add_argument('-s', '--size', type=int, help='size of the test')
parser.add_argument('-o', '--only', type=bool, help='test only this size of the test', default=False)
parser.add_argument('-p', '--protocol', choices=['sdk', 'rest','all'], default='all')
parser.add_argument('-t', '--transfert', choices=['inter', 'upload','download','upDown'], default='upDown')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if __name__ == '__main__':
    print 'arg de size: ' + str(args.size)
    print 'arg de only: ' + str(args.only)
    print 'arg de protocol: ' + str(args.protocol)
    print 'arg de transfert: ' + str(args.transfert)
