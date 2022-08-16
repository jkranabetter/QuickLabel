import os 
import glob
from constants import *

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
