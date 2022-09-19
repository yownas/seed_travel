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
        info = gr.HTML("<p style=\"margin-bottom:0.75em\">Samplers that seem to work well are: Euler, LMS, Heun, DPM2 & DDIM.</p>")
        dest_seed = gr.Textbox(label="Destination seed", lines=1)
        steps = gr.Textbox(label="Steps", lines=1)

        return [dest_seed, steps]

    def run(self, p, dest_seed, steps):
        # TODO: Force Batch Count to 1?
        # TODO: Fix filename...somehow
        # TODO: support for multiple dest_seed
        images = []
        for i in range(int(steps) + 1):
            print(f"Step {i} of {int(steps) + 1}\n")
            # This does not seem to work for all samplers.
            p.subseed = int(dest_seed)
            p.subseed_strength= float(i/float(steps))
            proc = process_images(p)
            images += proc.images

        processed = Processed(p, images, p.seed, p.subseed, f"Traveled from {p.seed} to {dest_seed} in {steps} steps.")

        return processed

    def describe(self):
        return "Travel between two seeds and create a picture at each step."


