#!/usr/bin/env python3
"""
Generate an ArUco marker PNG ready to print.
OpenCV 4.6.0 (legacy API).

Run:  python3 generate_marker.py
Then: print marker_0.png. Measure the printed BLACK square edge in mm
      (whole marker, border included) -> you'll need it for pose later.
"""
import cv2

DICT      = cv2.aruco.DICT_4X4_50   # 4x4 bits: robust at distance / low-res / motion blur
MARKER_ID = 0
SIZE_PX   = 800                     # high-res so the print stays crisp

aruco_dict = cv2.aruco.Dictionary_get(DICT)
img = cv2.aruco.drawMarker(aruco_dict, MARKER_ID, SIZE_PX)
out = f"marker_{MARKER_ID}.png"
cv2.imwrite(out, img)
print(f"Saved {out}  (dict=DICT_4X4_50, id={MARKER_ID}, {SIZE_PX}px)")
print("Tip: print it big (>=10cm edge) and glue it on something rigid/flat.")
