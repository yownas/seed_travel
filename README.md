# seed_travel
Small script for AUTOMATIC1111/stable-diffusion-webui to create images that exists between seeds.

Installation:
Copy the file in the scripts-folder to the scripts-folder from https://github.com/AUTOMATIC1111/stable-diffusion-webui

Will let you pick two seeds (or more) and then create a number of images while it morph between the two points of noise generated.

Samplers that work well are: Euler (sometimes), LMS, Heun, DPM2 & DDIM. A Batch Count of 1 is recommended.

