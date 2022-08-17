from utils import *
'''
Script for model 2 "clarity model" wheat head labelling. 

Use the a w d keys to assign the shown image to the one of the classes -1, 0, or 1.

Use the 'escape' key to terminate the program.

Key assignments:
a = class -1
w = class 0
d = class 1
u = undo

'''


class MaxStack(list):

    def __init__(self, max_size):
        super().__init__()
        self.max_size = max_size

    def push(self, element):
        self.append(element)

    def append(self, element):
        super().append(element)

        if super().__len__() > self.max_size:
            super().__delitem__(0)


def main():

    # make sure the proper directories exist
    verify_directories()

    # make sure unlabelled folder is not empty
    if file_count(UNLABELLED_FOLDER) == 0:
        print('your unlabelled folder is empty!')
        return

    # create file stack
    file_stack = []

    # get files in the directory and store in the stack
    for item in os.listdir(UNLABELLED_FOLDER):

        # check if the file is an image
        if item.endswith(".png") or item.endswith(".jpg"):
            file_stack.append(item)

    # sort files alphabetically
    file_stack.sort()

    # create buffer stack
    buffer_stack = MaxStack(BUFFER_SIZE)

    # run through the image files one by one
    while file_stack:

        # stack peek
        current_image = file_stack[-1]

        image_path = os.path.join(UNLABELLED_FOLDER, current_image)

        print(f'annotating image: {image_path}')
        number_unlabelled = file_count(UNLABELLED_FOLDER)
        number_labelled = file_count(LABELLED_FOLDER)
        print(f'{number_labelled} labelled, {number_unlabelled} unlabelled files')

        img = cv2.imread(image_path, cv2.IMREAD_ANYCOLOR)

        resized = resize_image(img)

        # display image and read keypress
        key_pressed = False
        key = None
        while not key_pressed:

            cv2.namedWindow(WINDOW_STRING, cv2.WINDOW_AUTOSIZE)
            cv2.imshow(WINDOW_STRING, resized)
            key = str(cv2.waitKey(0))

            if key in KEY_BINDINGS.keys():
                key_pressed = True

        show_feedback(resized, key)

        # exit by pressing the escape key
        if KEY_BINDINGS[key] == 'exit':
            print('terminating program')
            cv2.destroyAllWindows()
            print_results()
            break

        # assign a class with a w d keys
        if KEY_BINDINGS[key] == 'class -1':
            print('\tmoving to mislabelled folder')
            item1 = file_stack.pop()
            print(item1)
            destination_path_mislabel = os.path.join(LABELLED_FOLDER, FOLDERS[0], current_image)
            buffer_stack.push(
                (current_image, image_path, destination_path_mislabel))
            os.rename(image_path, destination_path_mislabel)
        elif KEY_BINDINGS[key] == 'class 0':
            print('\tmoving to fail folder')
            file_stack.pop()
            destination_path_fail = os.path.join(LABELLED_FOLDER, FOLDERS[1], current_image)
            buffer_stack.push(
                (current_image, image_path, destination_path_fail))
            os.rename(image_path, destination_path_fail)
        elif KEY_BINDINGS[key] == 'class 1':
            print('\tmoving to pass folder')
            file_stack.pop()
            destination_path_pass = os.path.join(LABELLED_FOLDER, FOLDERS[2], current_image)
            buffer_stack.push(
                (current_image, image_path, destination_path_pass))
            os.rename(image_path, destination_path_pass)
        elif KEY_BINDINGS[key] == 'undo':
            if not buffer_stack:
                print('the undo buffer is already empty, cant go back further')
                continue
            print('\tundo previous action')
            (buff_file, buff_source, buff_des) = buffer_stack.pop()
            os.rename(buff_des, buff_source)
            file_stack.append(buff_file)


if __name__ == '__main__':
    main()
