# Pixel Art Parser

Pixel Art Parser is a Python3 script for analyzing a pixel art image and producing text output of the corresponding DMC embroidery floss color codes. Useful for when you want to make a cross-stitch of a pixel art, but don't want to pick out the colors yourself.

## Installation
This script depends on Python libraries `colormath` and `Pillow`. Install them with pip
```
pip3 install colormath
pip3 install Pillow
```

## Usage
```
python3 parserMain.py path/to/image/file
```

## Sample Output
For example, [this image](kiwi.png) will produce the output:
```
19 x 18

       AAAAAAA     
    AAAAAAAAAAA    
   AABBBBBBBAAAA   
  ABBBBBBBBBBBAAA  
 ABBBBBBBBBBBBBAAA 
 ABBCBBCBCBBCBBAAAA
ABBBBCBCBCBCBBBBAAA
ABBBBBBBBBBBBBBBAAA
ABBBCCBBDBBCCBBBAAA
ABBBBBBDDDBBBBBBAAA
ABBBCCBDDDBCCBBBAAA
ABBBBBBBDBBBBBBBAAA
ABBBBCBBBBBCBBBBAAA
 ABBCBBCBCBBCBBAAA 
 ABBBBBCBCBBBBBAAA 
  ABBBBBBBBBBBAAA  
   AABBBBBBBAAAA   
     AAAAAAAAA     

A: 869
B: 704
C: 310
D: B5200
```
