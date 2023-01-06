import imageio.v3 as imageiov3
import imageio.v2 as imageiov2

from PIL import Image

import glob
import math

import args_parser


def init_writer(path: str, fps: int, **kwargs):
    """Init general mp4 writer

    Args:
        path (str): path to mp4 file.
        fps (int): FPS for video.

    Returns:
        Writer: FFMPEG writer.
    """
    return imageiov2.get_writer(
        path,
        fps=fps,
        format='FFMPEG',
        macro_block_size=None,
        ** kwargs
    )


def get_durations(gif: Image) -> list[int]:
    """Get a list of frame durations

    Args:
        gif (Image): GIF image.

    Returns:
        list[int]: A list of duration (ms).
    """
    assert gif.format == 'GIF'

    gif.seek(0)  # move to the start of the gif, frame 0
    durations = []
    # run a while loop to loop through the frames
    while True:
        try:
            # returns current frame duration in milli sec.
            frame_duration = gif.info['duration']
            durations.append(frame_duration)
            # now move to the next frame of the gif
            gif.seek(gif.tell() + 1)  # image.tell() = current frame
        except EOFError:
            # Return the lcm of all durations
            return durations


def get_gif_repeats(gif: Image) -> tuple[int, list[int]]:
    """Create an array of times frames should be repeat to sync under 1 FPS.

    Args:
        gif (Image): Image of type gif.

    Returns:
        tuple(int, list[int]): 
        - First element is GCD of frames duration, which is the duration that all frames should be after repeat.
        - Second element is list of times that each frame should repeat.
    """
    frame_durations = get_durations(gif)
    frame_duration_gcd = math.gcd(*frame_durations)
    frame_repeats = [int(duration/frame_duration_gcd)
                     for duration in frame_durations]

    return frame_duration_gcd, frame_repeats


def gif_to_mp4(gif_path: str, loop: int) -> None:
    """Convert GIF to MP4

    Args:
        gif_path (str): path to gif
    """
    pil_image = Image.open(gif_path)
    frame_duration, frame_repeate_times = get_gif_repeats(pil_image)
    fps = int(1000/frame_duration)

    gif = imageiov3.imread(gif_path)

    mp4_filepath = gif_path.rstrip('.gif') + '.mp4'
    writer = init_writer(mp4_filepath, fps)

    for _ in range(loop):
        for frame_index, frame in enumerate(gif):
            repeate_times = frame_repeate_times[frame_index]

            for _ in range(repeate_times):
                writer.append_data(frame)
    pass


if __name__ == "__main__":
    args = args_parser.args

    for gif_path in glob.glob(args.path):
        print(f'Converting {gif_path}')
        gif_to_mp4(gif_path, args.loop)
    pass
