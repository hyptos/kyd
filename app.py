import argparse
import sys
import bench


def init():
    print 'init'

parser = argparse.ArgumentParser(prog='KYP')
parser.add_argument('-s', '--size', help='size of the test',action='store_false')
parser.add_argument('-o', '--only', type=bool, help='test only this size of the test', default=False)
parser.add_argument('-p', '--protocol', choices=['sdk', 'rest','all'], default='all')
parser.add_argument('-m', '--premium', type=bool, help='Account used is premium', default=False)
parser.add_argument('-f', '--file', type=argparse.FileType('r'), help='file to test', default=False)
parser.add_argument('-t', '--transfert', choices=['inter', 'upload','download','upDown'], default='upDown')
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
args = parser.parse_args()

if __name__ == '__main__':
    print 'arg de size: ' + str(args.size)
    print 'arg de only: ' + str(args.only)
    print 'arg de protocol: ' + str(args.protocol)
    print 'arg de transfert: ' + str(args.transfert)
    print 'arg de file: ' + str(args.file)

    if args.size is None and args.file is False:
        print 'You have to give us a size or give us a file'
        #sys.exit()

    print 'You choose to do all tests with a random file of ' + str(args.size)
    #d = engine_dp.DropboxBench()
    d.start()
    #a = bench.S3Bench()
    a.start()
    #g = engine_gd.GoogleDriveBench()
    g.start()
    print 'c\'est fini'