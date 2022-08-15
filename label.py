import os
import cv2

'''
Script for model 2 "clarity model" wheat head labelling. 

Use the a w d keys to assign the shown image to the one of the classes -1, 0, or 1.

Use the 'escape' key to terminate the program.

Key assignments:
a = class -1
w = class 0
d = class 1

Key Codes:
a = 97 A = 65
w = 119 W = 87
d = 100 D = 68
'''

UNLABELLED_FOLDER = 'test_Joshua'
LABELLED_FOLDER = 'test_sorted'

key_bindings = {
    '97' : 'class -1',
    '65' : 'class -1',
    '119' : 'class 0',
    '87' : 'class 0',
    '100' : 'class 1',
    '68' : 'class 1',
    '32' : 'pending',
    '27' : 'exit'
}

def fileCount(folder):
    "count the number of files in a directory"

    num_files = 0
    num_dir = 0

    for base, dirs, files in os.walk(folder):
        for dir in dirs:
            num_dir += 1
        for file in files:
            num_files += 1

    return num_files

# create class folders if they dont alread exist
folders = ['-1', '0', '1', 'pending']
for folder in folders:
    folder_path = os.path.join(LABELLED_FOLDER, folder)
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)
        print(f'created folder {folder_path}')

# get the path/directory
for item in os.listdir(UNLABELLED_FOLDER):

    number_unlabelled = fileCount(UNLABELLED_FOLDER)
    number_labelled = fileCount(LABELLED_FOLDER)
    print(f'there are {number_labelled} labelled files and {number_unlabelled} unlabelled files')

    # check if the file is an image
    image_path = os.path.join(UNLABELLED_FOLDER, item)
    
    if (image_path.endswith(".png") or image_path.endswith(".jpg")):
        print(f'annotating image: {item}')

        # read image
        img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)
        # check the image shape
        h, w, c = img.shape
        # resize image
        max_dim = max(h, w)
        if max_dim < 100:
            scale_percent = 500
        elif max_dim < 150:
            scale_percent = 400
        elif max_dim < 200:
            scale_percent = 300
        else:
            scale_percent = 250
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        # create window and show image
        cv2.namedWindow('finalImg', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('finalImg', resized)
        key = str(cv2.waitKey(0))
        print(key)

        if key in key_bindings.keys():
            # exit by pressing the escape key
            if key_bindings[key] == 'exit':
                print('terminating program')
                cv2.destroyAllWindows()
                break
            
            # assign a class with a w d keys
            if key_bindings[key] == 'class -1':
                print('\tmoving to mislabelled folder')
                destination_path_mislabell = os.path.join(LABELLED_FOLDER, folders[0], item)
                os.rename(image_path, destination_path_mislabell)
            elif key_bindings[key] == 'class 0':
                print('\tmoving to fail folder')
                destination_path_fail = os.path.join(LABELLED_FOLDER, folders[1], item)
                os.rename(image_path, destination_path_fail)
            elif key_bindings[key] == 'class 1':
                print('\tmoving to pass folder')
                destination_path_pass = os.path.join(LABELLED_FOLDER, folders[2], item)
                os.rename(image_path, destination_path_pass)
            elif key_bindings[key] == 'pending':
                print('\tmoving to pending folder')
                destination_path_pending = os.path.join(LABELLED_FOLDER, folders[3], item)
                os.rename(image_path, destination_path_pending)
            print(f'\tyou have assigned to {key_bindings[key]}')
