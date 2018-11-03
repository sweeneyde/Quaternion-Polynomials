# Quaternion-Polynomials

This project attempts to discover the structure of the quaternion roots of polynomials with quaternion coefficients.

* `quat_poly.py` implements [an algorithm by R.Serôdio, E.Pereira, and J.Vitória](http://www.sciencedirect.com/science/article/pii/S0898122101002358) to find the roots of arbitrary quaternion polynomials.
* `generate_roots_data.py` computes and stores the roots of those quaternion polynomials whose coefficients have a -1, 0 or +1 in each component, such as (1-1i+0j+1k).
* Once a file of roots has been generated, `data_visualizations.py` can be used to create 2D and 3D plots and histograms of the data by uncommenting/changing lines in the file.

Requirements:

* Python 3.7+
* The numpy package (`pip install numpy`)
* The pyquaternion package (`pip install pyquaternion`)
