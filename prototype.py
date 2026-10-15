import cv2
import mediapipe as mp
import math
import csv
import numpy as np
from scipy.signal import find_peaks, savgol_filter

test_path = 'backsquat1.mp4'
csv_path = 'backsquat_data.csv'

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def point(landmark):
    return(landmark.x, landmark.y)
def calculate_angle(a, b, c):

    angle = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    angle = abs(angle)
    if angle > 180:
        angle = 360 - angle
    return angle


pose = mp_pose.Pose(
    static_image_mode = False,
    model_complexity = 1,
    smooth_landmarks = True,
    min_detection_confidence = 0.5,
    min_tracking_confidence = 0.5
)

video = cv2.VideoCapture(test_path)
csv_file = open(csv_path, mode = 'w', newline = '', encoding = 'utf-8')
writer = csv.writer(csv_file)
fps = video.get(cv2.CAP_PROP_FPS)

header = [
    'frame',
    'timestamp',

    'left_shoulder_x',
    'left_shoulder_y',
    'left_elbow_x',
    'left_elbow_y',
    'left_wrist_x',
    'left_wrist_y',
    'left_hip_x',
    'left_hip_y',
    'left_knee_x',
    'left_knee_y',
    'left_ankle_x',
    'left_ankle_y',

    'right_shoulder_x',
    'right_shoulder_y',
    'right_elbow_x',
    'right_elbow_y',
    'right_wrist_x',
    'right_wrist_y',
    'right_hip_x',
    'right_hip_y',
    'right_knee_x',
    'right_knee_y',
    'right_ankle_x',
    'right_ankle_y',

    'left_elbow_angle',
    'right_elbow_angle',
    'left_shoulder_angle',
    'right_shoulder_angle',
    'left_hip_angle',
    'right_hip_angle',
    'left_knee_angle',
    'right_knee_angle',
]

writer.writerow(header)
frame_number = 0
def point(landmark):
    return(landmark.x, landmark.y)

all_rows = []

while True:
    ret, frame = video.read()
    if not ret:
        break

    frame_number += 1
    timestamp = frame_number / fps

    height, width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = pose.process(rgb_frame)

    if result.pose_landmarks:

        landmarks = result.pose_landmarks.landmark

        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = landmarks[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = landmarks[mp_pose.PoseLandmark.LEFT_WRIST]
        left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP]
        left_knee = landmarks[mp_pose.PoseLandmark.LEFT_KNEE]
        left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE]
        left_foot = landmarks[mp_pose.PoseLandmark.LEFT_FOOT_INDEX]

        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = landmarks[mp_pose.PoseLandmark.RIGHT_WRIST]
        right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP]
        right_knee = landmarks[mp_pose.PoseLandmark.RIGHT_KNEE]
        right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE]
        right_foot = landmarks[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX]

        left_shoulder_angle = calculate_angle(point(left_elbow), point(left_shoulder), point(left_hip))
        left_elbow_angle = calculate_angle(point(left_shoulder), point(left_elbow), point(left_wrist))
        left_hip_angle = calculate_angle(point(left_shoulder), point(left_hip), point(left_knee))
        left_knee_angle = calculate_angle(point(left_hip), point(left_knee), point(left_ankle))
        left_ankle_angle = calculate_angle(point(left_knee), point(left_ankle), point(left_foot))

        right_shoulder_angle = calculate_angle(point(right_elbow), point(right_shoulder), point(right_hip))
        right_elbow_angle = calculate_angle(point(right_shoulder), point(right_elbow), point(right_wrist))
        right_hip_angle = calculate_angle(point(right_shoulder), point(right_hip), point(right_knee))
        right_knee_angle = calculate_angle(point(right_hip), point(right_knee), point(right_ankle))
        right_ankle_angle = calculate_angle(point(right_knee), point(right_ankle), point(right_foot))

        row = [
            frame_number,
            timestamp,

            left_shoulder.x,
            left_shoulder.y,
            left_elbow.x,
            left_elbow.y,
            left_wrist.x,
            left_wrist.y,
            left_hip.x,
            left_hip.y,
            left_knee.x,
            left_knee.y,
            left_ankle.x,
            left_ankle.y,

            right_shoulder.x,
            right_shoulder.y,
            right_elbow.x,
            right_elbow.y,
            right_wrist.x,
            right_wrist.y,
            right_hip.x,
            right_hip.y,
            right_knee.x,
            right_knee.y,
            right_ankle.x,
            right_ankle.y,

            left_elbow_angle,
            right_elbow_angle,
            left_shoulder_angle,
            right_shoulder_angle,
            left_hip_angle,
            right_hip_angle,
            left_knee_angle,
            right_knee_angle,
        ]

        all_rows.append(row)

        left_part_angles = [f'Left shoulder: {left_shoulder_angle}',
                            f'Left elbow: {left_elbow_angle}',
                            f'Left hip: {left_hip_angle}',
                            f'Left knee: {left_knee_angle}',
                            f'Left ankle: {left_ankle_angle}']

        right_part_angles = [f'Right shoulder: {right_shoulder_angle}',
                            f'Right elbow: {right_elbow_angle}',
                            f'Right hip: {right_hip_angle}',
                            f'Right knee: {right_knee_angle}',
                            f'Right ankle: {right_ankle_angle}']

        for i, text in enumerate(left_part_angles):
            cv2.putText(frame, text + 'deg', (20, 30 + 30 * i), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3)

        for j, text in enumerate(right_part_angles):
            cv2.putText(frame, text + 'deg', (1200, 30 + 30 * j), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 0), 3)

        mp_drawing.draw_landmarks(
            frame,
            result.pose_landmarks,
            mp_pose.POSE_CONNECTIONS
        )

    cv2.imshow("Backsquat analysis", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

left_knee_idx = header.index("left_knee_angle")
right_knee_idx = header.index("right_knee_angle")

angles = np.array([(float(row[left_knee_idx]) + float(row[right_knee_idx])) / 2 for row in all_rows])

window = min(11, len(angles) if len(angles) % 2 else len(angles) - 1)
smooth_angles = savgol_filter(angles, window, 2)

min_distance = max(1, int(fps * 0.5))

bottoms, _ = find_peaks(
    -smooth_angles,
    distance = min_distance,
    prominence = 10
)

tops, _ = find_peaks(
    smooth_angles,
    distance = min_distance,
    prominence = 10
)

critical_indices = sorted(set(
    [0, len(all_rows) - 1]
    + bottoms.tolist()
    + tops.tolist()
))

with open("backsquat_data.csv", "w", newline = '', encoding = 'utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(header)

    for idx in critical_indices:
        writer.writerow(all_rows[idx])

video.release()
pose.close()
csv_file.close()
cv2.destroyAllWindows()