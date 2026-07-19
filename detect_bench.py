#!/usr/bin/env python3
"""
Live ArUco detection on the bench. OpenCV 4.6.0 (legacy API).
Headless-safe: prints detected IDs + marker centre (px) to the terminal,
no display / X-server needed. This is the M1 checkpoint tool.

Run:  python3 detect_bench.py
Stop: Ctrl+C

Camera: set USE_PICAMERA below.
  False -> USB webcam (cv2.VideoCapture)
  True  -> Pi Camera via picamera2  (sudo apt install -y python3-picamera2)
"""
import cv2
import time

USE_PICAMERA = False   # <-- flip to True if you're on the Pi Camera ribbon module

# --- ArUco setup (legacy 4.6.0 API) ---
aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
params     = cv2.aruco.DetectorParameters_create()

# --- camera setup ---
if USE_PICAMERA:
    from picamera2 import Picamera2
    picam = Picamera2()
    picam.configure(picam.create_preview_configuration(
        main={"format": "RGB888", "size": (1280, 720)}))
    picam.start()
    time.sleep(1)
    get_frame = lambda: picam.capture_array()   # colour order is irrelevant, we go grayscale
else:
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Camera not found on index 0. Check `ls /dev/video*`.")
    def get_frame():
        ok, frame = cap.read()
        return frame if ok else None

print("Running. Move the marker in front of the camera. Ctrl+C to stop.\n")
try:
    while True:
        frame = get_frame()
        if frame is None:
            continue
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=params)

        if ids is not None:
            h, w = gray.shape
            for c, mid in zip(corners, ids.flatten()):
                cx, cy = c[0].mean(axis=0)          # marker centre in pixels
                dx = cx - w / 2                      # +right / -left of frame centre
                dy = cy - h / 2                      # +down  / -up   of frame centre
                print(f"ID {mid:>2}  centre=({cx:6.1f},{cy:6.1f})  "
                      f"offset_from_centre=({dx:+6.1f},{dy:+6.1f}) px")
        else:
            print("no marker", end="\r")
        time.sleep(0.03)                             # ~30 fps cap, keeps CPU sane
except KeyboardInterrupt:
    print("\nstopped")
