import cv2
import argparse
import numpy as np
import csv
import os

class FaceDetector:
    def __init__(self, face_model, face_proto, age_model, age_proto, gender_model, gender_proto):
        self.face_net = cv2.dnn.readNet(face_model, face_proto)
        self.age_net = cv2.dnn.readNet(age_model, age_proto)
        self.gender_net = cv2.dnn.readNet(gender_model, gender_proto)
        
        self.model_mean_values = (92.1263377603, 87.7689143744, 71.695847746)
        self.age_list = [
            '(0-2)', '(3-5)', '(6-8)', '(9-11)', '(12-14)', '(15-17)', '(18-20)', '(21-23)',
            '(24-26)', '(27-29)', '(30-32)', '(33-35)', '(36-38)', '(39-41)', '(42-44)', '(45-47)',
            '(48-50)', '(51-53)', '(54-56)', '(57-59)', '(60-62)', '(63-65)', '(66-68)', '(69-71)',
            '(72-74)', '(75-77)', '(78-80)', '(81-83)', '(84-86)', '(87-89)', '(90-92)', '(93-95)',
            '(96-98)', '(99-100)'
        ]
        self.gender_list = ['Male', 'Female']

    def highlight_faces(self, frame, conf_threshold=0.7):
        frame_copy = frame.copy()
        frame_height, frame_width = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(frame_copy, 1.0, (300, 300), [104, 117, 123], True, False)
        
        self.face_net.setInput(blob)
        detections = self.face_net.forward()
        
        face_boxes = []
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > conf_threshold:
                x1 = int(detections[0, 0, i, 3] * frame_width)
                y1 = int(detections[0, 0, i, 4] * frame_height)
                x2 = int(detections[0, 0, i, 5] * frame_width)
                y2 = int(detections[0, 0, i, 6] * frame_height)
                face_boxes.append([x1, y1, x2, y2])
                cv2.rectangle(frame_copy, (x1, y1), (x2, y2), (0, 255, 0), int(round(frame_height / 150)), 8)
        return frame_copy, face_boxes

    def analyze_face(self, face):
        blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), self.model_mean_values, swapRB=True, crop=False)
        
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = self.gender_list[gender_preds[0].argmax()]
        
        self.age_net.setInput(blob)
        age_preds = self.age_net.forward()
        age = self.age_list[age_preds[0].argmax()]
        
        return gender, age[1:-1]

def parse_arguments():
    parser = argparse.ArgumentParser(description="Detect age and gender from images or video")
    parser.add_argument('--image', type=str, help="Path to the image or video file")
    return parser.parse_args()

def resize_image(image, width, height):
    return cv2.resize(image, (width, height))

def main():
    args = parse_arguments()
    
    face_proto = "opencv_face_detector.pbtxt"
    face_model = "opencv_face_detector_uint8.pb"
    age_proto = "age_deploy.prototxt"
    age_model = "age_net.caffemodel"
    gender_proto = "gender_deploy.prototxt"
    gender_model = "gender_net.caffemodel"
    
    detector = FaceDetector(face_model, face_proto, age_model, age_proto, gender_model, gender_proto)
    
    video_source = args.image if args.image else 0
    video = cv2.VideoCapture(video_source)
    
    if not video.isOpened():
        print("[!] Error Could not open video source.")
        return
    
    padding = 20
    target_width, target_height = 1000, 900

    save_to_csv = input("Do you want to save results to a CSV file? (yes/no): ").strip().lower()
    if save_to_csv == 'yes':
        csv_filename = input("Enter the CSV file name: ").strip()
        csv_alias = input("Enter an alias for the image (optional): ").strip()
        
        csv_exists = os.path.exists(csv_filename)
        with open(csv_filename, 'a', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            if not csv_exists:
                csv_writer.writerow(['Alias', 'Gender', 'Age'])
    
    while True:
        has_frame, frame = video.read()
        if not has_frame:
            print("No frame available or video ended.")
            break
        
        result_img, face_boxes = detector.highlight_faces(frame)
        
        if not face_boxes:
            print("[!] No face detected")
        
        for face_box in face_boxes:
            x1, y1, x2, y2 = face_box
            face = frame[max(0, y1-padding):min(y2+padding, frame.shape[0]-1),
                         max(0, x1-padding):min(x2+padding, frame.shape[1]-1)]
            
            if face.size == 0:
                continue
            
            gender, age = detector.analyze_face(face)
            print(f'[*] Gender: {gender}')
            print(f'[*] Age: {age} years')
            
            text = f'{gender}, {age}'
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
            text_w, text_h = text_size
            cv2.rectangle(result_img, (x1, y1 - text_h - 10), (x1 + text_w, y1), (0, 255, 255), -1)
            cv2.putText(result_img, text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
            
            if save_to_csv == 'yes':
                with open(csv_filename, 'a', newline='') as csvfile:
                    csv_writer = csv.writer(csvfile)
                    csv_writer.writerow([csv_alias, gender, age])
    
        resized_img = resize_image(result_img, target_width, target_height)
        cv2.imshow("[+] Detecting Age and Gender", resized_img)
        key = cv2.waitKey(0)
        if key == ord('q'):
            break
    
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
