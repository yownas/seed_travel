Below is a simple test of "kitten, ultra realistic, concept art", 512x512, SD v1.5, CFG 7 and 20 sampling steps. Traveling between seed 1,2 & 3.
Some samplers work better than others, some will fail when swiching seed and subseed. Even if "0% of seed 1 and 100% of seed 2" should be the same as
"100% of seed 2 and 0% of seed 3", something goes wrong. I suspect some samplers use the main seed interanally and doesn't care about subseeds.
I can't really call it a bug, since the samplers probably never were made to work with subseeds and even less used as animations the way seed travel does.
But if someone has a good/clean idea how to fix this I'd be happy to add it.

From the table below we can see that samplers that work well with subseeds are: Euler, LMS, Heun, DPM2, DPM++ 2M, LMS Karras, DPM2 Karras, DPM++ 2M Karras, DDIM and PLMS.

![seed_travel_sampler_test](https://user-images.githubusercontent.com/13150150/209980850-b4dc4d07-415a-4dc2-a745-bade555a2e40.png)
