# PyOrbit3 package installation

## 0. Required software

One needs compilers and python development packages, depending on  Linux flavor the package can be called **python-dev** or **python-devel**.

This guide was tested on following configurations

| CPU           | Architecture | OS           | Python  | Compiler     |
|---------------|--------------|--------------|---------|--------------|
| Intel i7-7700 | x86_64       | RHEL 8.7     | 3.9.13  | gcc-8.5      |
|               | x86_64       | Arch         | 3.10.10 | gcc-12.2.1   |
| Apple M2      | arm64        | macOS 13.3.1 | 3.9.6   | clang-14.0.3 |


## 1. Installation from source

First step is to clone the source code:

```bash
git clone https://github.com/PyORBIT-Collaboration/PyORBIT3.git
```

Make sure you have a C++ compiler.

On Debian based distributions:
```
sudo apt-get update
sudo apt-get install build-essential
```

On RedHat based distributions
```
sudo yum update
sudo yum group install "Development Tools"
```

You will also need to install the relevant packages in order to use PyOrbit. You can either do this through conda, or by installing the packages with your preferred package manager.

### Conda Setup (Recommended):

First of all make sure you have conda installed. Then run the following:

```bash
cd pyorbit3
conda env create -n pyorbit --file environment.yml
conda activate pyorbit
```

On macOS, you also need to install the `compilers` conda package if you want MPI support:
```bash
conda install -c conda-forge compilers
```

### Manual Setup:

Make sure that you have the correct python version installed. We require python=3.10. Further the following packages are required, use your preferred packet manager to install them:

- FFTW
- Matplotlib
- Numpy & Scipy
- Mpich

On Debian based distributions:
```
sudo apt-get install python-dev libmpich-dev mpich  zlib1g-dev libfftw3-dev
```

On RedHat based distributions
```
sudo yum install python-devel mpich mpich-devel zlib-devel fftw-devel
```

Then install the Python dependencies using PIP:
```
pip install numpy scipy matplotlib
```

For both of these methods these are the minimum requirements you need to run the examples. Additional packages will be required if you would like to modify and deploy to GitHub. These packages are pre-commit, flake8 and pytest to name a few.

## 2. Build

After you have installed everything, the next step is to build. In order to build the project, navigate to the root pyorbit directory and run the following:

```bash
python setup.py clean --all
pip install .
```

By default you do not compile with MPI enabled. To compile with MPI, set CC and CXX environment variables for the pip command:

```bash
CC=mpicc CXX=mpicxx pip install .
```

You need only build the project after a change is made to the core c++ or python classes.

## 3. Run SNS linac example

Navigate to your examples directory:

```bash
cd examples/SNS_Linac/pyorbit3_linac_model/
python pyorbit3_sns_linac_mebt_hebt2.py
```

Additionally if you would like to run the example on multiple MPI nodes you can use the following:

```bash
mpirun -n 4 python pyorbit3_sns_linac_mebt_hebt2.py
```

In the above line you can change the number 4 for however many MPI nodes you would like to test it on.

# Structure
**./src**		- source code for the core ORBIT C++ classes, including
		  wrappers, etc.

**./py**		- python modules and wrapper classes for the core ORBIT
		  classes.

**./ext**		- source code for external modules. Compilations of this
		  code should be placed into **./lib**.

**./lib**  	- .so shared libraries to be used under pyORBIT interpreter.

**./examples**		- pyORBIT3 examples.

**./tests**		- pytests written for the CI Pipeline.
