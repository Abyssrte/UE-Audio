# UE-Audio
This Project Automates Audio Extraction From  (Unreal Engine) UE Wwise # .wem and .bnk Files Using Existing Open-Source Tools

## Credits & Open-Source Tools

This project is a helper/automation script and does **not** reimplement
audio extraction logic from scratch.

It relies on the following open-source tools:

- **ww2ogg**  
  Developed by **hcs64**  
  GitHub: https://github.com/hcs64/ww2ogg  
  Used for converting Wwise `.wem` files to `.ogg`.

- **FFmpeg**  
  https://ffmpeg.org  
  Used for audio decoding and format conversion.

All credit for the core extraction functionality goes to the original
tool authors. This project only automates and simplifies their usage.
