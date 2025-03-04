import cv2
import copy


def changes(base_frame, current_frame, threshold):
    base_gray = cv2.cvtColor(base_frame, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
    diff = cv2.absdiff(base_gray, current_gray)
    _, mask = cv2.threshold(diff, threshold, 255, cv2.THRESH_BINARY)
    out = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    return out 


def inverted(base_frame, current_frame):
    inverted_frame = 255 - current_frame
    blended_frame = cv2.addWeighted(inverted_frame, 0.2, base_frame, 0.2, 0)
    return blended_frame


def shift(input_file, frames=10):
    cap = cv2.VideoCapture(input_file)
    output = []
    queue = []
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        queue.append(frame)

        if i < frames:
            i += 1
            continue

        base_frame = queue.pop(0)
        inverted_frame = inverted(base_frame, frame)
        output.append(inverted_frame)

    cap.release()
    return output


def difference(input_file, threshold=20):
    cap = cv2.VideoCapture(input_file)
    output = []
    original = None
    i = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if i == 0:
            original = copy.deepcopy(frame)
            i = 1
            continue

        diff = changes(original, frame, threshold)
        output.append(diff)

    cap.release()
    return output


def main(input_file, output_file, frames=10, threshold=20, mode='shift'):
    print("Processing file...")
    cap = cv2.VideoCapture(input_file)

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()

    if frames > frame_count:
        print("Invalid input parameters!")
        return None

    if mode == 'shift':
        output = shift(input_file, frames)
    elif mode == 'diff':
        output = difference(input_file, threshold)
    else:
        print("Invalid Mode!")
        return None

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))
    for frame in output:
        out.write(frame)

    out.release()
    print("Finished Processing")


if __name__ == '__main__':
    INPUT_FILE = "./Videos/ants.mp4"
    OUTPUT_FILE = "Output/output.mp4"
    FRAMES = 20
    THRESHOLD = 50
    MODE = 'diff'
    
    main(
        INPUT_FILE,
        OUTPUT_FILE,
        FRAMES,
        THRESHOLD,
        MODE
    )