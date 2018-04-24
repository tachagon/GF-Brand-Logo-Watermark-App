#! python3
# resizeAndAddLogo.py - Resizes all images in current working directory to fit
# in a 300x300 square, and adds catlogo.png to the lower-right corner.

import os
from PIL import Image

LOGO_SIZE_BY_PERCENT = 25

LOGO_DIRECTORY = 'logo'
INPUT_DIRECTORY = 'input'
OUTPUT_DIRECTORY = 'output'

LOGO_STYLE_1 = 'logo_style_1.png'
LOGO_STYLE_2 = 'logo_style_2.png'
LOGO_STYLE_3 = 'logo_style_3.png'

LOGO_FILENAME = LOGO_STYLE_1

WANT_BACKGROUND = False

# Start the program

print('1. Choose logo style (1, 2 or 3)')
print('(enter nothing for choose style 1)')
logoStyleInput = input()

if len(logoStyleInput) > 0:
	if logoStyleInput == '1':
		LOGO_FILENAME = LOGO_STYLE_1
	elif logoStyleInput == '2':
		LOGO_FILENAME = LOGO_STYLE_2
	elif logoStyleInput == '3':
		LOGO_FILENAME = LOGO_STYLE_3

print('2. Enter percent of logo size')
print('(enter nothing for choose default is 25 percent)')
logoSizePercentInput = input()

if len(logoSizePercentInput) > 0:
	try:
		LOGO_SIZE_BY_PERCENT = float(logoSizePercentInput)
	except Exception as e:
		print('Error! You should enter percent as a number.')

print('3. Do you want any background: Y or N')
print('(enter nothing for choose N (No))')
wantBackground = input()

if len(wantBackground) > 0:
	if wantBackground == 'Y' or wantBackground == 'y':
		WANT_BACKGROUND = True

# Open Logo image
logoIm = Image.open(os.path.join(LOGO_DIRECTORY, LOGO_FILENAME))
logoWith, logoHeight = logoIm.size

# Create output derectory
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Loop over all files in the working directory.

for filename in os.listdir(INPUT_DIRECTORY):
	if not (filename.endswith('.png') or filename.endswith('.jpg')) \
		or filename == LOGO_FILENAME:
		continue # skip non-image files and the logo file itself

	im = Image.open(os.path.join(INPUT_DIRECTORY, filename))
	width, height = im.size

	# Resize logo

	if width > height:
		oldLogoHeight = logoHeight
		logoHeight = int(height * LOGO_SIZE_BY_PERCENT / 100)
		logoWith = int(logoWith * logoHeight / oldLogoHeight)
	else:
		oldLogoWidth = logoWith
		logoWith = int(width * LOGO_SIZE_BY_PERCENT / 100)
		logoHeight = int(logoHeight * logoWith / oldLogoWidth)

	logoIm = logoIm.resize((logoWith, logoHeight), Image.ANTIALIAS)

	# Add background
	if WANT_BACKGROUND:
		backgroundIm = Image.new('RGBA', (logoWith, logoHeight), (0, 0, 0, 64))
		im.paste(backgroundIm, (width - logoWith, height - logoHeight), backgroundIm)

	# Add the logo.

	print('Adding logo to %s...' % (filename))
	im.paste(logoIm, (width - logoWith, height - logoHeight), logoIm)

	# Save changes.

	im.save(os.path.join(OUTPUT_DIRECTORY, filename), optimize=True)