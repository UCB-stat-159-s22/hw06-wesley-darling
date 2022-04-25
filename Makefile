.PHONY: env
env:
	mamba env create -f environment.yml -p ~/envs/ligo
	bash -ic 'conda activate ligo;python -m ipykernel install --user --name ligo --display-name "IPython - ligo"'

html: 
	jupyter-book build .
	
	
html-hub:
	jupyter-book config sphinx .; sphinx-build  . _build/html -D html_baseurl=${JUPYTERHUB_SERVICE_PREFIX}/proxy/absolute/8000
	cd _build; cd html; python -m http.server

.PHONY : clean
clean :
	rm -f $(wildcard audio/*.wav)
	rm -f $(wildcard figures/*.png)
	# in case user selects to make PDF figures
	rm -f $(wildcard figures/*.pdf)
	rm -f $(wildcard data/*.csv)
	rm -f conf.py
	rm -rf _build
	rm -rf 