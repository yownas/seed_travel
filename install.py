import launch

if not launch.is_installed("imageio-ffmpeg"):
    launch.run_pip("install imageio-ffmpeg", "requirements for Seed Travel")
