import launch

if not launch.is_installed("moviepy"):
    launch.run_pip("install moviepy==1.0.3", "requirements for Seed Travel")
