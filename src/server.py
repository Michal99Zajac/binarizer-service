import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, VideoStreamTrack, RTCIceCandidate
import websockets
import json

# Define a BYE constant
BYE = "BYE"


class Signaling:
    def __init__(self, websocket):
        self.websocket = websocket

    async def send(self, data):
        await self.websocket.send(json.dumps(data))

    async def receive(self):
        msg = await self.websocket.recv()
        return json.loads(msg)


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


async def handle_signaling(websocket, path):
    signaling = Signaling(websocket)
    pc = RTCPeerConnection()

    @pc.on("track")
    def on_track(track):
        print("Track %s received" % track.kind)
        if track.kind == "video":
            local_video = VideoTransformTrack(track)
            pc.addTrack(local_video)

    await consume_signaling(pc, signaling)


start_server = websockets.serve(handle_signaling, "127.0.0.1", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
