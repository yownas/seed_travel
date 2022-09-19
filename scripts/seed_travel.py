import modules.scripts as scripts
import gradio as gr

from modules.processing import Processed, process_images, fix_seed
from modules.shared import opts, cmd_opts, state


class Script(scripts.Script):
    def title(self):
        return "Seed travel"

    def show(self, is_img2img):
        return not is_img2img

    def ui(self, is_img2img):
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
            p.seed = start_seed
            p.subseed = next_seed
            fix_seed(p)
            for i in range(int(steps)):
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

        processed = Processed(p, images, p.seed, initial_info)

        return processed

    def describe(self):
        return "Travel between two (or more) seeds and create a picture at each step."
