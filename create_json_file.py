import json
import argparse
import os
import cv2


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, required=True,
                        help='path to the file with prepared annotations')
    parser.add_argument('--iscrowd', type=int, default=0,
                        help='1 if picture contains multiple people, else 0')
    parser.add_argument('--image_server', type=str, required=True,
                        help='Image server url. Example: localhost:8080')
    parser.add_argument('--num_persons', type=int, default=1,
                        help='Number of persons in dataset')
    parser.add_argument('--json_out', type=str, default='out.json',
                        help='Json output file')
    args = parser.parse_args()
    return args


def get_shape(img_file):
    img = cv2.imread(img_file)
    h, w, _ = img.shape
    return h, w


def create_json_file(args):
    images = list()
    annotations = list()

    image_id = 0
    annotation_id = 0
    root_url = args.image_server

    # set up categories
    categories = []
    for i in range(args.num_persons):
        category = {"supercategory": "person", "id": i, "name": "person_" + str(i),
                    "keypoints": ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_shoulder",
                                  "right_shoulder", "left_elbow", "right_elbow", "left_wrist", "right_wrist",
                                  "left_hip", "right_hip", "left_knee", "right_knee", "left_ankle", "right_ankle"],
                    "skeleton": [[16, 14], [14, 12], [17, 15], [15, 13], [12, 13], [6, 12], [7, 13], [6, 7], [6, 8],
                                 [7, 9], [8, 10], [9, 11], [2, 3], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7]]}
        categories.append(category)
    licenses = [{"url": "http://creativecommons.org/licenses/by-nc-sa/2.0/", "id": 1,
                 "name": "Attribution-NonCommercial-ShareAlike License"},
                {"url": "http://creativecommons.org/licenses/by-nc/2.0/", "id": 2,
                 "name": "Attribution-NonCommercial License"},
                {"url": "http://creativecommons.org/licenses/by-nc-nd/2.0/", "id": 3,
                 "name": "Attribution-NonCommercial-NoDerivs License"},
                {"url": "http://creativecommons.org/licenses/by/2.0/", "id": 4, "name": "Attribution License"},
                {"url": "http://creativecommons.org/licenses/by-sa/2.0/", "id": 5,
                 "name": "Attribution-ShareAlike License"},
                {"url": "http://creativecommons.org/licenses/by-nd/2.0/", "id": 6,
                 "name": "Attribution-NoDerivs License"},
                {"url": "http://flickr.com/commons/usage/", "id": 7, "name": "No known copyright restrictions"},
                {"url": "http://www.usa.gov/copyright.shtml", "id": 8, "name": "United States Government Work"}]

    for root, dirs, files in os.walk(args.image_dir):
        for file in files:
            if file.endswith(".jpg"):
                image = dict()
                annotation = dict()
                file_name = os.path.join(root, file)
                license = "license"
                height, width = get_shape(file_name)
                url = os.path.join(root_url, file_name)
                # print(url)
                # image
                image['id'] = str(args.iscrowd) + '_' + str(image_id)
                image['height'] = height
                image['width'] = width
                image['file_name'] = file
                image['license'] = '6'
                image['url'] = url
                # license
                image_id += 1
                annotation_id += 1
                images.append(image)
    # print
    json_data = {'annotations': annotations, 'images': images, 'categories': categories, 'licenses': licenses}
    with open(args.json_out, 'w') as fout:
        json.dump(json_data, fout)


if __name__ == '__main__':
    args = parse_args()
    create_json_file(args)
