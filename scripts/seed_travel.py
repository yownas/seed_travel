import modules.scripts as scripts
import gradio as gr

from modules.processing import Processed, process_images
from modules.shared import opts, cmd_opts, state


class Script(scripts.Script):
    def title(self):
        return "Seed travel"

    def show(self, is_img2img):
        return not is_img2img

    def ui(self, is_img2img):
        info = gr.HTML("<p style=\"margin-bottom:0.75em\">Samplers that work well are: Euler, LMS, Heun, DPM2 & DDIM. A Batch Count of 1 is recommended.</p>")
        dest_seed = gr.Textbox(label="Destination seed(s) (Comma separated)", lines=1)
        steps = gr.Textbox(label="Steps", lines=1)

        return [dest_seed, steps]

    def run(self, p, dest_seed, steps):
        initial_info = None
        images = []

        start_seed = p.seed
        seeds = [int(x.strip()) for x in dest_seed.split(",")]
        print(f"Generating {((int(steps)) * len(seeds)) + 1} images.")
        for next_seed in seeds:
            for i in range(int(steps)):
                p.seed = start_seed
                p.subseed = next_seed
                p.subseed_strength = float(i/float(steps))
                proc = process_images(p)
                if initial_info is None:
                    initial_info = proc.info
                images += proc.images
            start_seed = next_seed
        p.subseed_strength = 1.0
        proc = process_images(p)
        images += proc.images

        processed = Processed(p, images, p.seed, initial_info)

        return processed

    def describe(self):
        return "Travel between two (or more) seeds and create a picture at each step."
