import cv2, ntpath
from argparse import ArgumentParser
from collections import deque

def main():
    parser = ArgumentParser()
    parser.add_argument('filepaths', nargs='+')
    parser.add_argument('-o', '--offset', type=float, required=True)
    parser.add_argument('--out')
    args = parser.parse_args()

    for filepath in args.filepaths:
        video = cv2.VideoCapture(filepath)

        fps = int(video.get(cv2.CAP_PROP_FPS))
        numFrames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        invertedFrameDelay = int(args.offset * fps)

        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

        outpath = ""
        if args.out:
            if len(args.filepaths) > 1:
                filename = ntpath.basename(filepath)
                outpath = ntpath.join(args.out, filename)
            else:
                outpath = args.out
        else:
            filenameNoExt = ntpath.basename(ntpath.splitext(filepath)[0])
            filedir = ntpath.dirname(filepath)
            outpath = ntpath.join(filedir, f"{filenameNoExt}-motion-extraction-offset-{args.offset}.mp4")

        out = cv2.VideoWriter(
            outpath,
            cv2.VideoWriter_fourcc(*'avc1'),
            fps,
            (width, height)
        )

        invertedQueue = deque()
        while len(invertedQueue) < invertedFrameDelay:
            _, frame = video.read()
            invertedQueue.append(frame)


        i = 0
        while True:
            ret, frame = video.read()
            if not ret: break

            print(f"Processing frame {i}")
            inverted = cv2.bitwise_not(invertedQueue.popleft())
            invertedQueue.append(frame)
            frame = cv2.bitwise_not(cv2.add(frame, inverted))
            out.write(frame)

            i += 1

        video.release()
        out.release()
    


if __name__ == "__main__":
    main()