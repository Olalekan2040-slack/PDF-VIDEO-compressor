import streamlit as st
import subprocess
import tempfile
import os
from pathlib import Path

st.set_page_config(page_title="Media Tool", page_icon="🛠️", layout="wide")

# ── Custom CSS for caption editor ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap');

div[data-testid="stTextArea"] textarea {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 15px;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛠️ Media Compressor & Caption Generator")
st.markdown("**PDF • Video Compressor • Auto Captions** (Local Processing)")

tab1, tab2, tab3 = st.tabs(["📄 PDF Compressor", "🎬 Video Compressor", "📝 Auto Captions"])

# ====================== PDF COMPRESSOR ======================
with tab1:
    st.subheader("PDF Compressor")
    uploaded_pdf = st.file_uploader("Upload PDF File", type=["pdf"], key="pdf")
    pdf_level = st.selectbox("Compression Level", ["Low", "Medium", "High"], key="pdf_level")

    if uploaded_pdf and st.button("Compress PDF", type="primary"):
        try:
            settings = {"Low": "/printer", "Medium": "/ebook", "High": "/screen"}[pdf_level]
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_in:
                tmp_in.write(uploaded_pdf.getvalue())
                input_path = tmp_in.name
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_out:
                output_path = tmp_out.name

            gs_cmd = [
                "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
                f"-dPDFSETTINGS={settings}", "-dNOPAUSE", "-dQUIET", "-dBATCH",
                f"-sOutputFile={output_path}", input_path
            ]
            if os.name == "nt":
                gs_cmd[0] = "gswin64c.exe"

            subprocess.run(gs_cmd, check=True, capture_output=True)
            with open(output_path, "rb") as f:
                compressed = f.read()

            orig = len(uploaded_pdf.getvalue()) / (1024 * 1024)
            comp = len(compressed) / (1024 * 1024)
            reduction = (1 - comp / orig) * 100

            st.success(f"✅ Done! Size reduced by {reduction:.1f}%")
            st.download_button("⬇️ Download Compressed PDF", compressed,
                               f"COMPRESSED_{uploaded_pdf.name}", "application/pdf")
            for p in [input_path, output_path]:
                if os.path.exists(p):
                    os.unlink(p)
        except Exception as e:
            st.error(f"Error: {e}")

# ====================== VIDEO COMPRESSOR ======================
with tab2:
    st.subheader("🎬 Video Compressor")
    uploaded_video = st.file_uploader("Upload Video", type=["mp4", "mov", "avi", "mkv", "webm"], key="vcomp")
    col1, col2 = st.columns(2)
    with col1:
        quality = st.selectbox("Quality", ["High Quality", "Medium", "Small Size"])
    with col2:
        fmt = st.selectbox("Output Format", ["mp4", "webm"])

    if uploaded_video and st.button("Compress Video", type="primary"):
        with st.spinner("Compressing..."):
            try:
                crf = {"High Quality": "18", "Medium": "23", "Small Size": "28"}[quality]
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_in:
                    tmp_in.write(uploaded_video.getvalue())
                    in_path = tmp_in.name
                with tempfile.NamedTemporaryFile(delete=False, suffix=f".{fmt}") as tmp_out:
                    out_path = tmp_out.name

                cmd = [
                    "ffmpeg", "-i", in_path,
                    "-vcodec", "libx264" if fmt == "mp4" else "libvpx-vp9",
                    "-crf", crf, "-preset", "medium",
                    "-acodec", "aac" if fmt == "mp4" else "libopus",
                    "-y", out_path
                ]
                subprocess.run(cmd, check=True, capture_output=True)
                with open(out_path, "rb") as f:
                    data = f.read()

                st.success("✅ Video compressed successfully!")
                st.download_button("⬇️ Download Compressed Video", data,
                                   f"COMPRESSED_{Path(uploaded_video.name).stem}.{fmt}",
                                   f"video/{fmt}")
                for p in [in_path, out_path]:
                    if os.path.exists(p):
                        os.unlink(p)
            except Exception as e:
                st.error(f"Error: {e}")

# ====================== HELPERS ======================

def seconds_to_srt_time(seconds: float) -> str:
    """Convert float seconds to SRT timestamp: HH:MM:SS,mmm"""
    hours   = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs    = int(seconds % 60)
    millis  = int(round((seconds - int(seconds)) * 1000))
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


def build_srt_from_segments(segments: list) -> tuple:
    """
    Build SRT string + structured list from Whisper segments.
    Each segment = one sentence (Whisper already segments by phrase/sentence).
    Returns:
        srt_content (str)
        seg_dicts   (list of dict)
    """
    seg_dicts = []
    srt_lines = []
    for i, seg in enumerate(segments, 1):
        start_str = seconds_to_srt_time(seg.start)
        end_str   = seconds_to_srt_time(seg.end)
        text      = seg.text.strip()
        seg_dicts.append({
            "index":     i,
            "start":     seg.start,
            "end":       seg.end,
            "start_str": start_str,
            "end_str":   end_str,
            "text":      text,
        })
        srt_lines.append(f"{i}\n{start_str} --> {end_str}\n{text}\n")
    return "\n".join(srt_lines), seg_dicts


def rebuild_srt(seg_dicts: list) -> str:
    """Rebuild clean SRT from (possibly edited) segment dicts."""
    lines = []
    for s in seg_dicts:
        lines.append(f"{s['index']}\n{s['start_str']} --> {s['end_str']}\n{s['text']}\n")
    return "\n".join(lines)


def build_ass_with_slide(seg_dicts: list, video_width: int = 1280, video_height: int = 720) -> str:
    """
    Build an ASS subtitle file where each subtitle line slides in from the LEFT.
    Uses ASS \move() tag: \move(x1,y1,x2,y2,t1,t2)
      x1,y1 = start position (off-screen left)
      x2,y2 = end position   (final resting place, bottom-center)
      t1,t2 = animation time in ms (relative to subtitle start)

    Font: Plus Jakarta Sans — bold, 32pt, yellow, black outline.
    """
    # Y position = 88% down the frame
    y_pos    = int(video_height * 0.88)
    x_final  = video_width // 2        # centre of screen
    x_start  = -video_width // 2       # fully off-screen to the left
    slide_ms = 300                     # slide duration: 300 ms

    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {video_width}
PlayResY: {video_height}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Plus Jakarta Sans,32,&H00F5C518,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0.5,0,1,2,1,2,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    def srt_to_ass_time(srt: str) -> str:
        # SRT: HH:MM:SS,mmm  →  ASS: H:MM:SS.cc
        srt = srt.replace(",", ".")
        parts = srt.split(":")
        h, m, rest = parts[0], parts[1], parts[2]
        s, ms_str = rest.split(".")
        centisecs = int(ms_str[:3]) // 10
        return f"{int(h)}:{m}:{s}.{centisecs:02d}"

    dialogue_lines = []
    for seg in seg_dicts:
        start = srt_to_ass_time(seg["start_str"])
        end   = srt_to_ass_time(seg["end_str"])
        text  = seg["text"].replace("\n", " ")

        # \an2 = bottom-center anchor
        # \move slides from x_start to x_final over slide_ms milliseconds
        ass_text = (
            f"{{\\an2\\move({x_start},{y_pos},{x_final},{y_pos},0,{slide_ms})}}{text}"
        )
        dialogue_lines.append(
            f"Dialogue: 0,{start},{end},Default,,0,0,0,,{ass_text}"
        )

    return header + "\n".join(dialogue_lines)


def burn_subtitles_ass(video_path: str, ass_path: str) -> tuple:
    """
    Burn ASS subtitles into video using the 'ass' filter (supports \move animation).
    Returns (success, stderr, video_bytes).
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as out_tmp:
        burned_path = out_tmp.name

    if os.name == "nt":
        escaped = ass_path.replace("\\", "\\\\").replace(":", "\\:")
    else:
        escaped = ass_path.replace("'", "\\'")

    burn_cmd = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"ass='{escaped}'",
        "-c:v", "libx264",
        "-crf", "22",
        "-preset", "medium",
        "-c:a", "aac",
        "-y", burned_path,
    ]

    result = subprocess.run(burn_cmd, capture_output=True, text=True)

    if result.returncode == 0 and os.path.getsize(burned_path) > 0:
        with open(burned_path, "rb") as f:
            data = f.read()
        os.unlink(burned_path)
        return True, result.stderr, data
    else:
        if os.path.exists(burned_path):
            os.unlink(burned_path)
        return False, result.stderr, b""


def get_video_dimensions(video_path: str) -> tuple:
    """Return (width, height) of a video file using ffprobe."""
    result = subprocess.run([
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height",
        "-of", "csv=p=0",
        video_path
    ], capture_output=True, text=True)

    if result.returncode == 0 and result.stdout.strip():
        parts = result.stdout.strip().split(",")
        if len(parts) == 2:
            return int(parts[0]), int(parts[1])
    return 1280, 720   # safe default


# ====================== AUTO CAPTIONS TAB ======================
with tab3:
    st.subheader("📝 Auto Caption Generator")
    st.markdown(
        "Captions are generated **sentence-by-sentence**, timed to the speaker. "
        "Each sentence **slides in from the left** when burned into video."
    )

    video_file = st.file_uploader(
        "Upload Video", type=["mp4", "mov", "avi", "mkv", "webm"], key="caption"
    )

    col_a, col_b = st.columns(2)
    with col_a:
        model_size = st.selectbox(
            "Whisper Model",
            ["tiny", "base", "small", "medium"],
            index=1,
            help="'base' is a good balance of speed and accuracy."
        )
    with col_b:
        burn_subs = st.checkbox("Burn subtitles into video after editing", value=False)

    # ── Transcription ─────────────────────────────────────────────────────────
    if video_file and st.button("🎙️ Generate Captions", type="primary"):
        temp_files = []
        try:
            from faster_whisper import WhisperModel

            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(video_file.getvalue())
                video_path = tmp.name
            temp_files.append(video_path)

            with st.spinner("Transcribing audio — please wait..."):
                model = WhisperModel(model_size, device="cpu", compute_type="int8")
                # word_timestamps=False → Whisper segments by sentence naturally
                segments_gen, info = model.transcribe(
                    video_path, beam_size=5, word_timestamps=False
                )
                segment_list = list(segments_gen)

            srt_content, seg_dicts = build_srt_from_segments(segment_list)

            # Persist to session state
            st.session_state["seg_dicts"]   = seg_dicts
            st.session_state["srt_content"] = srt_content
            st.session_state["video_path"]  = video_path
            st.session_state["video_name"]  = video_file.name
            st.session_state["language"]    = info.language.upper()

        except ImportError:
            st.error("Please install faster-whisper: `pip install faster-whisper`")
        except Exception as e:
            st.error(f"Transcription error: {e}")
            for p in temp_files:
                try:
                    if os.path.exists(p):
                        os.unlink(p)
                except OSError:
                    pass

    # ── Caption Editor ────────────────────────────────────────────────────────
    if "seg_dicts" in st.session_state and st.session_state["seg_dicts"]:

        seg_dicts = st.session_state["seg_dicts"]
        lang      = st.session_state.get("language", "?")

        st.success(
            f"✅ {len(seg_dicts)} sentences detected · Language: **{lang}**"
        )
        st.markdown("---")
        st.markdown("### ✏️ Review & Edit Captions")
        st.caption(
            "Each row is one caption sentence. Edit text directly if Whisper made mistakes. "
            "Check **Del** to remove a segment. Timestamps are preserved automatically."
        )

        edited_dicts = []
        for seg in seg_dicts:
            with st.container():
                col_ts, col_text, col_del = st.columns([1.4, 5.5, 0.5])

                with col_ts:
                    st.markdown(
                        f"<p style='font-family:monospace;font-size:11px;color:#999;"
                        f"line-height:1.8;padding-top:6px;margin:0;'>"
                        f"<b style=\"color:#f5c518\">#{seg['index']:03d}</b><br>"
                        f"▶ {seg['start_str']}<br>"
                        f"■ {seg['end_str']}</p>",
                        unsafe_allow_html=True
                    )

                with col_text:
                    new_text = st.text_area(
                        label=f"Caption #{seg['index']}",
                        value=seg["text"],
                        height=75,
                        label_visibility="collapsed",
                        key=f"edit_{seg['index']}",
                    )

                with col_del:
                    st.markdown("<div style='padding-top:20px'>", unsafe_allow_html=True)
                    delete = st.checkbox(
                        "Del",
                        key=f"del_{seg['index']}",
                        help="Check to remove this segment"
                    )
                    st.markdown("</div>", unsafe_allow_html=True)

            if not delete:
                edited_dicts.append({**seg, "text": new_text.strip()})

        # Re-index after deletions
        for new_i, d in enumerate(edited_dicts, 1):
            d["index"] = new_i

        st.session_state["edited_dicts"] = edited_dicts

        # ── Preview + SRT download ───────────────────────────────────────────
        st.markdown("---")
        final_srt = rebuild_srt(edited_dicts)

        col_prev, col_dl = st.columns([3, 1])
        with col_prev:
            with st.expander("👁️ Preview final SRT"):
                st.code(final_srt, language="text")
        with col_dl:
            st.download_button(
                "⬇️ Download SRT",
                final_srt.encode("utf-8"),
                f"{Path(st.session_state['video_name']).stem}.srt",
                "text/plain",
                use_container_width=True,
            )

        # ── Burn section ─────────────────────────────────────────────────────
        if burn_subs:
            st.markdown("### 🔥 Burn Subtitles into Video")

            st.info(
                "**Subtitle style:** Plus Jakarta Sans · 32pt · Bold · Yellow · Black outline\n\n"
                "Each sentence slides in from the **left edge** of the frame, timed exactly "
                "to when the speaker says it.",
                icon="🎨"
            )

            if st.button("🎬 Burn Edited Subtitles into Video", type="primary"):
                video_path = st.session_state.get("video_path")

                if not video_path or not os.path.exists(video_path):
                    st.error(
                        "The original video is no longer on disk. "
                        "Please re-upload and re-transcribe."
                    )
                else:
                    temp_burn_files = []
                    try:
                        # Get actual video dimensions for correct ASS resolution
                        vid_w, vid_h = get_video_dimensions(video_path)

                        # Build ASS with slide-in animation
                        ass_content = build_ass_with_slide(edited_dicts, vid_w, vid_h)

                        with tempfile.NamedTemporaryFile(
                            delete=False, suffix=".ass",
                            mode="w", encoding="utf-8"
                        ) as ass_file:
                            ass_file.write(ass_content)
                            ass_path = ass_file.name
                        temp_burn_files.append(ass_path)

                        with st.spinner("🎞️ Burning subtitles — this may take a minute..."):
                            success, stderr, burned_data = burn_subtitles_ass(video_path, ass_path)

                        if success:
                            st.success("✅ Done! Your captioned video is ready.")
                            st.download_button(
                                "⬇️ Download Captioned Video",
                                burned_data,
                                f"{Path(st.session_state['video_name']).stem}_captioned.mp4",
                                "video/mp4",
                                use_container_width=True,
                            )
                        else:
                            st.error("❌ Burning failed. Your SRT is still available above.")
                            with st.expander("Show ffmpeg error details"):
                                st.code(stderr[-2000:], language="text")

                    finally:
                        for p in temp_burn_files:
                            try:
                                if os.path.exists(p):
                                    os.unlink(p)
                            except OSError:
                                pass

st.caption("Tip: Use videos under 2 minutes for faster processing.")