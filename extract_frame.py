import cv2
import os
import argparse

def extract_frame(path, file):
    if not os.path.exists(os.path.join(path, file.split('.')[0])):
        os.mkdir(os.path.join(path, file.split('.')[0]))
    else:
        for img in os.listdir(os.path.join(path, file.split('.')[0])):
            os.remove(os.path.join(path, file.split('.')[0], img))

    video = cv2.VideoCapture(os.path.join(path, file))
    path = os.path.join(path, file.split('.')[0])
    index = 0
    temp = 0
    while True:
        _, frame = video.read()
        temp += 1
        if not _:
            break

        if temp % 4 == 0:
            cv2.imwrite(os.path.join(path, file.split('.')[0] + "_" + str(index) + ".jpg"), frame)
            index += 1

def main(args):
    for folder in os.listdir(os.path.join(args.path, 'multiple')):
        if os.path.isdir(os.path.join(args.path, 'multiple', folder)):
            for file in os.listdir(os.path.join(args.path, 'multiple', folder)):
                if os.path.isfile(os.path.join(args.path, 'multiple', folder, file)) and file.split('.')[-1].lower() == 'mp4':
                    extract_frame(os.path.join(args.path, 'multiple', folder), file)

    for action in os.listdir(os.path.join(args.path, 'single')):
        if os.path.isdir(os.path.join(args.path, 'single', action)):
            for position in os.listdir(os.path.join(args.path, 'single', action)):
                if os.path.isdir(os.path.join(args.path, 'single', action, position)):
                    for file in os.listdir(os.path.join(args.path, 'single', action, position)):
                        if os.path.isfile(os.path.join(args.path, 'single', action, position, file)) and file.split('.')[-1].lower() == 'mp4':
                            extract_frame(os.path.join(args.path, 'single', action, position), file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="path to dataset folder", default='dataset')
    args = parser.parse_args()
    main(args)
