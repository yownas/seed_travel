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
        return not is_img2img

    def ui(self, is_img2img):
        unsinify = gr.Checkbox(label='Reduce effect of sin() during interpolation', value=True)
        dest_seed = gr.Textbox(label="Destination seed(s) (Comma separated)", lines=1)
        steps = gr.Number(label="Steps", value=10)
        save_video = gr.Checkbox(label='Save results as video', value=True)

        return [dest_seed, steps, unsinify, save_video]

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

    def run(self, p, dest_seed, steps, unsinify, save_video):
        initial_info = None
        images = []

        # Custom seed travel saving
        travel_path = os.path.join(p.outpath_samples, "travels")
        os.makedirs(travel_path, exist_ok=True)
        travel_number = Script.get_next_sequence_number(travel_path)
        travel_path = os.path.join(travel_path, f"{travel_number:05}")
        p.outpath_samples = travel_path

        start_seed = p.seed
        seeds = [int(x.strip()) for x in dest_seed.split(",")]
        total_images = int(steps) * len(seeds) + 1
        print(f"Generating {total_images} images.")
        state.job_count = total_images # Set the job count to the total number of images to be generated
        for next_seed in seeds:
            p.seed = start_seed
            p.subseed = next_seed
            fix_seed(p)
            for i in range(int(steps)):
                if unsinify:
                    x = float(i/float(steps))
                    p.subseed_strength = x + (0.1 * math.sin(x*2*math.pi))
                else:
                    p.subseed_strength = float(i/float(steps))
                proc = process_images(p)
                if initial_info is None:
                    initial_info = proc.info
                images += proc.images
            start_seed = p.subseed
        p.seed = p.subseed
        p.subseed = None
        p.subseed_strength = 0.0
        proc = process_images(p)
        images += proc.images

        if save_video:
            import moviepy.video.io.ImageSequenceClip as ImageSequenceClip
            import numpy as np
            clip = ImageSequenceClip.ImageSequenceClip([np.asarray(i) for i in images], fps=30)
            clip.write_videofile(os.path.join(travel_path, f"travel-{travel_number:05}.mp4"), verbose=False, logger=None)

        processed = Processed(p, images, p.seed, initial_info)

        return processed

    def describe(self):
        return "Travel between two (or more) seeds and create a picture at each step."
