#region Imports
import time
import re
from pyfiglet import Figlet
from pynput.mouse import Listener as MouseListener
from pytesseract import image_to_string
from PIL import Image
from ctypes import windll
import keyboard
import win32api
import win32gui
import win32con
import win32ui
import win32process
#endregion

awakening_interval = 2.8


def main():
	attribute1 = input('What is the attribute? ')
	min_value_attr1 = int(input(f'What is the minimum value of {attribute1}? '))

	attribute2 = input('What is the attribute 2? (Optional) ')
	if not attribute2:
		attribute2 = attribute1
		min_value_attr2 = min_value_attr1
		attr_same_time = 'n'
	else:
		min_value_attr2 = int(input(f'What is the minimum value of {attribute2}?'))
		attr_same_time = input('Both Attribute at the same time? (y/n) ')

	maximum_attempts = int(input('Maximum awake attempts? '))

	hwnd = get_hwnd_from_pid(19664)
	start_awake_button_pos = get_window_point(hwnd)
	awake_area_pos = get_window_region(hwnd)

	start_countdown(3)

	print('\nHold "q" to stop the bot.')
	awake_count = 0
	while keyboard.is_pressed('q') == False:
		awake_area = window_screenshot(hwnd, awake_area_pos)
		awake_area_converted = image_convertion(awake_area)
		awake_text_list = get_text_from_image(awake_area_converted)

		if awake_count >= maximum_attempts:
			print(f'Maximum attempts reached! {maximum_attempts} attempts.')
			exit()

		# Search for the awake
		attr_same_time_found = 0
		for attr in awake_text_list:
			if attr_same_time.lower() == 'y' or attr_same_time.lower() == 'yes':
				if attribute1 in attr and attr_same_time_found == 0:
					attr_value = int(re.findall('\d+', attr)[0])
					if min_value_attr1 <= attr_value:
						attr_same_time_found = 1
				if attribute2 in attr and attr_same_time_found == 1:
					attr_value = int(re.findall('\d+', attr)[0])
					if min_value_attr2 <= attr_value:
						print(f'Wanted:\n\t{attribute1}: +{min_value_attr1}\n\t{attribute2}: +{min_value_attr2}')
						print(f'\nFound: {awake_text_list}')
						print(f'Awake Attempts: {awake_count}\n')
						exit()
			else:
				if attribute1 in attr:
					attr_value = int(re.findall('\d+', attr)[0])
					if min_value_attr1 <= attr_value:
						print(f'\nFound: {awake_text_list}')
						print(f'Awake Attempts: {awake_count}\n')
						exit()
				if attribute2 in attr:
					attr_value = int(re.findall('\d+', attr)[0])
					if min_value_attr2 <= attr_value:
						print(f'\nFound: {awake_text_list}')
						print(f'Awake Attempts: {awake_count}\n')
						exit()

		#click in awake button
		magic_click(hwnd, *start_awake_button_pos)
		time.sleep(awakening_interval)
		awake_count += 1

# region Image
def window_screenshot(hwnd, region):
	x, y, width, height = region
	wDC = win32gui.GetWindowDC(hwnd)
	dcObj = win32ui.CreateDCFromHandle(wDC)
	cDC = dcObj.CreateCompatibleDC()
	dataBitMap = win32ui.CreateBitmap()
	dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
	cDC.SelectObject(dataBitMap)
	cDC.BitBlt((0, 0), (width, height), dcObj, (x, y), win32con.SRCCOPY)

	bmpinfo = dataBitMap.GetInfo()
	bmpstr = dataBitMap.GetBitmapBits(True)

	img = Image.frombuffer(
		'RGB',
		(bmpinfo['bmWidth'], bmpinfo['bmHeight']),
		bmpstr, 'raw', 'BGRX', 0, 1)

	dcObj.DeleteDC()
	cDC.DeleteDC()
	win32gui.ReleaseDC(hwnd, wDC)
	win32gui.DeleteObject(dataBitMap.GetHandle())

	return img


def image_convertion(pil_img):
	return pil_img.convert('1', dither=Image.NONE) # Convert PIL img to bw


def get_text_from_image(img):
	# get text and split in array
	text_list = image_to_string(img, lang='eng').split('\n')
	# Delete empty strings
	text_list = [i for i in text_list if i.strip()]
	#Print the list
	print(', '.join(text_list))
	return text_list
# endregion


# region Mouse

def get_hwnd_from_pid(pid):
    hwnd_list = []

    def callback(hwnd, hwnd_list):
        _, window_pid = win32process.GetWindowThreadProcessId(hwnd)
        
        if window_pid == pid:
            hwnd_list.append(hwnd)

    win32gui.EnumWindows(callback, hwnd_list)

    return hwnd_list[0] if hwnd_list else None


def get_window_point(hwnd):
	print('\nClick in the "start" awakening button! The first click will be considered.')
	pos = []
	x_win, y_win, cx_win, cy_win = win32gui.GetWindowRect(hwnd)

	def on_click(x, y, button, pressed):
		if pressed:
			pos.extend((x - x_win, y - y_win))
		if not pressed:
			return False

	with MouseListener(on_click=on_click) as mouse_listener:
		mouse_listener.join()

	time.sleep(0.5)
	return (pos[0], pos[1] + 10)


def get_window_region(hwnd, use_coordinates=False):
	print("\nSelect the top-left corner of the white awakening area, then select the " +
		  "bottom-right corner.\nThe two first clicks will be considered.")

	region = []
	absolute_position = []
	is_first_click = [True]
	x_win, y_win, cx_win, cy_win = win32gui.GetWindowRect(hwnd)

	def on_click(x, y, button, pressed):
		if pressed:
			if is_first_click[0]:
				region.extend((x - x_win, y - y_win))
				absolute_position.extend((x, y))
				is_first_click[0] = False
			else:
				if not use_coordinates:
					width = x - absolute_position[0]
					height = y - absolute_position[1]
					region.extend((width, height))
				else:
					region.extend((x - x_win, y - y_win))
				return False

	with MouseListener(on_click=on_click) as mouse_listener:
		mouse_listener.join()

	time.sleep(0.5)
	return region


def magic_click(hwnd, x, y):
	old_pos = win32api.GetCursorPos()
	windll.user32.BlockInput(True)
	win32api.SetCursorPos((x, y))
	win32api.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, 0)
	time.sleep(0.005)
	win32api.PostMessage(hwnd, win32con.WM_LBUTTONUP, None, 0)
	time.sleep(0.015)
	win32api.SetCursorPos(old_pos)
	windll.user32.BlockInput(False)
	
# endregion


# region Helpers
def start_countdown(sleep_time_sec=5):
	print('Starting', end='')
	for i in range(10):
		print('.', end='')
		time.sleep(sleep_time_sec/10)
	print('\nReady, forcing dwarves to work!')


def print_logo(text_logo: str):
	figlet = Figlet(font='slant')
	print(figlet.renderText(text_logo))
# endregion


if __name__ == '__main__':
	try:
		print_logo('Flyff Awake Bot')
		main()
	except Exception as e:
		print(str(e))
