import json
import os

import cv2
from aiohttp import web
from aiortc import MediaStreamTrack, RTCPeerConnection, RTCSessionDescription
from av import VideoFrame

ROOT = os.path.dirname(__file__)
PUBLIC = os.path.join(ROOT, "..", "public")


class EchoTrack(MediaStreamTrack):
    """
    A MediaStreamTrack that echoes the frames from another track.
    """

    kind = "video"

    def __init__(self, track: VideoFrame) -> None:
        super().__init__()  # don't forget to call super()
        self.track = track

    async def recv(self) -> VideoFrame:
        frame = await self.track.recv()

        # Convert the frame to a numpy array
        img = frame.to_ndarray(format="bgr24")

        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Apply adaptive binarization
        binarized = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2
        )

        # Convert the binarized image back to a VideoFrame
        frame = VideoFrame.from_ndarray(binarized, format="gray")

        return frame


async def index(request: web.Request) -> web.Response:
    content = open(os.path.join(PUBLIC, "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def offer(request: web.Request) -> web.Response:
    params = await request.json()

    # Create an offer
    offer = RTCSessionDescription(sdp=params["sdp"], type=params["type"])

    pc = RTCPeerConnection()

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange() -> None:
        print("ICE connection state is %s" % pc.iceConnectionState)
        if pc.iceConnectionState == "failed":
            await pc.close()

    @pc.on("track")
    def on_track(track: VideoFrame) -> None:
        print("Track %s received" % track.kind)

        if track.kind == "video":
            pc.addTrack(EchoTrack(track))

        @track.on("ended")
        async def on_ended() -> None:
            print("Track %s ended" % track.kind)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return web.Response(
        content_type="application/json",
        text=json.dumps({"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}),
    )


async def handle_options(request: web.Request) -> None:
    return web.Response(text="ok")


app = web.Application()


app.router.add_route("OPTIONS", "/offer", handle_options)
app.router.add_post("/offer", offer)
app.router.add_get("/", index)

web.run_app(app, host="127.0.0.1", port=8000)
