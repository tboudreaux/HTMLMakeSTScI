# HTMLMakeSTScI
Code to Generate HTML pages for summer STScI internship

<h2>Dependencies not in stdlib</h2>
-gPhoton
-matplotlib
-astropy
-plotly
-numpy
-scipy
<br>
<h2>How to Install Dependencies</h2>
<h3>Scipy</h3>
It is recommended that you install SciPy through anaconda, else:
- pip install git+https://github.com/scipy/scipy.git

<h3>Matplotlib</h3>
It is recommended that you install matplotlib through anaconda, else
<h4>Debian/ubuntu</h4>
- sudo apt-get build-dep python-matplotlib
<h4>Fedora</h4>
- su -c "yum-builddep python-matplotlib"
<h4>Other</h4>
- git clone git@github.com:matplotlib/matplotlib.git
- cd matplotlib
- python setup.py install
- edit shell profile to add matplotlib root folder to PYTHONPATH

<h3>Astropy</h3>
It is recommended that you install Astropy through anaconda, else:
- pip install --no-deps astropy

<h3>plotly</h3>
-pip install plotly 

<h3>numpy</h3>
It is recommended that you install numpy through anaconda, else:
<h4>Debina/Ubunut</h4>
-sudo apt-get install python-numpy
<h4>Fedora</h4>
- sudo yum install numpy
<h4>MacPorts</h4>
- sudo port install py27-numpy
<h4>Other</h4>
- git clone https://github.com/numpy/numpy.git
- cd numpy
- python setup.py install
- edit shell profile to add numpy root folder to PYTHONPATH
  - ex. 'PYTHONPATH="$PYTHONPATH:/home/RDanile/Downloads/numpy_build"'
