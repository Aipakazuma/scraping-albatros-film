# -*- coding:utf-8 -*-
import cv2


image_path = './img/'


def matching():
    im = cv2.imread(image_path + 'b.jpg', cv2.IMREAD_GRAYSCALE)  # 比較するImageFile
    image_hist = cv2.calcHist([im], [0], None, [256], [0, 256])

    target = compare_target_hist(image_hist)

    result = []

    while True:
        try:
            result.append(target.__next__())

        except StopIteration:
            break

    result.sort(reverse=True)

    return result


# 比較されるImageFile
def gen_target():
    yield image_path + 'b.jpg'
    yield image_path + 'c.jpg'
    yield image_path + '9a7dbba0ec3589372c20eed3c32f2f7e1.jpg'
    yield image_path + '621b78ce7c250b0db4025cd2ffd2a46a1.jpg'


def compare_target_hist(image_hist):
    target_files = gen_target()

    while True:
        try:
            target_file = target_files.__next__()
            im = cv2.imread(target_file, cv2.IMREAD_GRAYSCALE)
            target_hist = cv2.calcHist([im], [0], None, [256], [0, 256])
            yield (compare_hist(image_hist, target_hist), target_file)

        except StopIteration:
            break


# ヒストグラムを比較の計算をしている
def compare_hist(hist1, hist2):
    total = 0
    for i in range(len(hist1)):
        total += min(hist1[i], hist2[i])
    return float(total) / sum(hist1)


if __name__ == '__main__':
    for i in matching():
        print(i)
