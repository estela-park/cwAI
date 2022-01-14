import argparse


parser = argparse.ArgumentParser()
# parser.add_argument('arg1', help='you can write sth helpful to figure this out')
# parser.add_argument('arg2')
# parser.add_argument('arg3')
parser.add_argument('-arg4')
parser.add_argument('-f', '--flag', action='store_true')
parser.add_argument('-c', '--count', action='count')
args = parser.parse_args()


## positional arg
# print('first arg:', args.arg1)
# print('second arg:', args.arg2)
# print('third arg:', args.arg3)


## optional arg
if args.arg4:
    print("you've just figured this out")
    
if args.flag:
    print('flag is used')
else:
    print('flag is not in use')

if args.count:
    print('counted:', args.count)