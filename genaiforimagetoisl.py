import os
from PIL import Image
import cv2  # Import OpenCV for video playback
import time  # Import time for adding delays
from transformers import BlipProcessor, BlipForConditionalGeneration

# Example paths (replace with actual paths)
MEDIA_DIR = 'C:\\Users\\HP\\Downloads\\INDIAN SIGN LANGUAGE ANIMATED VIDEOS\\'  # Path for all media files

def preprocess_text(text):
    """Preprocess the input text by lowercasing and removing punctuation."""
    text = text.lower().strip()
    # For simplicity, we remove punctuation and split by spaces
    words = text.split()
    return words

def media_exists(media_name):
    """Check if the media file exists in the dataset."""
    return os.path.isfile(os.path.join(MEDIA_DIR, f"{media_name}.mp4"))

def lookup_alphabet(letter):
    """Get the first image path for a given letter."""
    letter_dir = os.path.join(MEDIA_DIR, letter.upper())  # Path to the letter's folder
    if os.path.exists(letter_dir):
        images = [img for img in os.listdir(letter_dir) if img.endswith('.jpg')]  # List all jpg images
        if images:
            return os.path.join(letter_dir, images[0])  # Return the first image path
    return None  # Return None if no images found

def display_video(video_path):
    """Play a video using OpenCV."""
    cap = cv2.VideoCapture(video_path)  # Open the video file

    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()  # Read a frame from the video
        if not ret:
            break  # Exit if no frames are left

        cv2.imshow('Video', frame)  # Display the frame

        if cv2.waitKey(25) & 0xFF == ord('q'):  # Exit on 'q' key press
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows

def display_image(image_path):
    """Display an image using PIL."""
    img = Image.open(image_path)  # Open the image file
    img.show()  # Display the image

def process_text(text):
    words = preprocess_text(text)
    media_sequence = []  # List to hold the sequence of media to display

    for word in words:
        if media_exists(word):  # Check if the word exists in the dataset
            media_sequence.append(os.path.join(MEDIA_DIR, f"{word}.mp4"))  # Add video path to sequence
        else:
            # Break down the word into individual letters
            for letter in word:
                if media_exists(letter):  # Check for individual letter videos
                    media_sequence.append(os.path.join(MEDIA_DIR, f"{letter}.mp4"))  # Add letter video path to sequence
                else:
                    print(f"Letter '{letter}' not found in media dataset.")

    # Display the media in the correct sequence
    for media in media_sequence:
        print(f"Displaying: {media}")  # Log the media being displayed
        if media.endswith('.mp4'):
            display_video(media)  # Call function to play video
        
        time.sleep(0.7)  # Add a delay of 2 seconds between displays

def describe_image(image_path):
    """Generate a caption for an image using BLIP."""
    # Load the processor and model
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

    # Load and preprocess the image
    image = Image.open(image_path).convert("RGB")

    # Process the image and generate a caption
    inputs = processor(images=image, return_tensors="pt")
    out = model.generate(**inputs)
    description = processor.decode(out[0], skip_special_tokens=True)

    return description

if __name__ == "__main__":
    # Specify the image path directly here
    image_path = "C:\\Users\\HP\\Downloads\\bird.png"
    
    # Step 1: Generate description from the image
    description = describe_image(image_path)
    print("Generated Description:", description)
    
    # Step 2: Process the generated description into ISL
    process_text(description)
