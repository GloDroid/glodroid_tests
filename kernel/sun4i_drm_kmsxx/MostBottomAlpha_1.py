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

format = pykms.PixelFormat.ARGB8888
magenta = pykms.RGB(255, 0, 255)
grey = pykms.RGB(128, 255, 255, 255)

card.disable_planes()

mode = conn.get_default_mode()
modeb = mode.to_blob(card)
req = pykms.AtomicReq(card)
req.add(conn, "CRTC_ID", crtc.id)
req.add(crtc, {"ACTIVE": 1,
               "MODE_ID": modeb.id})
r = req.commit_sync(allow_modeset = True)
assert r == 0, "Initial commit failed: %d" % r

planes=[]

max_planes=16

for i in range(max_planes):
    p = res.reserve_generic_plane(crtc)
    if p == None:
        break
    planes.append(p)

fbX = int(mode.hdisplay / len(planes))
fbY = int(mode.vdisplay)

fb = pykms.DumbFramebuffer(card, fbX, fbY, format);
pykms.draw_rect(fb, 0, 0, int(fbX), int(fbY), grey)
pykms.draw_rect(fb, int(fbX*0.1), int(fbY*0.1), int(fbX*0.8), int(fbY*0.8), magenta)

def PlaneAlphaTest(plane_index):
	print("Plane {} is the most bottom".format(plane_index))
	req = pykms.AtomicReq(card)

	for p in range(0,len(planes)):
		req.add_plane(planes[p], fb, crtc, dst=(fbX * p, 0, fbX, fbY), zpos=(p-plane_index)%len(planes))
	r = req.commit_sync()

	for a in np.linspace(65535, 0, num=100):
		req = pykms.AtomicReq(card)

		for p in range(0,len(planes)):
			req.add(planes[p], {"alpha": int(a) })

		r = req.commit_sync()
		assert r == 0, "Plane commit failed: %d" % r

	print("Press enter to continue")
	input()

	req = pykms.AtomicReq(card)
	for p in range(0,len(planes)):
		req.add(planes[p], {"alpha": 65535 })
	r = req.commit_sync()

for i in range(0, len(planes)):
	PlaneAlphaTest(i)
