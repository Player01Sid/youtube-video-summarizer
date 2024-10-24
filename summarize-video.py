from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Load the summarization model
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def get_transcript(video_id):
    try:
        # Check if the video_id is valid
        if not video_id:
            return "Error: Invalid video ID provided."
        
        # Get the transcript of the video
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        # Combine the text segments into one full transcript
        full_transcript = "\n".join([entry['text'] for entry in transcript])
        
        return full_transcript
    
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"

def summarize_transcript(transcript):
    try:
        # Summarize using the free Hugging Face summarization model
        summary = summarizer(transcript, max_length=150, min_length=40, do_sample=False)
        return summary[0]['summary_text']

    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL or ID: ").strip()
    
    # Extract video ID from full URL if needed
    if "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        video_id = video_url  # Direct video ID input
    
    # Step 1: Get transcript
    transcript = get_transcript(video_id)
    if "Error" in transcript:
        print(transcript)
    else:
        print("Transcript retrieved successfully.")
        
        # Step 2: Summarize transcript
        summary = summarize_transcript(transcript)
        print("\nSummary of the video:")
        print(summary)
