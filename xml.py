import os
import re
import glob

def text(path):
  exp = re.compile(r'<[^>]+>')
  with open(path) as file:
    return ' '.join(exp.sub(' ', file.read()).split())

def getrels(root):
  sre = re.compile('image(\d*)')
  pre = re.compile('media/(.*)/slide([0-9]*).xml.rels')
  for i in glob.glob(os.path.join(root, 'media/*/slide[0-9]*.xml.rels')):
    with open(i) as f:
      m = sre.search(f.read())
      if m:
        d, slide = pre.search(i).groups()
        imgnum = m.groups()[0]
        img = glob.glob(os.path.join(
          root,
          'media/%s/image%s.*' % (d, imgnum)))[0]
        print "<LearningObject><TextToDisplay> %s </TextToDisplay><ImageToDisplay> %s </ImageToDisplay></LearningObject>" % (
            text('media/%s/slide%s.xml' % (d, slide)),
            img)

import sys
getrels(sys.argv[1])
