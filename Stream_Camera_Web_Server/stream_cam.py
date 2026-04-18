#!/usr/bin/env python3
import argparse
import os
import threading
import time
from datetime import datetime, timezone

import cv2
from flask import Flask, Response, jsonify

app = Flask(__name__)

state = {
    "started_at": datetime.now(timezone.utc),
    "frame_count": 0,
    "last_frame_at": None,
    "camera_opened": False,
    "capture_errors": 0,
    "driver": None,
    "requested_driver": None,
    "sensor_model": None,
    "width": None,
    "height": None,
    "fps": None,
}

frame_lock = threading.Lock()
latest_jpeg = None
stop_event = threading.Event()


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat()


def build_boundary_frame(jpeg_bytes: bytes) -> bytes:
    return (
        b"--frame\r\n"
        b"Content-Type: image/jpeg\r\n"
        + f"Content-Length: {len(jpeg_bytes)}\r\n\r\n".encode("ascii")
        + jpeg_bytes
        + b"\r\n"
    )


def _encode_jpeg(frame_bgr):
    encoded, jpeg = cv2.imencode(".jpg", frame_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 95])
    if not encoded:
        return None
    return jpeg.tobytes()


def _capture_loop_opencv(camera_index: int, width: int, height: int, fps: int):
    global latest_jpeg

    # Ép backend V4L2
    capture = cv2.VideoCapture(camera_index, cv2.CAP_V4L2)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, float(width))
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, float(height))
    capture.set(cv2.CAP_PROP_FPS, float(fps))

    state["camera_opened"] = capture.isOpened()
    if not state["camera_opened"]:
        state["capture_errors"] += 1
        print("[camera] Failed to open camera device. Check /dev/video0 permissions.")
        print("Try: sudo chmod 777 /dev/video0")
        return False

    state["driver"] = "opencv"
    state["sensor_model"] = "unknown"
    state["width"] = width
    state["height"] = height
    state["fps"] = fps

    frame_interval = 1.0 / max(1, fps)
    print(f"[camera] Camera opened (index={camera_index}, {width}x{height}@{fps}fps)")

    while not stop_event.is_set():
        ok, frame = capture.read()
        if not ok or frame is None:
            state["capture_errors"] += 1
            time.sleep(0.1)
            continue

        jpeg_bytes = _encode_jpeg(frame)
        if jpeg_bytes is None:
            state["capture_errors"] += 1
            continue

        with frame_lock:
            latest_jpeg = jpeg_bytes

        state["frame_count"] += 1
        state["last_frame_at"] = utc_now_iso()
        time.sleep(frame_interval)

    capture.release()
    state["camera_opened"] = False
    return True


def capture_loop(driver: str, camera_index: int, width: int, height: int, fps: int):
    state["requested_driver"] = driver
    # Hiện tại chỉ dùng OpenCV
    _capture_loop_opencv(camera_index, width, height, fps)


@app.route("/health", methods=["GET"])
def health():
    uptime_sec = int((datetime.now(timezone.utc) - state["started_at"]).total_seconds())
    return jsonify(
        {
            "status": "ok" if state["camera_opened"] else "degraded",
            "camera_opened": state["camera_opened"],
            "frame_count": state["frame_count"],
            "last_frame_at": state["last_frame_at"],
            "capture_errors": state["capture_errors"],
            "uptime_sec": uptime_sec,
        }
    )


@app.route("/stream.mjpg", methods=["GET"])
def stream_mjpeg():
    def generate():
        while not stop_event.is_set():
            with frame_lock:
                frame = latest_jpeg

            if frame is None:
                time.sleep(0.05)
                continue

            yield build_boundary_frame(frame)
            time.sleep(0.01)

    return Response(generate(), mimetype="multipart/x-mixed-replace; boundary=frame")


def parse_args():
    parser = argparse.ArgumentParser(description="Raspberry Pi MJPEG camera streamer")
    parser.add_argument("--host", default=os.getenv("CAMERA_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("CAMERA_PORT", "8080")))
    parser.add_argument("--fps", type=int, default=int(os.getenv("CAMERA_FPS", "20")))
    parser.add_argument("--width", type=int, default=int(os.getenv("CAMERA_WIDTH", "640")))
    parser.add_argument("--height", type=int, default=int(os.getenv("CAMERA_HEIGHT", "480")))
    parser.add_argument("--camera-index", type=int, default=int(os.getenv("CAMERA_INDEX", "0")))
    return parser.parse_args()


def main():
    args = parse_args()

    thread = threading.Thread(
        target=capture_loop,
        args=( "opencv", args.camera_index, args.width, args.height, args.fps),
        daemon=True,
    )
    thread.start()

    print(f"[camera] HTTP server listening on http://{args.host}:{args.port}")
    # host=0.0.0.0 để truy cập từ mạng LAN
    app.run(host=args.host, port=args.port, threaded=True)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
    finally:
        stop_event.set()
