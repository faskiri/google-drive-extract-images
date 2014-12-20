import os
import re
import glob

def text(path):
  exp = re.compile(r'<[^>]+>')
  with open(path) as file:
    return ' '.join(exp.sub(' ', file.read()).split())

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
    with open('media/%s/manifest.xml' % d, 'w') as manifest_file:
      manifest_file.write('<Module>\n')

      meta.sort(lambda (s1, k1), (s2, k2): cmp (int(s1), int(s2)))

      for (slide, img) in meta:
        manifest_file.write(
          '  <LearningObject>\n'
          '    <TextToDisplay>%s</TextToDisplay>\n'
          '    <ImageToDisplay>%s</ImageToDisplay>\n'
          '  </LearningObject>\n' % (
                  text('media/%s/slide%s.xml' % (d, slide)),
                  img))
      manifest_file.write('</Module>')

import sys
getrels(sys.argv[1])
