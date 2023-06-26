import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, RTCIceCandidate
import websockets
import json

# Define a BYE constant
BYE = "BYE"


class Signaling:
    def __init__(self, url):
        self.url = url
        self.websocket = None

    async def connect(self):
        self.websocket = await websockets.connect(self.url)

    async def disconnect(self):
        if self.websocket is not None:
            await self.websocket.close()

    async def send(self, data):
        if self.websocket is not None:
            await self.websocket.send(json.dumps(data))
        else:
            raise ConnectionError("Not connected to a WebSocket.")

    async def receive(self):
        if self.websocket is not None:
            msg = await self.websocket.recv()
            return json.loads(msg)
        else:
            raise ConnectionError("Not connected to a WebSocket.")


class VideoTransformTrack(VideoStreamTrack):
    def __init__(self, track):
        super().__init__()  # don't forget this!
        self.track = track

    async def recv(self):
        frame = await self.track.recv()

        # simply pass the same frame forward
        return frame


async def consume_signaling(pc, signaling):
    while True:
        obj = await signaling.receive()

        if isinstance(obj, dict):
            if "sdp" in obj and "type" in obj:
                await pc.setRemoteDescription(RTCSessionDescription(**obj))

                if obj["type"] == "offer":
                    # send answer
                    answer = await pc.createAnswer()
                    await pc.setLocalDescription(answer)
                    await signaling.send(
                        {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}
                    )
            elif "candidate" in obj:
                candidate = RTCIceCandidate(**obj["candidate"])
                await pc.addIceCandidate(candidate)
            elif obj == BYE:
                print("Exiting")
                break


async def run(pc, signaling):
    @pc.on("track")
    def on_track(track):
        print("Track %s received" % track.kind)
        if track.kind == "video":
            local_video = VideoTransformTrack(track)
            pc.addTrack(local_video)

    await consume_signaling(pc, signaling)


async def main():
    pc = RTCPeerConnection()

    signaling = Signaling("ws://localhost:8000")
    await signaling.connect()

    try:
        await run(pc, signaling)
    finally:
        await pc.close()
        await signaling.disconnect()


asyncio.run(main())
