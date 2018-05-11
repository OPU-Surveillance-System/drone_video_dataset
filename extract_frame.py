#!/usr/bin/env python3

import os, random, subprocess
import imageio
import visvis as vv

path = 'avenue_dataset/testing_videos/'
videos = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]

video = random.choice(videos)
reader = imageio.get_reader(path + video)

n = reader.get_length()
i = random.randrange(0, n)
frame = reader.get_data(i)


vv.title('%s, frame %i' % (video, i))
vv.imshow(frame)
answer = input('normal ? (y/n) : ')
