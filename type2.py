from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

# Load the summarization model
# summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


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

def summarize_transcript(transcript, max_chunk_size=1000):
    try:
        # Split the transcript into smaller chunks
        transcript_chunks = [transcript[i:i+max_chunk_size] for i in range(0, len(transcript), max_chunk_size)]
        
        # Summarize each chunk and combine the results
        summaries = []
        for chunk in transcript_chunks:
            summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        
        # Join all summaries together
        final_summary = " ".join(summaries)
        return final_summary

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
