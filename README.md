# Seed Travel
Small script for AUTOMATIC1111/stable-diffusion-webui to create images that exists between seeds.

Will let you pick two seeds (or more) and then create a number of images while it morph between the two points of noise generated.

Samplers that work well are: Euler, LMS, Heun, DPM2 & DDIM. (And possibly others, not Eular a though.)

Batch Count and Batch Size will be ignored and set to 1. Trying to generate images with Euler a will fail and print an error. If you really want to use it there is a checkbox to allow it.

# Installation
1. Copy the file in the scripts-folder to the scripts-folder from https://github.com/AUTOMATIC1111/stable-diffusion-webui
2. Add `moviepy==1.0.3` to requirements_versions.txt

# What is "seed traveling"?
To understand what "seed traveling" is I first have to give a very very simplified explaination of how Stable Diffusion generates pictures.
It starts with noise and then tweak and poke it until it gets an image that looks like something that match the prompt you gave. And to get all this initial noise you use a seed. The seed is used to generate a bunch of random numbers which will be your inital noise. A different seed generates a different set of random numbers.

The problem is that the seed is a 32 bit value, around 4 billion different possible values. Which is a lot, but it is infinitesimal compared to the possible initial noises.

If we imagine all the possible noises as a map, a seed could be seen as one single point on that map. A huge universe with only a few possible places to stand and look at it. What seed traveling lets you do is to pick two "points" on this map and then travel between them, each step a new variation of noise that no one could ever reach by only using a seed.

So, interpolating between the noise from two seeds will not only look cool as a video, you will also get images you might never have seen.

# Usage

`Destination seed(s)`: Seeds to travel to from `Seed`. If initial seed is empty, the first destination seed will be chosen as start seed. Seeds placed between parentheses will be ignored. (Might be useful while testing.) 

`Only use Random seeds`: Let you set `Number of random seeds` instead of typing them manually. `Seed` will be ignored unless comparing paths (see below).

`Steps`: Number of images to generate between each seed.

`Loop back to Initial seed`: When reaching the end, generate images to get back to the first seed.

`Save results as video`: Makes videos.

`Frames per second`: The fps of the video.

'Bump seed': If this is set higher than 0, instead of traveling to the destination seeds you will get a number of images based on the initial seed, mixed with the destination seeds. Perfect for when you have an almost perfect image but want to nudge it a little to see if you can improve it.

`Show generated images in ui`: Disable this if you generate a lot of steps to make life easier for your browser.

`"Hug the middle" during interpolation`: Left over from an old experiment. Makes the interpolation go a little bit faster at the start and at the end. May sometimes produce smoother video, most often not.

# Output

The images and video (if selected) will show up in the `outputs\txt2-images\travels` folder. With a separate numbered folder for each travel you've made.

# Example:
![kitten_example](https://user-images.githubusercontent.com/13150150/191132820-aeb80b3c-4244-4905-b49d-3bab52ee75ff.png)

# Result after making video of the images.
https://user-images.githubusercontent.com/13150150/191132919-3d594854-7045-4c48-8e61-f5a0a117035a.mp4
