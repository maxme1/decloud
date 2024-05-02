import sys

from telegram.normalizer import normalize


normalize(*sys.argv[1:])
