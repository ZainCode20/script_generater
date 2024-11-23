
import wave
import decimal
import math
import requests
import re
import os
from PIL import Image
import cv2
from moviepy.editor import VideoFileClip, AudioFileClip

from pydub import AudioSegment
import pyttsx3

api_key='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'

API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
headers = {
    "Authorization": f"Bearer {api_key}",
}

def query(payload,filename):
    try:
        print("loading...for this..",payload)

        response = requests.post(API_URL, headers=headers, json=payload)
        print(response.content)
        print("loading...end")
        if response.status_code == 200:
            content_type = response.headers.get("Content-Type")

            if "image" in content_type:
                # Check if it's an image
                with open(filename, "wb") as f:
                    f.write(response.content)
                    print("Image saved as {filename}.")
            else:
                print("Received non-image data.")
        else:
            print(f"Error: {response.status_code} - {response.text}")
        
        return response.content

    except Exception as e:
        print(e)
         
# pay = query("In a tiny village, surrounded by a lush forest, a curious little boy lived with his family. He loved exploring and wondered what lay beyond the trees.", "image1.jpg")

# You can access the image with PIL.Image for example
def clean_prompt(prompt):

    """
    Clean and validate the input prompt before processing.
    """
    # Strip leading/trailing whitespace
    cleaned_prompt = prompt.strip()

    # Check if the prompt is empty after cleaning
    if not cleaned_prompt:
        print("Error: Empty prompt found. Skipping this prompt.")
        return None

    # Remove any unwanted special characters (you can customize this list)
    cleaned_prompt = re.sub(r'[^\x00-\x7F]+', '', cleaned_prompt)  # Remove non-ASCII characters

    # Further cleaning can be added here as needed (e.g., handling punctuation, extra spaces)
    cleaned_prompt = re.sub(r'\s+', ' ', cleaned_prompt)  # Collapse multiple spaces into one

    return cleaned_prompt

list_promt=[]
def image_process(image_prompts):
    output_dir = "generated_images"
    print("raw data ",image_prompts)
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist

# Loop through the prompts and generate images
    for i, prompt in enumerate(image_prompts):
        if i==0:
            continue
        cleaned_prompt = clean_prompt(prompt)


        list_promt.append(cleaned_prompt)
        print("cleaned prompts list = ",list_promt)
        
       
        
        # Skip empty or invalid prompts
        if not cleaned_prompt:
            continue
        payload = cleaned_prompt
        filename = os.path.join(output_dir, f"image_{i + 1}.jpg")  # Unique filename
        query(payload, filename)

    print("All images have been processed.")
    prompt_file(list_promt)
    video_generater(list_promt)

  


# text to audio converter.....

def text_to_audio_narration(text_segments, output_file="audio_narration.mp3"):
    if len(text_segments)!=0:

   

        full_prompt = " ".join(text_segments)

        # Initialize the text-to-speech engine
        engine = pyttsx3.init()

        # Set speech rate (adjust to make audio ~5-10 seconds per prompt if needed)
        engine.setProperty('rate', 125)  # Adjust rate (words per minute) as needed

        # Directory to save the combined audio file
        output_directory = "audio_combined"
        os.makedirs(output_directory, exist_ok=True)

        # Save the full prompt to a single audio file
        audio_file = os.path.join(output_directory, "combined_prompts_audio.mp3")
        print("Generating combined audio...")
        engine.save_to_file(full_prompt, audio_file)
        engine.runAndWait()

        print("Combined audio file generated successfully!")


         # For length of audio file...
        try:
            audio_file_path = r'audio_combined/combined_prompts_audio.mp3'  # Correct file path
            if os.path.exists(audio_file_path):
                with wave.open(audio_file_path, 'rb') as wave_file:
                 frame_rate = wave_file.getframerate()
                 num_frames = wave_file.getnframes()
                 duration = num_frames / frame_rate
                 print("duration",duration)

                return duration
            else:
                print("Error: Audio file not found.")
                return None
        except Exception as e:
            print(f"Error calculating audio length: {e}")



    else:
        print("Not text provided for audio conversion")



def apply_zoom(image, zoom_factor=1.02):
    height, width = image.shape[:2]
    
    # Calculate the new dimensions
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)

    # Resize the image to apply the zoom
    zoomed_image = cv2.resize(image, (new_width, new_height))

    # Center the zoomed image by cropping back to original dimensions
    start_x = (new_width - width) // 2
    start_y = (new_height - height) // 2
    zoomed_image = zoomed_image[start_y:start_y+height, start_x:start_x+width]

    return zoomed_image

# video genration .....
def video_generater(image_list):
    folder_path = 'generated_images'

    take_audio_lenght=text_to_audio_narration(image_list)
    print("audio length=",take_audio_lenght)
    if take_audio_lenght!='':
     duratone_one_image=round_method(take_audio_lenght,len(image_list))
    

    if duratone_one_image!=0 :


    # List all image files in the folder
        image_files = [f for f in os.listdir(folder_path) if f.endswith('.jpg') or f.endswith('.png')]

        # Print the list of image files
        print(image_files)
        
        # Path to save the video
        video_path = 'output_video.mp4'

        # Define the frame rate (e.g., 1 frame per second)
        frame_rate = 30  # 1 frame per second
        image_duration =int (duratone_one_image ) # Duration for each image in seconds (each image will be displayed for 7 seconds)

        # Get the first image to extract dimensions
        first_image = cv2.imread(os.path.join(folder_path, image_files[0]))
        height, width, layers = first_image.shape

        # Create a video writer object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 file
        video_writer = cv2.VideoWriter(video_path, fourcc, frame_rate, (width, height))

        # Add each image to the video
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = cv2.imread(image_path)
            
            # Write the image multiple times for the desired duration
            for frame in range(frame_rate * image_duration):
                zoom_factor = 1 + (frame / (frame_rate * image_duration)) * 0.2  # Zoom from 1 to 1.2 over the duration
                
                # Apply the zoom effect on the image
                zoomed_image = apply_zoom(image, zoom_factor)
                
                # Write the zoomed image to the video
                video_writer.write(zoomed_image)  # # Write the frame to the video

        # Release the video writer object
        video_writer.release()

        print(f"Video saved to {video_path}")
    else:
        print("video not created because of invalid audio length")    
def audio_comb_video():
   

# Load the video and audio
    video_clip = VideoFileClip('output_video.mp4')
    audio_clip = AudioFileClip(r'audio_combined\combined_prompts_audio.mp3') # Ensure you have your audio file

    # Set the audio to the video
    video_clip = video_clip.set_audio(audio_clip)

    # Save the final video with audio
    video_clip.write_videofile('final_video_with_audio.mp4', codec='libx264')

    print("Final video with audio saved.")
# audio_comb_video() 

def round_method(tim, img_len):
    div = tim / img_len
    print("Image duration:", div)
    
    if div % 1 == 0:  # Check if div is an integer
        return div
    else:
        concise =tim-1
        print(concise)
        adjusted_num=concise/img_len
        print("Adjusted image duration:", adjusted_num)
        return adjusted_num   
        




def prompt_file(image_prom):
   
    output_file = "image_prompts.py"
    with open(output_file, "w") as f:
        f.write("image_prompts = [\n")
        for prompt in image_prom:
            f.write(f"    {repr(prompt)},\n")  # Use repr() to ensure proper string formatting
        f.write("]\n")


