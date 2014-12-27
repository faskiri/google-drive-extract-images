import os
import re
import glob
import model

def text(path):
  exp = re.compile(r'<[^>]+>')
  with open(path) as file:
    txt = []
    for e in exp.sub(' ', file.read()).split():
      if 'style.visibility' in e: continue
      txt.append(e)
    return ' '.join(txt)

def getrels(root):
  sre = re.compile('image(\d*)\.')
  pre = re.compile('media/(.*)/slide([0-9]*).xml.rels')
  manifest = {}
  for i in glob.glob(os.path.join(root, 'media/*/slide[0-9]*.xml.rels')):
    with open(i) as f:
      for m in sre.finditer(f.read()):
        d, slide = pre.search(i).groups()
        imgnum = m.groups()[0]
        img = glob.glob(os.path.join(
          root,
          'media/%s/image%s.*' % (d, imgnum)))[0]

        m = manifest.get(d, [])
        m.append((slide, img))
        manifest[d] = m

  for d, meta in manifest.iteritems():
    m = model.Model(d)
    meta.sort(lambda (s1, k1), (s2, k2): cmp (int(s1), int(s2)))

    for (slide, img) in meta:
      m.add_object(
          text=text('media/%s/slide%s.xml' % (d, slide)),
          image=os.path.basename(img))

import sys
getrels(sys.argv[1])
