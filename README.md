# LotusVis
No more paraview screen shots! This is a quick visualisation tool for Lotus simulations to use on or offline. Guarenteed to be quicker than paraview.

## Aims & Motivation
The aim of this module is to provide the grunt of the visualisation for Lotus where paraview takes too much time for simple checks.

The advantage of this module as opposed to paraview is that you can run it online as part of the post proceccing. The visualtisations also look much more professional and could go straight into a paper as a quick sketch of the fluid flow.

There is already a routine in Lotus that can print flow quantities to an image. However, this is solely online and you don't have much flexibility to change limits or axes to suit your visualisation aims.

## Code setup
`io.py` holds the procedure to read in the data and format to a numpy array. `flowfield.py` holds the base class that holds the values and flow quantities. `plot_flow.py` then holds the functions to plot the vorticity, pressure, and velocity magnitude.
Running `main.py` calls the three plot functions. You only need to parse your main length scale if you are already in the correct directory. You can pass it the filepath as a string if you are working from a different directory.

## Implementation
Install the package

	git clone https://github.com/J-Massey/lotusvis.git
	cd lotusvis
	sudo pip install -e .
	
Or on iridis

	git clone https://github.com/J-Massey/lotusvis.git
	cd lotusvis
	pip install --user -r requirements.txt
	pip install --user .

To dump the visualisations copy the function from `main.py` and add to the `run.py` script. It should be quick because all the files we're accessing will have been the most recently written and all of them should be cached in memory.

Make sure you are in the correct working directory and pop back up a directory after. I normally do something like:

	os.chdir(str(idx))
        fluid_vis(512)
        os.chdir('../.')

## To do
Deal better with multiple time instances
	 - Integrate animation option
	 - POD / DMD ?
	 
## Not going to do
Deal with `fort.9`; it's too variable with how you set it up, very simple and most of the time you're comparing with something else anyway.
