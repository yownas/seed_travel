# Seed Travel
Small script for AUTOMATIC1111/stable-diffusion-webui to create images that exists between seeds.

Will let you pick two seeds (or more) and then create a number of images while it morph between the two points of noise generated.

Samplers that work well are: Euler, LMS, Heun, DPM2, DPM++ 2M, LMS Karras, DPM2 Karras, DPM++ 2M Karras, DDIM and PLMS

[Look here for more information about issues with some samplers.](SAMPLER_TEST.md)

Batch Count and Batch Size will be ignored and set to 1. Trying to generate images with Euler a will fail and print an error. If you really want to use it there is a checkbox to allow it.

[Examples of what you can do](USER_EXAMPLES.md).

# Installation

Easiest way to install it is to:
1. Go to the "Extensions" tab in the webui
2. Click on the "Install from URL" tab
3. Paste https://github.com/yownas/seed_travel.git into "URL for extension's git repository" and click install
4. ("Optional". You will need to restart the webui for dependensies to be installed or you won't be able to generate video files.)

Manual install:
1. Copy the file in the scripts-folder to the scripts-folder from https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Add `moviepy==1.0.3` to requirements_versions.txt

# Colab

Seed travel should work in one of the Colab links on AUTOMATIC1111's page. But to be able to create videos you need to make sure that yoour Colab has the correct version of moviepy installed. By default version 0.2.3.5 seem to be installed, but it is easy to fix by just adding this to your code (somewhere at the top is fine). Then install Seed Travel from the Extensions tab as usual.

`!pip install moviepy==1.0.3`

# What is "seed traveling"?
To understand what "seed traveling" is I first have to give a very very simplified explaination of how Stable Diffusion generates pictures.
It starts with noise and then tweak and poke it until it gets an image that looks like something that match the prompt you gave. And to get all this initial noise you use a seed. The seed is used to generate a bunch of random numbers which will be your inital noise. A different seed generates a different set of random numbers.

The problem is that the seed is a 32 bit value, around 4 billion different possible values. Which is a lot, but it is infinitesimal compared to the possible initial noises.

If we imagine all the possible noises as a map, a seed could be seen as one single point on that map. A huge universe with only a few possible places to stand and look at it. What seed traveling lets you do is to pick two "points" on this map and then travel between them, each step a new variation of noise that no one could ever reach by only using a seed.

So, interpolating between the noise from two seeds will not only look cool as a video, you will also get images you might never have seen.

# Usage

`Destination seed(s)`: Seeds to travel to from `Seed`. If initial seed is empty, the first destination seed will be chosen as start seed. Seeds placed between parentheses will be ignored. (Might be useful while testing.) 

`Only use Random seeds`: Let you set `Number of random seeds` instead of typing them manually. `Seed` will be ignored unless comparing paths (see below).

`Compare paths`: Instead of traveling betwen the seeds in order, travel from the first seed to each of the other seeds. For example, "1, 2, 3, 4" would normally travel from 1 to 2, to 3 to 4. If this is enabled the script will travel from 1 to 2, 1 to 3, 1 to 4. Useful if you want to test paths.

`Steps`: Number of images to generate between each seed.

`Loop back to Initial seed`: When reaching the end, generate images to get back to the first seed.

`SSIM threshold (0 to disable)`: If this is set to something other than 0, the script will first generate the steps you've specified above, but then take a second pass and fill in the gaps between images that differ too much according to Structual Similarity Index Metric [(pdf)](https://www.cns.nyu.edu/pub/eero/wang03-reprint.pdf). A good value depends a lot on which model and prompt you use, but 0.7 to 0.8 should be a good starting value. More than 0.95 will probably not improve much. If you want a very smooth video you should use something like [Flowframes](https://nmkd.itch.io/flowframes).

`Save results as video`: Makes videos.

`SSIM CenterCrop% (0 to disable)`: Crop a piece from the center of the image to be used for SSIM. In percent of the height and width. 0 will use the entire image. Only checking a small part of the image might make SSIM more sensitive. Be prepared to lower SSIM threshold to 0.4 to 0.5 if you use this.

`Frames per second`: The fps of the video.

`Number of frames for lead in/out`: Amount of frames to be padded with a static image at the start and ending of the video. So you'll get a short pause before the video start/ends.

`Upscaler`: Choose upscale method to be applied to the images before made into a video.

`Upscale ratio`: How much the images should be upscaled. A value of 0 or 1 will disable scaling.

`Bump seed`: If this is set higher than 0, instead of traveling to the destination seeds you will get a number of images based on the initial seed, mixed with the destination seeds. Perfect for when you have an almost perfect image but want to nudge it a little to see if you can improve it.

`Use cache`: To speed up generation, generated images are cached and re-used if possible. If you want to manually post-process the images and want all of them to be generated, please disable this.

`Show generated images in ui`: Disable this if you generate a lot of steps to make life easier for your browser.

`Interpolation rate`: Select how the interpolation should be done. Make the changes linear, slow in the middle, at the end or in the beginning. This can be used if you want your animation to change to the beat of music or make the interpolation more interesting.

`Rate strength`: (Only affect the "Slow start" and "Quick start" rate.) Choose how fast/slow interpolation should be done. Useful numbers are around 2 to 5. (Below 1.0 things will be very weird.)

`Allow the default Euler a Sampling method. (Does not produce good results)`: By default Euler A is disabled since it breaks animations with more than 2 seeds. Some Samplers doesn't seem to handle Variation Seeds well, and fail when switching from one seed to another. Mostly the ones with a "a" in them. You are of course free to use them, but you might get weird skips in the animation.

`SSIM minimum substep`: Smallest "step" SSIM is allowed to take. Sometimes animations can't me smoothed out, no matter how small steps you take. It is better to let the script give up and have a single skip than force it and get an animation that flickers.

`Desired min SSIM threshold (% of threshold)`: Try to make new images "at least" this good. By default SSIM will give up a newly generated image is worse then the gap it is trying to fill. This will allow you to set "Steps" to something as low as 1 and not have SSIM give up just because the image halfway through was bad.

# Output

The images and video (if selected) will show up in the `outputs\txt2-images\travels` folder. With a separate numbered folder for each travel you've made.

# Notice:

If you get an error like this `ValueError: could not convert string to float: ''` the problem might be that you have old default values stored. To fix this edit the file `ui-config.json` and remove the lines starting with `"customscript/seed_travel.py/...`. This issue could also be caused by other scripts, and the simplest way to fix is to remove the lines for those scripts as well.

# Example:
![kitten_example](https://user-images.githubusercontent.com/13150150/191132820-aeb80b3c-4244-4905-b49d-3bab52ee75ff.png)

# Result after making video of the images.
https://user-images.githubusercontent.com/13150150/191132919-3d594854-7045-4c48-8e61-f5a0a117035a.mp4
