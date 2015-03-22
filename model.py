import os

import collections

LearningObject = collections.namedtuple(
  'LearningObject',
  ['text', 'image'])

class Model(object):
  def __init__(self, name):
    self._name = name
    self._objs = []

  def add_object(self, text, image):
    self._objs.append(LearningObject(text, image))

  def write(self):
    if not os.path.exists('xml'): os.mkdir('xml')

    path = 'xml/LearningObjectsModularList-%s.xml' % self._name
    with open(path, 'w') as manifest_file:
      manifest_file.write('<Modules>\n')
      manifest_file.write('  <Module>\n')
      manifest_file.write('    <ModuleName>%s</ModuleName>\n' % self._name)

      for o in self._objs:
        manifest_file.write(
          '    <LearningObject>\n'
          '      <TextToDisplay>%s</TextToDisplay>\n'
          '      <ImageToDisplay>%s</ImageToDisplay>\n'
          '    </LearningObject>\n' % (o.text, o.image))
      manifest_file.write('  </Module>\n')
      manifest_file.write('</Modules>')
