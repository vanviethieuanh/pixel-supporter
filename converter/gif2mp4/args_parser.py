import argparse

parser = argparse.ArgumentParser(
    prog='python gif2mp4.py',
    description='Convert GIF image to MP4 video.')

parser.add_argument('-l', '--loop', type=int, default=1,
                    help='Times that GIF gonna loop.')
parser.add_argument('-p', '--path', type=str, default='*.gif',
                    help='Paths to files. If not specify, program will wildcard ./*.gif')

args = parser.parse_args()