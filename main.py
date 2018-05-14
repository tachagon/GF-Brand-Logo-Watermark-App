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

SPECIFY_LOGO_POSITION = False

isAuto = True

# Start the program

def ask_is_auto():
	print('Do you want auto for all pictures ? (Y or N)')
	print('(Enter nothing for Y (Yes))')
	isAutoInput = input()

	if len(isAutoInput) > 0:
		if isAutoInput == 'N' or isAutoInput == 'n':
			return False

	return True

def ask_type_of_logo():
	print('1. Choose logo style (1, 2 or 3)')
	print('(enter nothing for choose style 1)')
	logoStyleInput = input()

	if len(logoStyleInput) > 0:
		if logoStyleInput == '1':
			return LOGO_STYLE_1
		elif logoStyleInput == '2':
			return LOGO_STYLE_2
		elif logoStyleInput == '3':
			return LOGO_STYLE_3
	
	return LOGO_STYLE_1

def ask_size_of_logo():
	print('2. Enter percent of logo size')
	print('(enter nothing for choose default is 25 percent)')
	logoSizePercentInput = input()

	if len(logoSizePercentInput) > 0:
		try:
			return float(logoSizePercentInput)
		except Exception as e:
			print('Error! You should enter percent as a number.')

	return 25

def ask_has_background():
	print('3. Do you want any background: Y or N')
	print('(enter nothing for choose N (No))')
	wantBackground = input()

	if len(wantBackground) > 0:
		if wantBackground == 'Y' or wantBackground == 'y':
			return True

	return False

def ask_specify_logo_position():
	print('4. Do you want to specify logo position: Y or N')
	print('(enter nothing for choose N (No))')
	specifyLogoPosition = input()

	if len(specifyLogoPosition) > 0:
		if specifyLogoPosition == 'Y' or specifyLogoPosition == 'y':
			return True

	return False

# accep specify position from user
# position_name must be 'x' or 'y'
# user can choose center also
def ask_position(position_name, image_distance = 0, logo_distance = 0):
	print('')
	print('Specify ' + position_name + ' positon of logo. (Ref point: Bottom Right of Logo)')
	print('options here:')
	print('		type a number or')
	print('		"ct"	or	"center" ')
	print('		"id"	or 	"image distance" ')
	print('		"ld"	or 	"logo distance"')
	position_input = input()

	if position_input == 'ct' or position_input == 'center':
		return int((image_distance / 2) + (logo_distance / 2))
	elif position_input == 'id' or position_input == 'image distance':
		return int(image_distance)
	elif position_input == 'ld' or position_input == 'logo distance':
		return int(logo_distance)
	else:
		try:
			return int(position_input)
		except Exception as e:
			print('Error! You should inter a number.')
			return ask_position(position_name)

# ================================================================
# Start Program Here!
# ================================================================

isAuto = ask_is_auto()

if isAuto:
	# question 1 ask type of logo
	LOGO_FILENAME = ask_type_of_logo()

	# question 2 ask size of logo
	LOGO_SIZE_BY_PERCENT = ask_size_of_logo()

	# question 3 ask Are there any background
	WANT_BACKGROUND = ask_has_background()

	# question 4 ask specify logo position
	SPECIFY_LOGO_POSITION = ask_specify_logo_position()

# Create output derectory
os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)

# Loop over all files in the working directory.

for filename in os.listdir(INPUT_DIRECTORY):

	if not(isAuto):
		# question 1 ask type of logo
		LOGO_FILENAME = ask_type_of_logo()

		# question 2 ask size of logo
		LOGO_SIZE_BY_PERCENT = ask_size_of_logo()

		# question 3 ask Are there any background
		WANT_BACKGROUND = ask_has_background()

		# question 4 ask specify logo position
		SPECIFY_LOGO_POSITION = ask_specify_logo_position()

	# Open Logo image
	logoIm = Image.open(os.path.join(LOGO_DIRECTORY, LOGO_FILENAME))
	logoWith, logoHeight = logoIm.size

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

	print('Adding logo to %s...' % (filename))

	if SPECIFY_LOGO_POSITION:
		width = ask_position('x', width, logoWith)
		height = ask_position('y', height, logoHeight)

	if WANT_BACKGROUND:
		backgroundIm = Image.new('RGBA', (logoWith, logoHeight), (0, 0, 0, 64))
		im.paste(backgroundIm, (width - logoWith, height - logoHeight), backgroundIm)

	# Add the logo.

	im.paste(logoIm, (width - logoWith, height - logoHeight), logoIm)

	# Save changes.

	im.save(os.path.join(OUTPUT_DIRECTORY, filename), optimize=True)