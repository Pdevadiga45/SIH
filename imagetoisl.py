
import os
import time
import cv2
from paddleocr import PaddleOCR
from PIL import Image

# Example path for all media files
MEDIA_DIR = "C:\\Users\HP\\Downloads\\INDIAN SIGN LANGUAGE ANIMATED VIDEOS\\"

# Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')  # Set language to English

def preprocess_text(text):
    """Preprocess the input text by capitalizing the first letter and removing punctuation."""
    text = text.lower().strip()
    words = text.split()
    # Capitalize the first letter of each word
    words = [word.capitalize() for word in words]
    return words
    
def media_exists(media_name):
    """Check if the media file exists in the dataset."""
    file_path = os.path.join(MEDIA_DIR, f"{media_name}.mp4")
    exists = os.path.isfile(file_path)
    print(f"Checking for {file_path}: {'Exists' if exists else 'Not Found'}")  # Add this line
    return exists

def display_video(video_path):
    """Play a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def detect_text(image_path):
    """Detect and recognize text in an image using PaddleOCR."""
    result = ocr.ocr(image_path, cls=True)  # Perform OCR on the image
    detected_text = []

    for line in result:
        for word_info in line:
            text = word_info[1][0]  # Extract recognized text
            detected_text.append(text)

    return ' '.join(detected_text)

def process_text(text):
    words = preprocess_text(text)
    media_sequence = []  # List to hold the sequence of media to display

    for word in words:
        if media_exists(word):  # Check if the word exists in the dataset
            media_sequence.append(os.path.join(MEDIA_DIR, f"{word}.mp4"))  # Add video path to sequence
        else:
            # Break down the word into individual letters and capitalize them
            capitalized_letters = [letter.upper() for letter in word]
            for letter in capitalized_letters:
                if media_exists(letter):  # Check for individual letter videos
                    media_sequence.append(os.path.join(MEDIA_DIR, f"{letter}.mp4"))  # Add letter video path to sequence
                else:
                    print(f"Letter '{letter}' not found in media dataset.")

    # Display the media in the correct sequence
    for media in media_sequence:
        print(f"Displaying: {media}")  # Log the media being displayed
        display_video(media)  # Call function to play video
        time.sleep(2)  # Add a delay of 2 seconds between displays

# Example usage for image input
image_input_path = "C:\\Users\\HP\\Downloads\\sign_text.png"
detected_text = detect_text(image_input_path)
process_text(detected_text)
