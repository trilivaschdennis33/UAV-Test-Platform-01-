# TP01 — Autonomous Ops · Build Log

Autonomous precision-landing loop on a quadcopter using an onboard companion
computer for ArUco-marker vision. Vision runs on a Raspberry Pi (Camera Module 3);
control runs on a Pixhawk 6C mini flashed with ArduCopter. The Pi detects the
marker, computes the offset, and feeds `LANDING_TARGET` MAVLink messages to the
flight controller's precision-landing (PLND) subsystem.

**Stack:** Python · OpenCV 4.6.0 (legacy ArUco API) · picamera2 · pymavlink · ArduPilot

---

## Milestones

| #  | Milestone                                              | Status   |
|----|--------------------------------------------------------|----------|
| M0 | Airframe / Tinkerbell (TBELL) integration (Pixhawk, TELEM2)    | ☐        |
| M1 | Bench vision pipeline — detect ArUco, output offsets   |  Done  |
| M2 | Camera calibration — pixels → real-world angles        |  Next  |
| M3 | MAVLink link — send LANDING_TARGET to Pixhawk (bench)  | ☐        |
| M4 | Precision Loiter — hold over marker in flight          | ☐        |
| M5 | Precision Land — autonomous landing + error logging    | ☐        |
| M6 | Full autonomous loop — mission → land → self-charging dock | ☐     |

---

## M1 — Bench vision pipeline ✅ · 2026-07-19

**Goal:** Prove ArUco detection end-to-end on the companion computer, no aircraft
required. Output the marker's pixel offset from the frame centre in real time.

**Hardware**
- Raspberry Pi `<MODEL — fill in>`
- Raspberry Pi Camera Module 3 (Sony IMX708, autofocus), CSI ribbon

**Software**
- OpenCV 4.6.0 — verified `cv2.__version__ == "4.6.0"`, `cv2.aruco` present
- picamera2 for CSI capture
- Marker: `DICT_4X4_50`, ID 0, printed ≥10 cm on a rigid flat mount

**What I did**
1. Verified OpenCV + ArUco module on the Pi.
2. Generated the marker (`generate_marker.py`).
3. Wrote a headless detection loop (`detect_bench.py`): capture → grayscale →
   `detectMarkers` → print ID + centre + offset-from-centre (px).
4. Recorded an annotated demo (`detect_record.py`) → `detection_demo.mp4`.

**Result**
- Stable detection of ID 0; centre and offset track smoothly across the frame.
- Marker re-acquires cleanly after leaving and re-entering the frame.
- Demo video captured for portfolio.

**Key learnings / gotchas**
- **OpenCV 4.6.0 uses the *legacy* ArUco API** (`Dictionary_get`,
  `DetectorParameters_create`, `detectMarkers(img, dict, parameters=…)`).
  Most online tutorials target 4.7+ and crash on 4.6.0.
- The camera is a **Module 3 (IMX708)**, not a V2 (IMX219) — it has autofocus,
  which must be locked to a fixed focus before flight to avoid focus-hunting blur
  during descent (handled in a later milestone).
- Detection quality is gated by **lighting** and **motion blur**, not by code.
- Offsets here are in **pixels**, not angles. The flight controller needs
  *angular* offsets → that conversion requires camera calibration (M2).

**Next:** M2 — camera calibration to obtain the camera matrix and distortion
coefficients, turning pixel offsets into real angular offsets.

---

## M2 — Camera calibration ⏳
*(in progress — notes go here)*

