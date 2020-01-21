from distutils.core import setup
 
setup(
      name="NeuroSkyPy",
      packages=['NeuroSkyPy'],
      version="1.1",
      license="GNU General Public License v3.0",
      description="Library for interfacing with Neurosky's Mindwave EEG headset",
      author="Jorge Lopez Marcos",
      author_email="jlomar2005@hotmail.com",
      url="https://github.com/Jor-G-ete/NeuroSkyPy",
      download_url="https://github.com/Jor-G-ete/NeuroSkyPy/archive/v1.1.tar.gz",
      keyword=["python3.7", "NeuroSky", "graphics"],
      classifiers=[
            'Development Status :: 3 - Alpha',  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: GNU General Public License v3.0',  # Again, pick a license
            'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.7',
            ],
      )
