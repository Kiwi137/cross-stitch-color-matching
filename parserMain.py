from parserLogic import parseImage
import sys

def main():
  if len(sys.argv) < 2:
      raise RuntimeError('Usage: pixelArtParser.py path/to/image')
  parseImage(sys.argv[1])

main()
