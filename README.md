# Binarizer Service

This Python project uses WebRTC technology to stream video between a browser and a server, applying a Sauvola binarization algorithm to the video on the server side.

## Core Functionality

The core functionality of this project is as follows:

1. The client connects to the server and sends its video stream using WebRTC.
2. The server receives the stream and applies the Sauvola binarization algorithm to the frames in real time.
3. The transformed video is then sent back to the client and displayed in the browser.

This process is facilitated using the aiohttp and aiortc Python libraries on the server side, and WebRTC on the client side.

## Sauvola Binarization

Sauvola binarization is an image processing method that applies a local thresholding algorithm to an image. This technique is particularly useful in scenarios where the image has different lighting conditions in different areas.

In this project, Sauvola binarization is applied to the video frames on the server side, transforming the original video stream in real time.

## Running the Project

Before running this project, make sure you have all the necessary dependencies installed. They are listed in the `pyproject.toml` file and can be installed using Poetry.

The server can be started by running `server.py` inside the `src` directory.

Once the server is running, you can open the client-side application in your browser by navigating to `localhost:8000`.

## Note

This project is for demonstration purposes and may not be ready for production use. It's recommended to add proper error handling and testing before using it in a production environment.
