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
        steps = gr.Textbox(label="Steps", lines=1)

        return [dest_seed, steps, unsinify]

    def run(self, p, dest_seed, steps, unsinify):
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

        processed = Processed(p, images, p.seed, initial_info)

        return processed

    def describe(self):
        return "Travel between two (or more) seeds and create a picture at each step."
