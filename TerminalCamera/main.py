import ctypes
import cv2
import numpy as np
import sys
import time

from util import get_console_size

###############################################################################

##### General Config #####

MAX_ROWS = 30 # How tall each frame is, updated by the program when resized
MAX_COLS = 120 # How wide each frame is, updated by the program when resized

# You probably won't need to change this for monospaced fonts
CHAR_ASPECT = 2.0 # Approximate aspect ratio of character height to width

# ASCII characters to range from black to white pixels
# The length is not fixed--you can make these anything you want
ASCII_CHARS = " .:-=+*#%@"

###############################################################################

# Helper method, parses a frame from the MatLike object into an ascii frame
def parse_frame(frame: np.ndarray) -> str:
    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape

    # Adjust height
    effective_h = h / CHAR_ASPECT
    scale = min(MAX_ROWS / effective_h, MAX_COLS / w)

    # Calculate new width & height
    new_w, new_h = int(w * scale), int(h * scale / CHAR_ASPECT)

    # Get aspect ratio to determine rows/cols
    scaled_frame = cv2.resize(gray, (new_w, new_h), interpolation=cv2.INTER_AREA)

    # Convert to ASCII
    indices = (scaled_frame / 256 * len(ASCII_CHARS)).astype(int)
    indices = np.clip(indices, 0, len(ASCII_CHARS)-1)
    ascii_array = np.array(list(ASCII_CHARS))[indices]
    ascii_text = "\n".join("".join(row) for row in ascii_array)

    # ascii_text = ""
    # for r in range(new_h):
    #     for c in range(new_w):
    #         ascii_text += ASCII_CHARS[
    #             math.floor(scaled_frame[r, c] / 256 * len(ASCII_CHARS))
    #         ]
    #     ascii_text += "\n"

    return ascii_text

def main(feed_url: str):
    # 1. Open camera feed
    cap = cv2.VideoCapture(feed_url)

    if not cap.isOpened():
        print("Err: failed to open camera feed!")
        return

    # 2. Open new terminal window
    ctypes.windll.kernel32.FreeConsole()
    ctypes.windll.kernel32.AllocConsole()
    sys.stdout = open("CONOUT$", "w")
    sys.stderr = open("CONOUT$", "w")

    # 3. Read pixels
    last_resize_check = 0
    RESIZE_CHECK_INTERVAL = 0.25 # How often to poll for dimension changes
    while(True):
        try:
            # Get frame
            frame = cap.read()[1]

            # Show raw feed
            # cv2.imshow("frame", frame)
            # if cv2.waitKey(1) & 0xFF == ord("q"):
            #     break

            # Check dimensions
            now = time.time()
            if now - last_resize_check > RESIZE_CHECK_INTERVAL:
                global MAX_ROWS; global MAX_COLS
                MAX_ROWS, MAX_COLS = get_console_size()
                last_resize_check = now

            # Parse frame
            frame_ascii = parse_frame(frame)
            print("\033[2J\033[H", end="")
            print(frame_ascii, flush=True)
        except KeyboardInterrupt:
            print("Closing...")
            break

    # 4. Clean up
    cap.release()
    cv2.destroyAllWindows()
    ctypes.windll.kernel32.FreeConsole()

if __name__ == "__main__":
    main("http://129.161.212.227:4747/video")