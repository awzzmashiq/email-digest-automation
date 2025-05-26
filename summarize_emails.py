from transformers import pipeline

# Initialize the Hugging Face summarizer model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def summarize_emails(email_data):
    # Combine all email text
    full_text = " ".join(email_data).strip()

    # Handle empty or very short input
    if not full_text or len(full_text.split()) < 50:
        return "No important emails found today, or the content is too short for summarization."

    # Hugging Face models have a max input size (~1024 tokens), so we truncate if needed
    max_input_length = 1024
    if len(full_text) > max_input_length:
        full_text = full_text[:max_input_length]

    # Generate summary
    try:
        summary = summarizer(full_text, max_length=200, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Error during summarization: {str(e)}"
