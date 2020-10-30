from PIL import Image, ImageDraw
import string

from colormath.color_objects import sRGBColor, LabColor
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie2000

COLORCODE_FILE = 'colorCodes'

# Return a value (delta_e) that indicates how different
# the given colors are, where greater value means larger
# difference.
# Both c1rgb and c2rgb should be a 3-tuple of rgb values
# in the range [0,1]
def colorDiff(c1rgb, c2rgb):
  color1_lab = convert_color(sRGBColor(*c1rgb), LabColor)
  color2_lab = convert_color(sRGBColor(*c2rgb), LabColor)
  return delta_e_cie2000(color1_lab, color2_lab)

def makeClosestColorMap(colorToLetterMap, rgbToCodeMap):
  colorToClosestColorMap = {} # hashmap of [0,255] color value to closest [0,1] color value
  closestColorToColorMap = {} # reverse of colorToClosestColorMap
  remainingColors = set(colorToLetterMap.keys()) # set of [0,255] colors needing closest color
  while len(remainingColors) > 0:
    color = remainingColors.pop()
    used = set([])
    while True:
      closestColor = getClosestColor(color, rgbToCodeMap, used)
      if closestColor in closestColorToColorMap:
        competitor = closestColorToColorMap[closestColor]
        if colorDiff(normalizeColorVal(color), closestColor) < colorDiff(normalizeColorVal(competitor), closestColor):
          del colorToClosestColorMap[competitor]
          del closestColorToColorMap[closestColor]
          remainingColors.add(competitor)
          break
        used.add(closestColor)
      else:
        break
    colorToClosestColorMap[color] = closestColor
    closestColorToColorMap[closestColor] = color
  return colorToClosestColorMap

def makeColorCodeMap(image, rgbToCodeMap):
  [numCol, numRow] = image.size
  print('%r x %r\n' % (numCol, numRow))
  pix = image.load()
  first = True
  firstVal = None

  draw = ImageDraw.Draw(image)

  # loop through every pixel, store each color in a hashmap with a letter
  # as the key, and print the corresponding letter for each pixel
  letterIndex = 0;
  colorToLetterMap = {} # hashmap of [0,255] color value to letter
  letterToColorCodeMap = {} # hashmap of letter to color code
  for i in range(0, numRow):
    for j in range(0, numCol):
      val = pix[j,i]
      if first:
        firstVal = val
        first = False

      if val == firstVal:
        print(' ', end='')
        continue

      if val not in colorToLetterMap:
        letter = string.ascii_uppercase[letterIndex]
        colorToLetterMap[val] = letter
        letterIndex += 1;
      print(colorToLetterMap[val], end='')
    print()

  colorToClosestColorMap = makeClosestColorMap(colorToLetterMap, rgbToCodeMap)
  for i in range(0, numRow):
    for j in range(0, numCol):
      val = pix[j,i]
      if val == firstVal:
        continue

      letter = colorToLetterMap[val]
      closestColor = colorToClosestColorMap[val]
      letterToColorCodeMap[letter] = rgbToCodeMap[closestColor]
      draw.point([j,i], unnormalizeColorVal(closestColor))
  # image.save(str(WEIGHT_HUE) + '|' + str(WEIGHT_LIGHTNESS) + '|' + str(WEIGHT_SATURATION) + '.png', "PNG")
  image.save('new.png', "PNG")
  return letterToColorCodeMap

# Convert the given 6-character hex color value to a 3-tuple
# of non-negative numbers in the range [0,1]
# eg. ffffff -> (1, 1, 1)
#     3300ff -> (0.2, 0, 1)
def strColorToTuple(s):
  res = [0, 0, 0]
  res[0] = int(s[0:2], 16) / 255.0
  res[1] = int(s[2:4], 16) / 255.0
  res[2] = int(s[4:6], 16) / 255.0
  return tuple(res)

def getColorCodes():
  rgbToCodeMap = {} # hashmap of color rgb value to color code
  with open(COLORCODE_FILE) as f:
    for line in f:
      parts = line.split(' ')
      code = parts[0]
      rgb = strColorToTuple(parts[1])
      assert(rgb not in rgbToCodeMap)
      rgbToCodeMap[rgb] = code
  return rgbToCodeMap

# Given a 3-tuple in range [0,255], normalize to range [0,1]
def normalizeColorVal(val):
  return (val[0]/255.0, val[1]/255.0, val[2]/255.0)

# Given a 3-tuple in range [0,1], unnormalize to range [0,255]
def unnormalizeColorVal(val):
  return (int(val[0]*255), int(val[1]*255), int(val[2]*255))

def colorDiffWithUsed(canadidateColor, target, used):
  diff = colorDiff(canadidateColor, target)
  if canadidateColor in used:
    diff += 100
  return diff

# Given a [0,255] colorVal, return the closest [0,1] color we have
def getClosestColor(colorVal, rgbToCodeMap, used):
  target = normalizeColorVal(colorVal)
  return min(rgbToCodeMap.keys(), key=lambda c : colorDiffWithUsed(c, target, used))

def parseImage(pathToImage):
  rgbToCodeMap = getColorCodes()
  image = Image.open(pathToImage, 'r')
  letterToColorCodeMap = makeColorCodeMap(image, rgbToCodeMap)

  print()
  # print the letters and their corresponding color code in hexadecimal
  for i in range(len(letterToColorCodeMap)):
    letter = string.ascii_uppercase[i]
    code = letterToColorCodeMap[letter]
    print('%s: %s' % (letter, code))
  print()
  