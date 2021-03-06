# Program fetches traffic camera images from Digitraffic API repository and shows them
# sequentially from the point user chooses to the amount user chooses. Saves last checked
# image into a file and lets user continue from last checked image.

from urllib import request
from urllib import error
import numpy as np
import cv2

succes_count = 0
fail_count = 0


def show_image(url):
    resp = request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def main():
    last_value = 0
    counter = 0

    value = int(input("How many images: "))
    last = str(input("Continue from last? (y/n): "))

    if last == "y":
        try:
            file = open("last.txt", "r")
            last_value = int(file.read())
        except IOError:
            try:
                file = open("last.txt", "w")
            except IOError:
                raise IOError("FAILED TO ACCESS FILE " + "last.txt")
            file.flush()
            file.close()
        start = last_value
    else:
        start = int(input("Start image number (suggestion: 150000): "))

    time = int(input("Watching time per image (in milliseconds): "))

    print("Please wait a moment...")
    for i in range(start, 9999999):
        if counter >= value:
            last_value = i - 2
            break
        url = get_url(i)
        if url != "":
            img = show_image(url)
            cv2.imshow("Image", img)
            cv2.waitKey(time)
            counter += 1

    print()
    print("FAILS: ", end="")
    print(fail_count)
    print("SUCCESSES: ", end="")
    print(succes_count)

    try:
        file = open("last.txt", "w")
        file.flush()
        file.write(str(last_value))
        file.close()
    except IOError:
        raise IOError("FAILED TO ACCESS FILE " + "last.txt")

    return 0


def get_url(i):
    base = "https://weathercam.digitraffic.fi/"
    photoname = "C"
    jpg = ".jpg"

    name = ""
    i_str = str(i)
    if len(i_str) < 7:
        for j in range(0, 7 - len(i_str)):
            name += "0"
    name += i_str

    if len(name) != 7:
        print("NAME ERROR")
        return

    photo = photoname + name
    url = base + photo + jpg

    try:
        request.urlopen(url)
        print("URL SUCCESS: " + url)
        global succes_count
        succes_count += 1
        return url

    except error.HTTPError as e:
        global fail_count
        fail_count += 1
        return ""


main()
