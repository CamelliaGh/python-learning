from pytubefix import YouTube
from pytubefix.exceptions import (
    VideoUnavailable,
    RegexMatchError,
    VideoPrivate,
    VideoRegionBlocked,
    AgeRestrictedError,
    MembersOnly,
    RecordingUnavailable,
    LiveStreamError,
    MaxRetriesExceeded,
)
from pathlib import Path
from tqdm import tqdm
import argparse
import sys


class YouTubeDownloader:
    """Downloads YouTube videos with progress tracking and quality selection."""

    def __init__(
        self, url: str, output_path: str | None = None, quality: str | None = None
    ) -> None:
        """Initialize YouTube downloader.

        Args:
            url: YouTube video URL
            output_path: Directory to save video (default: current directory)
            quality: Video quality like '720p', '1080p', or 'highest' (default: 'highest')
        """
        self.url = url
        self.quality = quality or "highest"
        self.pbar = None

        if output_path:
            self.output_path = Path(output_path)
            if not self.output_path.exists():
                try:
                    self.output_path.mkdir(parents=True, exist_ok=True)
                except (PermissionError, OSError) as e:
                    raise ValueError(
                        f"Cannot create or access output directory '{output_path}': {e}"
                    )
            elif not self.output_path.is_dir():
                raise ValueError(f"Output path '{output_path}' is not a directory")
        else:
            self.output_path = Path.cwd()

        if not url or not isinstance(url, str):
            raise ValueError("URL must be a non-empty string")

        try:
            self.yt = YouTube(
                url,
                on_progress_callback=self.on_progress,
                on_complete_callback=self.on_complete,
            )
        except VideoUnavailable:
            raise ValueError(
                f"Video is unavailable. The video may have been deleted, made private, or the URL is invalid: {url}"
            )
        except VideoPrivate:
            raise ValueError(f"Video is private and cannot be accessed: {url}")
        except VideoRegionBlocked:
            raise ValueError(f"Video is not available in your region: {url}")
        except AgeRestrictedError:
            raise ValueError(f"Video is age-restricted and requires sign-in: {url}")
        except MembersOnly:
            raise ValueError(
                f"Video is members-only and requires channel membership: {url}"
            )
        except RecordingUnavailable:
            raise ValueError(f"Live stream recording is not available: {url}")
        except LiveStreamError:
            raise ValueError(
                f"Cannot download live stream while it's in progress: {url}"
            )
        except RegexMatchError:
            raise ValueError(
                f"Invalid YouTube URL or unable to extract video information: {url}"
            )
        except MaxRetriesExceeded:
            raise ConnectionError(
                "Failed to connect to YouTube after multiple retries. "
                "Please check your internet connection and try again."
            )
        except Exception as e:
            raise RuntimeError(
                f"Unexpected error initializing YouTube object: {type(e).__name__}: {e}"
            )

    def download(self):
        """Download video with selected quality and progress tracking."""
        video_stream = None
        try:
            streams = self.yt.streams.filter(progressive=True, file_extension="mp4")

            if self.quality and self.quality != "highest":
                video_stream = streams.filter(res=self.quality).first()
                if video_stream is None:
                    print(
                        f"Warning: Quality '{self.quality}' not available, using highest quality instead."
                    )
                    video_stream = streams.order_by("resolution").desc().first()
            else:
                video_stream = streams.order_by("resolution").desc().first()

            if video_stream is None:
                available_qualities = [
                    str(stream.resolution) for stream in streams if stream.resolution
                ]
                raise ValueError(
                    f"No downloadable streams found for this video.\n"
                    f"Title: {self.yt.title}\n"
                    f"Available qualities: {', '.join(set(available_qualities)) if available_qualities else 'None'}"
                )

            try:
                self.pbar = tqdm(
                    total=video_stream.filesize,
                    unit="B",
                    unit_scale=True,
                    desc=self.yt.title[:50],
                    colour="green",
                )
            except Exception as e:
                print(f"Warning: Could not initialize progress bar: {e}")

            try:
                video_stream.download(self.output_path)
            except PermissionError:
                raise PermissionError(
                    f"Permission denied: Cannot write to '{self.output_path}'. "
                    f"Please check directory permissions or choose a different output path."
                )
            except OSError as e:
                raise OSError(
                    f"File system error while downloading: {e}. "
                    f"Please check available disk space and directory permissions."
                )
            except Exception as e:
                raise RuntimeError(f"Download failed: {type(e).__name__}: {e}")

        except KeyboardInterrupt:
            print("\n\nDownload cancelled by user.")
            if self.pbar:
                self.pbar.close()
            raise
        except (ValueError, PermissionError, OSError, RuntimeError):
            if self.pbar:
                self.pbar.close()
            raise
        except Exception as e:
            error_msg = f"Unexpected error during download: {type(e).__name__}: {e}"
            print(f"Error: {error_msg}")
            if self.pbar:
                self.pbar.close()
            raise RuntimeError(error_msg) from e

    def on_progress(self, stream, chunk, bytes_remaining):
        """Update progress bar during download."""
        try:
            if self.pbar is not None:
                current = stream.filesize - bytes_remaining
                self.pbar.update(current - self.pbar.n)
        except Exception:
            pass

    def on_complete(self, stream, file_path):
        """Handle download completion and cleanup."""
        try:
            if self.pbar is not None:
                self.pbar.close()
                self.pbar = None

            title = getattr(self.yt, "title", "Unknown")
            print(f"\n✓ Downloaded '{title}' successfully to: {file_path}")
        except Exception as e:
            if self.pbar is not None:
                try:
                    self.pbar.close()
                except Exception:
                    pass
                self.pbar = None
            print(
                f"\nDownload completed, but there was an error displaying completion message: {e}"
            )


def main():
    """Parse command line arguments and execute download."""
    parser = argparse.ArgumentParser(
        description="Download YouTube videos with customizable quality settings",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "-u", "--url", help="YouTube video URL", required=True, type=str
    )
    parser.add_argument(
        "-q",
        "--quality",
        help="The desired video quality (e.g., 720p, 1080p, highest). Default: highest",
        default="highest",
        type=str,
    )
    parser.add_argument(
        "-o",
        "--output_path",
        help="The output directory to save the video. Default: current directory",
        default=".",
        type=str,
    )
    args = parser.parse_args()

    try:
        youtube_downloader = YouTubeDownloader(args.url, args.output_path, args.quality)
        youtube_downloader.download()
        return 0
    except KeyboardInterrupt:
        print("\n\nDownload interrupted by user.")
        return 130
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except PermissionError as e:
        print(f"Permission Error: {e}", file=sys.stderr)
        return 13
    except OSError as e:
        print(f"File System Error: {e}", file=sys.stderr)
        return 1
    except ConnectionError as e:
        print(f"Connection Error: {e}", file=sys.stderr)
        return 1
    except RuntimeError as e:
        print(f"Runtime Error: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unexpected Error: {type(e).__name__}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
