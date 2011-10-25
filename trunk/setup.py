# -*- encoding: UTF-8 -*-
'''
Created on 20 Oct. 2011

@author: thierry
'''
from distutils.core import setup
setup(name='magen',
      version='0.1.0-SNAPSHOT',
      package_dir = {'': 'src'},
      packages=['maegen',
                'maegen.common',
                'maegen.core',
                'maegen.gui'],               
      scripts=['scripts/maegen'],
      package_data={'maegen': ['*.png','*.jpg']},      
      data_files=[('/usr/share/applications/hildon',['hildon/maegen.desktop']),
                  ('/usr/share/icons/hicolor/48x48/hildon',['hildon/icons/48x48/maegen.png']),
                  ('/usr/share/icons/hicolor/64x64/hildon',['hildon/icons/64x64/maegen.png'])],    
      author='Thierry Bressure',
      author_email='thierry@bressure.net',
      maintainer='Thierry Bressure',
      maintainer_email='caritang@bressure.net',
      url='http://blog.maegen.bressure.net',
      download_url='http://maegen.bressure.net',
      description='Maegen is a genealogical application for N900',
      long_description='Maegen let you to collect genealogical information on the go and export then in GEDCOM format',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          "Environment :: Handhelds/PDA's",          
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',          
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python'          
          ],

      )

