# LineupRecommender
All of our code can be run from updater.py. updater.py contains a class called DailyUpdate, with a function called get_todays_optimal_lineup(). What this function does is it prepares the csvs with all of the data that we are scraping from stats.nba.com and NumberFire and the data we are getting from the Stattleship API. It prepares all the necessary dictionaries from the csvs and runs the regressor in DailyProjector and obtains the projected scores for all the players playing today. Then it optimizes this lineup to get the best 9 players that would get the highest overall score. This is outlined in updater.py in step 0, 1, 2, and 3. 

*** IMPORTANT ***
To run our code without needing to comment out any of the steps, mainly the step involving optimization, it is necessary to install the following packages:
	
	- openopt. This can be done from the command line using the command "pip install openopt", or one can download it directly from https://pypi.python.org/pypi/openopt, and unzip the tar.gz file and run "python setup.py install" from inside the unzipped folder.

	- funcdesigner. Again this can be done from the command line with the phrase "pip install funcdesigner". One could also download it directly from https://pypi.python.org/pypi/FuncDesigner, unzip the tar.gz folder and run "python setup.py install" from inside the unzipped folder. 

	- glpk. This can be done from homebrew, the command line package installer. HOMEBREW MUST BE UPDATED BEFORE INSTALLING glpk. To install glpk using brew, run the command "brew install glpk" or "brew install homebrew/science/glpk". It is also possible to download it from http://www.gnu.org/software/glpk/glpk.html and run "python setup.py install" from inside the unzipped folder. Please make sure the version of the package installed is 4.60.

	- cvxopt. The package should be downloaded from http://cvxopt.org/install/. Unzip the folder and navigate inside of the unzipped folder. Three environment variables must be set to tell python where the unzipped folder is, where the glpk folder is, and to use it when using the package cvxopt. They must be set inside the unzipped cvxopt folder.

		- export CVXOPT_BUILD_GLPK=1
		- export CVXOPT_GLPK_LIB_DIR="path/to/glpk/4.60/lib" 
		   	in our case, it looked something like this:
		   		export CVXOPT_GLPK_LIB_DIR="/usr/local/Cellar/glpk/4.60/lib"
		- export CVXOPT_GLPK_INC_DIR="path/to/glpk/4.60/include"
			in our case, the command looked like this:
				export CVXOPT_GLPK_INC_DIR="/usr/local/Cellar/glpk/4.60/include"

	- the sklearn package should also be installed as we use that package in projecting the scores.

All of these packages are necessary to run the optimizer, which optimizes the lineup. To run our code without the optimizer, without the optimized lineup, one can simply comment out step 3 in updater.py.

After all the packages are installed, running "python updater.py" will run all of our code. 

Because we were unable to get our website, https://lineup-recommender.herokuapp.com/, to update every day because the optimizer packages refused to work on heroku, the optimizing must be done locally. Then to see our lineup, run "python app.py", which uses flask to render the front end, and the address, localhost:5000,  will display the webpage with the lineup locally. 

	- if one does not have the flask package installed, it is possible to install it using the command "pip install flask" or downloading it from https://pypi.python.org/pypi/Flask and unzipping it and running python setup.py install from inside the unzipped folder. 

It shows the player's team as an unknown team, but this is because it needs to be updated every day. 

We also use anaconda in setting up packages to use in our code. If one wants to use conda, it is downloadable from https://docs.continuum.io/anaconda/install. To create a conda environment run the command "conda create --name &lt;env&gt; --file &lt;this file&gt;", where &lt;env&gt; is the name of the environment and &lt;this file&gt; is conda-requirements.txt. Then to activate the environment, run "source activate &lt;env&gt;". All the packages used are in conda-requirements.txt. If one does not have all the packages listed there, it is recommended to use anaconda to set up the environment along with the packages mentioned above to run our code. 
