let pc = null;

async function start() {
    const config = {'iceServers': [{'urls': 'stun:stun.l.google.com:19302'}]};

    // create the RTCPeerConnection object
    pc = new RTCPeerConnection(config);

    // get the media stream from the webcam
    const mediaStream = await navigator.mediaDevices.getUserMedia({video: true, audio: false});

    // add the stream's tracks to the connection
    mediaStream.getTracks().forEach(track => pc.addTrack(track, mediaStream));

    // when we get the remote track, add it to the video element
    pc.ontrack = function (event) {
        const videoElement = document.querySelector('video');
        videoElement.srcObject = event.streams[0];
    };

    // create an offer and set it as the local description
    let offer = await pc.createOffer();
    await pc.setLocalDescription(offer);

    // send the offer to the server
    const response = await fetch('/offer', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({'sdp': pc.localDescription.sdp, 'type': pc.localDescription.type}),
    });

    // get the answer from the server and set it as the remote description
    const responseData = await response.json();
    await pc.setRemoteDescription(new RTCSessionDescription(responseData));
}

// start the connection when the page loads
window.onload = start;
