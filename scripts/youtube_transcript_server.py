# youtube_transcript_server.py
import logging

import typer
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from youtube_transcript_api import NoTranscriptFound, TranscriptsDisabled, YouTubeTranscriptApi

assert load_dotenv(override=True), "Failed to load .env file"
logger = logging.getLogger(__name__)
app = typer.Typer()


def set_verbosity(verbose: bool):
    if verbose:
        logging.basicConfig(level=logging.DEBUG)


# Initialize FastMCP server
mcp = FastMCP(
    "youtube_transcript",
    port=8001,
    debug=True,
)


@mcp.tool()
def get_transcript(
    video_id: str,
    language: str = "en",
) -> str:
    """
    Get transcript for a YouTube video.

    Args:
        video_id: YouTube video ID (e.g. dQw4w9WgXcQ)
        language: Language code for transcript (default: "en")

    Returns:
        String containing the transcript text
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(
            video_id=video_id,
            languages=[
                language,
            ],
        )

        # Format transcript with timestamps
        formatted_transcript = ""
        for entry in transcript:
            start_time = int(entry["start"])
            minutes = start_time // 60
            seconds = start_time % 60
            formatted_transcript += f"[{minutes:02d}:{seconds:02d}] {entry['text']}\n"

        return formatted_transcript if formatted_transcript else "No transcript content found."

    except TranscriptsDisabled:
        return "Transcripts are disabled for this video."
    except NoTranscriptFound:
        return f"No transcript found in language '{language}'. Try another language code."
    except Exception as e:
        return f"Error retrieving transcript: {str(e)}"


@mcp.tool()
def list_available_transcripts(video_id: str) -> str:
    """
    List all available transcript languages for a YouTube video.

    Args:
        video_id: YouTube video ID (e.g. dQw4w9WgXcQ)

    Returns:
        String containing list of available transcript languages
    """
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        available_languages = []
        for transcript in transcript_list:
            language_code = transcript.language_code
            language_name = transcript.language
            is_generated = " (auto-generated)" if transcript.is_generated else ""
            available_languages.append(f"{language_code}: {language_name}{is_generated}")

        return "\n".join(available_languages) if available_languages else "No transcripts available."

    except Exception as e:
        return f"Error listing transcripts: {str(e)}"


@mcp.tool()
def get_transcript_summary(video_id: str, language: str = "en", max_length: int = None) -> str:
    """
    Get a summary of a YouTube video transcript.

    Args:
        video_id: YouTube video ID (e.g. dQw4w9WgXcQ)
        language: Language code for transcript (default: "en")
        max_length: Maximum length of the summary (default: None for full text)

    Returns:
        String containing a simplified transcript summary
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        # Combine all text into one continuous transcript
        full_text = " ".join([entry["text"] for entry in transcript])

        # Return full text if max_length is None, otherwise truncate
        if max_length is None or len(full_text) <= max_length:
            return full_text
        else:
            return full_text[:max_length] + "..."

    except Exception as e:
        return f"Error summarizing transcript: {str(e)}"


# Command-line interface for the script


@app.command(
    help="Get transcript for a YouTube video",
)
def get_transcript_run(
    video_id: str = "dQw4w9WgXcQ",  # e.g. dQw4w9WgXcQ
    language: str = "en",  # e.g. en, ja
    verbose: bool = False,
):
    set_verbosity(verbose)
    print(list_available_transcripts(video_id=video_id))
    print(get_transcript(video_id=video_id, language=language))
    print(get_transcript_summary(video_id=video_id, language=language))


@app.command(
    help="Run the FastMCP server",
)
def mcp_run(
    transport: str = "stdio",  # e.g. sse, stdio
    verbose: bool = False,
):
    set_verbosity(verbose)
    mcp.run(transport=transport)


if __name__ == "__main__":
    app()
