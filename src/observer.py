import time
import mss
from PIL import Image, ImageChops, ImageStat


CHANGE_THRESHOLD = 5.0
COMPARE_SIZE = (160, 90)


def capture_screen():
    with mss.MSS() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)

        image = Image.frombytes(
            "RGB",
            screenshot.size,
            screenshot.rgb
        )

        return image


def get_change_score(previous, current):
    # Make the images much smaller before comparing them.
    # This makes the comparison cheaper.
    previous_small = previous.resize(COMPARE_SIZE).convert("L")
    current_small = current.resize(COMPARE_SIZE).convert("L")

    difference = ImageChops.difference(
        previous_small,
        current_small
    )

    # Average pixel difference from 0 to 255
    score = ImageStat.Stat(difference).mean[0]

    return score


previous = None

while True:
    latest = capture_screen()

    if previous is not None:
        score = get_change_score(previous, latest)

        print(f"Change score: {score:.2f}")

        if score >= CHANGE_THRESHOLD:
            print(">>> SIGNIFICANT SCREEN CHANGE")
        else:
            print("No significant change")

    latest.save("../data/screenshots/latest.png")

    previous = latest

    time.sleep(0.5)