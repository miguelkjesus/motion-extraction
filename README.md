# Motion Exctrator

Inspried by [this video](https://www.youtube.com/watch?v=NSS6yAMZF78)

**WORKS BEST WITH STILL IMAGES**

## Examples

Intersection Source Video

[![Source Video](https://img.youtube.com/vi/vpFrzhFYbO4/maxresdefault.jpg)](https://youtu.be/vpFrzhFYbO4)

Motion Extracted (frame offset = 1)

[![Motion Extracted](https://img.youtube.com/vi/_lSy4VmjS8A/maxresdefault.jpg)](https://youtu.be/_lSy4VmjS8A)

(Notice how the still cars are invisible until they start moving)

## Setup

1. Clone this repository.
2. Install all the required dependencies by opening a terminal inside the cloned directory, and executing the following command:

```powershell
pip install -r REQUIREMENTS.txt
```

## Usage

```
py extract_motion.py VIDEO_PATH -o FRAME_OFFSET [--out OUT] [--color] [--no-console] [--preview-video]
```

Positional Arguments

- `VIDEO_PATH` **REQUIRED** The path to the video to process

Options

- `-o FRAME_OFFSET` **REQUIRED** The number of frames to delay the negative by. Larger offsets will track slower motion more effectively and vice versa.
- `--out OUT` **REQUIRED** The path to save the processed video.
- `--color` If set, output videos will keep their color, rather than be converted to grayscale. This will roughly double rendering times.
- `--no-console` If set, the program will not print to the console.
- `--preview-video` If set, displays a preview of the video as it is rendered. This will slow the rendering down a little bit.
