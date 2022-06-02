#!/usr/bin/python3

# SPDX-FileCopyrightText: https://github.com/tomba/kmsxx project authors
# SPDX-FileCopyrightText: 2022 Roman Stratiienko <r.stratiienko@gmail.com>
# SPDX-License-Identifier: MPL-2.0

import pykms
import time
import numpy as np

card = pykms.Card()
res = pykms.ResourceManager(card)
conn = res.reserve_connector('')
crtc = res.reserve_crtc(conn)

format = pykms.PixelFormat.XRGB8888
green = pykms.RGB(0, 255, 0)
black = pykms.RGB(0, 0, 0)

card.disable_planes()

mode = conn.get_default_mode()
modeb = mode.to_blob(card)
req = pykms.AtomicReq(card)
req.add(conn, "CRTC_ID", crtc.id)
req.add(crtc, {"ACTIVE": 1,
               "MODE_ID": modeb.id})
r = req.commit_sync(allow_modeset = True)
assert r == 0, "Initial commit failed: %d" % r

fbX = mode.hdisplay
fbY = mode.vdisplay

fb_full = pykms.DumbFramebuffer(card, fbX, fbY, format);
pykms.draw_rect(fb_full, int(fbX*0.1), int(fbY*0.1), int(fbX*0.8), int(fbY*0.8), green)
pykms.draw_rect(fb_full, int(fbX*0.2), int(fbY*0.2), int(fbX*0.6), int(fbY*0.6), black)

fbX = int(fbX/2)
fbY = int(fbY/2)

fb_half = pykms.DumbFramebuffer(card, fbX, fbY, format);
pykms.draw_rect(fb_half, int(fbX*0.1), int(fbY*0.1), int(fbX*0.8), int(fbY*0.8), green)
pykms.draw_rect(fb_half, int(fbX*0.2), int(fbY*0.2), int(fbX*0.6), int(fbY*0.6), black)

max_planes=16

frame_time = 1 / mode.vrefresh

toggle = False

# First plane is VI plane
vi_plane = res.reserve_generic_plane(crtc)

card.disable_planes()
for i in np.linspace(0.0, frame_time*0.8, num=360):
	time.sleep(i)

	req = pykms.AtomicReq(card)
	req.add_plane(vi_plane, fb_full if toggle else fb_half, crtc, dst=(0, 0, mode.hdisplay, mode.vdisplay), zpos=0)

	toggle = not toggle

	r = req.commit_sync()
	assert r == 0, "Plane commit failed: %d" % r
