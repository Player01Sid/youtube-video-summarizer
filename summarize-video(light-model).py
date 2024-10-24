from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline

summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def get_transcript(video_id):
    try:
        if not video_id:
            return "Error: Invalid video ID provided."
        
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        
        full_transcript = "\n".join([entry['text'] for entry in transcript])
        
        return full_transcript
    
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"

def summarize_transcript(transcript, max_chunk_size=500, max_chunks=3):
    try:
        transcript_chunks = [transcript[i:i + max_chunk_size] for i in range(0, len(transcript), max_chunk_size)]
        
        transcript_chunks = transcript_chunks[:max_chunks]
        
        summaries = summarizer(transcript_chunks, max_length=100, min_length=30, do_sample=False)
        
        final_summary = " ".join([summary['summary_text'] for summary in summaries])
        return final_summary

    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"

if __name__ == "__main__":
    video_url = input("Enter the YouTube video URL or ID: ").strip()
    
    if "v=" in video_url:
        video_id = video_url.split("v=")[-1].split("&")[0]
    else:
        video_id = video_url 
    
    transcript = get_transcript(video_id)
    if "Error" in transcript:
        print(transcript)
    else:
        print("Transcript retrieved successfully.")
        
        summary = summarize_transcript(transcript)
        print("\nSummary of the video:")
        print(summary)
