#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, cv2
from typing import Any
from argparse import ArgumentParser
from collections import deque
from tqdm import tqdm
from termcolor import colored


class MotionExtracter:
    def __init__(self, video_path: str, frame_offset: int, *, grayscale: bool = True, no_console: bool = True, preview_video: bool = False) -> None:
        self.video_path = video_path
        self.frame_offset = frame_offset
        self.grayscale = grayscale
        self.no_console = no_console
        self.preview_video = preview_video

        self.PREVIEW_WINDOW_TITLE = "Press 'Q' to exit the preview" 

    
    def next_frame(self, video: cv2.VideoCapture) -> tuple[bool, Any]:
        """Gets the next frame from a video"""
        
        ret, frame = video.read()
        if self.grayscale:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return ret, frame


    def debug(self, string: str) -> None:
        """Print function that prints if no_console is disabled"""
        
        if not self.no_console:
            print(string)


    def get_motion_frame(self, frame1: Any, frame2: Any) -> Any:
        """Gets the motion frame between two frames"""

        processed = cv2.bitwise_not(cv2.add(frame1, cv2.bitwise_not(frame2)))
        return processed


    def save(self, out_path: str) -> None:
        """Processes the video and saves it into the out_path"""

        video = cv2.VideoCapture(self.video_path)

        fps = int(video.get(cv2.CAP_PROP_FPS))
        num_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = int(video.get(cv2.CAP_PROP_FOURCC))

        if self.frame_offset > num_frames:
            raise ValueError(f"Frame offset ({self.frame_offset}) must be < the number of frames in the video ({num_frames})")

        out = cv2.VideoWriter(
            out_path,
            fourcc,
            fps,
            (width, height),
            0 if self.grayscale else None)

        # Create queue of frames to offset the negative
        inverted_queue = deque()
        while len(inverted_queue) < self.frame_offset:
            _, frame = self.next_frame(video)
            inverted_queue.append(frame)

        # Process video
        self.debug(f"{colored('Processing', 'light_blue')} {colored(':', 'grey')} {os.path.abspath(self.video_path)}")

        frame_idxs = range(0, num_frames - self.frame_offset)
        for _ in tqdm(frame_idxs) if not self.no_console else frame_idxs:
            ret, frame = self.next_frame(video)
            if not ret: break
            
            processed = self.get_motion_frame(frame, inverted_queue.popleft())
            inverted_queue.append(frame)
            out.write(processed)

            if self.preview_video:
                cv2.imshow(self.PREVIEW_WINDOW_TITLE, processed)
                if cv2.waitKey(1) == ord("q"): 
                    self.preview_video = False
                    cv2.destroyWindow(self.PREVIEW_WINDOW_TITLE)

        self.debug(f"{colored('Saved in', 'green')} {colored(':', 'grey')} {os.path.abspath(out_path)}")

        video.release()
        out.release()


def main() -> None:
    """Used for the CLI"""

    parser = ArgumentParser()
    parser.add_argument(
        'video_path',
        help="The path to the video to process")
    parser.add_argument(
        '-o', 
        '--frame-offset', 
        type=int, 
        required=True, 
        help="The number of frames to delay the negative by. Larger offsets will track slower motion more effectively and vice versa.")
    parser.add_argument(
        '--out', 
        help="The path to store the output file in")
    parser.add_argument(
        '--color', 
        action='store_true', 
        help="Doesn't convert to output to grayscale. (About half as fast as normal)")
    parser.add_argument(
        '--no-console', 
        action='store_true',
        help="If set, the program will not print to the console")
    parser.add_argument(
        '--preview-video', 
        action='store_true',
        help="If set, displays a preview of the video as it is rendered. This will slow the rendering down a little bit")
    args = parser.parse_args()

    path = os.path.splitext(args.video_path)[0]  # remove extension
    out_path = args.out or f"{path}-frame-offset-{args.offset}.mp4"

    MotionExtracter(
        args.video_path, 
        args.frame_offset, 
        grayscale=not args.color,
        no_console=args.no_console,
        preview_video=args.preview_video
    ).save(out_path)


if __name__ == "__main__":
    main()
