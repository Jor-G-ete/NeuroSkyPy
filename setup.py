from setuptools import setup

version = "1.3"

setup(
      name="NeuroSkyPy",
      packages=['NeuroSkyPy'],
      version=version,
      license="GNU General Public License v3.0",
      description="Library for interfacing with Neurosky's Mindwave EEG headset",
      author="Jorge Lopez Marcos",
      author_email="jlomar2005@hotmail.com",
      url="https://github.com/Jor-G-ete/NeuroSkyPy",
      download_url="https://github.com/Jor-G-ete/NeuroSkyPy/archive/v"+version+".tar.gz",
      project_urls={
            "Documentation":"",
            "Source Code":""
      },
      platforms="Windows",
      keywords=["python3.7", "NeuroSky", "graphics", "threads"],
      install_requires=[
            'json',
            'numpy',
            'scikit-learn',
            'matplotlib',
            'pyserial',
            'pyyaml'
      ],
      classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',  # Define that your audience are developers
            'Topic :: Software Development :: Build Tools',
            "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
            'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
            'Programming Language :: Python :: 3.7',
            "Natural Language :: English",
            "Natural Language :: Spanish",
            "Operating System :: Microsoft :: Windows :: Windows 10",
            "Topic :: Scientific/Engineering :: Medical Science Apps."
            ],
      python_requires=">=3.7",
      )
