import os
import modules.scripts as scripts
import gradio as gr
import math
from modules.processing import Processed, process_images, fix_seed
from modules.shared import opts, cmd_opts, state


class Script(scripts.Script):
    def title(self):
        return "Seed travel"

    def show(self, is_img2img):
        return True

    def ui(self, is_img2img):
        unsinify = gr.Checkbox(label='Reduce effect of sin() during interpolation', value=True)
        dest_seed = gr.Textbox(label="Destination seed(s) (Comma separated)", lines=1)
        steps = gr.Number(label="Steps", value=10)
        loopback = gr.Checkbox(label='Loop back to initial seed', value=True)
        save_video = gr.Checkbox(label='Save results as video', value=True)
        video_fps = gr.Number(label='Frames per second', value=30)

        return [dest_seed, steps, unsinify, loopback, save_video, video_fps]

    def get_next_sequence_number(path):
        from pathlib import Path
        """
        Determines and returns the next sequence number to use when saving an image in the specified directory.

        The sequence starts at 0.
        """
        result = -1
        dir = Path(path)
        for file in dir.iterdir():
            if not file.is_dir(): continue
            try:
                num = int(file.name)
                if num > result: result = num
            except ValueError:
                pass
        return result + 1

    def run(self, p, dest_seed, steps, unsinify, loopback, save_video, video_fps):
        initial_info = None
        images = []

        # Custom seed travel saving
        travel_path = os.path.join(p.outpath_samples, "travels")
        os.makedirs(travel_path, exist_ok=True)
        travel_number = Script.get_next_sequence_number(travel_path)
        travel_path = os.path.join(travel_path, f"{travel_number:05}")
        p.outpath_samples = travel_path

        seeds = [p.seed] + [int(x.strip()) for x in dest_seed.split(",")]
        total_images = (int(steps) * len(seeds)) - (0 if loopback else (int(steps) - 1))
        print(f"Generating {total_images} images.")

        # Set generation helpers
        state.job_count = total_images
        p.extra_generation_params["Travel steps"] = steps
        p.extra_generation_params["Destination seeds"] = str(seeds)

        for i in range(len(seeds)):
            p.seed = seeds[i]
            p.subseed = seeds[i+1] if i+1 < len(seeds) else seeds[0]
            fix_seed(p)
            # We want to save seeds since they might have been altered by fix_seed()
            seeds[i] = p.seed
            if i+1 < len(seeds): seeds[i+1] = p.subseed

            numsteps = 1 if not loopback and i+1 == len(seeds) else int(steps) # Number of steps is 1 if we aren't looping at the last seed
            for i in range(numsteps):
                if unsinify:
                    x = float(i/float(steps))
                    p.subseed_strength = x + (0.1 * math.sin(x*2*math.pi))
                else:
                    p.subseed_strength = float(i/float(steps))
                proc = process_images(p)
                if initial_info is None:
                    initial_info = proc.info
                images += proc.images

        if save_video:
            import moviepy.video.io.ImageSequenceClip as ImageSequenceClip
            import numpy as np
            clip = ImageSequenceClip.ImageSequenceClip([np.asarray(i) for i in images], fps=video_fps)
            clip.write_videofile(os.path.join(travel_path, f"travel-{travel_number:05}.mp4"), verbose=False, logger=None)

        processed = Processed(p, images, p.seed, initial_info)

        return processed

    def describe(self):
        return "Travel between two (or more) seeds and create a picture at each step."
