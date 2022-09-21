# seed_travel
Small script for AUTOMATIC1111/stable-diffusion-webui to create images that exists between seeds.

Installation:
1. Copy the file in the scripts-folder to the scripts-folder from https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Add `moviepy==1.0.3` to requirements_versions.txt

Will let you pick two seeds (or more) and then create a number of images while it morph between the two points of noise generated.

Samplers that work well are: Euler (sometimes), LMS, Heun, DPM2 & DDIM. A Batch Count of 1 is recommended.

# Example:
![kitten_example](https://user-images.githubusercontent.com/13150150/191132820-aeb80b3c-4244-4905-b49d-3bab52ee75ff.png)

# Result after making video of the images.
https://user-images.githubusercontent.com/13150150/191132919-3d594854-7045-4c48-8e61-f5a0a117035a.mp4
