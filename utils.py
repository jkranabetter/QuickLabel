import os 
import glob
from constants import *
import cv2

def verify_directories():
    # create unlabelled folder if it doesnt already exist
    if not os.path.isdir(UNLABELLED_FOLDER):
        print('no unlabelled folder... creating it for you')
        os.makedirs(UNLABELLED_FOLDER)

    # create class folders if they dont already exist
    for folder in FOLDERS:
        folder_path = os.path.join(LABELLED_FOLDER, folder)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)
            print(f'created folder {folder_path}')

def fileCount(folder) -> int:
    "count the number of files in a directory"

    num_files = 0
    num_dir = 0

    for base, dirs, files in os.walk(folder):
        for dir in dirs:
            num_dir += 1
        for file in files:
            num_files += 1

    return num_files

def print_results():
    """
    Calculate the results of classification and display them
    for the user on the console
    """
    # get the pictures in the 3 folders and the unlabelled
    os.chdir("./labelled/-1")
    files_minus_1 = glob.glob("*")
    os.chdir("../0")
    files_0 = glob.glob("*")
    os.chdir("../1")
    files_1 = glob.glob("*")
    os.chdir("../../unlabelled")
    unlabelled_files = glob.glob("*")

    # calculate results
    total = len(files_minus_1) + len(files_0) + len(files_1)
    error_per = round(len(files_minus_1) / total * 100, 2)
    undecided_per = round(len(files_0) / total * 100, 2)
    good_per = round(len(files_1) / total * 100, 2)

    # print results
    print("\nResults:")
    print(str(total) + " total images classified.")
    print(str(len(files_minus_1)) + " images classified as -1: " + str(error_per) + "%")
    print(str(len(files_0)) + " images classified as 0: " + str(undecided_per) + "%")
    print(str(len(files_1)) + " images classified as 1: " + str(good_per) + "%")
    print(str(len(unlabelled_files)) + " unclassified images remaining.")

def show_feedback(image, key):

    if KEY_BINDINGS[key] == 'class -1':
        # Red color in BGR
        color = (0, 0, 200)
        text = 'mislabel'
    elif KEY_BINDINGS[key] == 'class 0':
        # Blue color in BGR
        color = (255, 100, 0)
        text = 'fail'
    elif KEY_BINDINGS[key] == 'class 1':
        # Green color in BGR
        color = (0, 150, 0)
        text = 'pass'
    elif KEY_BINDINGS[key] == 'undo':
        color = (100, 100, 100)
        text = 'undo'
    elif KEY_BINDINGS[key] == 'exit':
        # white
        color = (255, 255, 255)
        text = 'see ya'
    else:
        color = (0,0,0)
        text = 'no command'

    font = cv2.FONT_HERSHEY_DUPLEX
    thickness = 2
    fontScale = 1

    # get the text size and calculate position for text
    (text_w, text_h), baseline = cv2.getTextSize(text, font, fontScale, thickness)
    org_x = round(image.shape[1] / 2)
    org_y = round(image.shape[0] / 2)
    text_org = (org_x - round(text_w / 2), org_y + round(text_h/2) + round(baseline/2))

    # draw a black box behind text for better contrast
    cv2.rectangle(image, (org_x - round(text_w / 2), org_y - round(text_h / 2)), (org_x + round(text_w / 2), org_y + round(text_h / 2) + baseline), (0,0,0), -1)
    image = cv2.putText(image, text, text_org, font, fontScale, color, thickness, cv2.LINE_AA)

    # show the selected class on the image for a moment before changing images
    cv2.imshow(WINDOW_STRING, image)
    cv2.waitKey(250)

def resize_image(img):
    """
    resize image based on largest dimension
    """
    # resize image
    h, w, c = img.shape
    max_dim = max(h, w)
    if max_dim == h:
        change_ratio = MAX_WINDOW_HEIGHT / h
        width = int(img.shape[1] * change_ratio)
        height = int(MAX_WINDOW_HEIGHT)
    else:
        change_ratio = MAX_WINDOW_WIDTH / w
        width = int(MAX_WINDOW_WIDTH)
        height = int(img.shape[0] * change_ratio)
    dim = (width, height)
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resized
