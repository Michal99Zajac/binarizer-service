import cv2
import numpy as np
from aiortc import MediaStreamTrack
from av import VideoFrame
from skimage.filters import threshold_sauvola


class SauvolaBinarizerTrack(MediaStreamTrack):
    kind = "video"

    def __init__(self, track: MediaStreamTrack) -> None:
        super().__init__()
        self.track = track

    async def recv(self) -> VideoFrame:
        frame = await self.track.recv()

        # convert pyav to opencv
        img = frame.to_ndarray(format="bgr24")

        # prepare grayscale
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # apply sauvola thresholding
        sauvola = threshold_sauvola(img_gray, window_size=15, k=0.2, r=128)
        img_binarized = img_gray > sauvola

        # transform binarized image back to uint8 type
        img_binarized = img_binarized.astype(np.uint8) * 255

        # add a color dimension
        img_binarized_3ch = cv2.cvtColor(img_binarized, cv2.COLOR_GRAY2BGR)

        # rebuild a VideoFrame, preserving timing information
        new_frame = VideoFrame.from_ndarray(img_binarized_3ch, format="bgr24")
        new_frame.pts = frame.pts
        new_frame.time_base = frame.time_base

        return new_frame
