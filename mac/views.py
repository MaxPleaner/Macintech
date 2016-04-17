from django.shortcuts import render
from django.http import HttpResponse, Http404
from os import listdir, system
from jack import *
from forms import *
from django.views.decorators.csrf import csrf_protect

@csrf_protect
def landing(request):
	try:
		vaporsfile = open('vapors.txt', "r")
		vapors = int(vaporsfile.read())
	except ValueError:
		vapors = 0
		vaporsfile = open('vapors.txt', "w")
		vaporsfile.write(str(vapors))
	except IOError:
		vapors = 0
		vaporsfile = open('vapors.txt', "w")
		vaporsfile.write(str(vapors))
	vaporsfile.close()

	return render(request, 'mac/landing.html', {'vapors':vapors})

@csrf_protect
def result(request):
	if request.method != 'POST':
		raise Http404("No vaporwave found. Is vaporwave dead yet?")

	form = BandNameForm(request.POST)
	if form.is_valid():
		band = form.cleaned_data['band']
		VaporMain.gen_vapor(band)
	
	try:
		vaporsfile = open('vapors.txt', 'r+')
		vapors = int(vaporsfile.read()) + 1
	except IOError:
		vapors = 1
		vaporsfile = open('vapors.txt', 'w')
	vaporsfile.write(str(vapors))
	vaporsfile.close()

	band_dir = r'mac/templates/mac/' + band.lower()
	try:
		file_ls = listdir(band_dir)
	except OSError, err:
		system("echo $PWD")
		raise err
	try:
		img_link = [filename for file in file_ls if ("." in filename) and (".wav" not in filename)][0]
	except Exception:
		img_link = "vape_me.jpg"
	songname = [filename for file in file_ls if ".wav" in filename][0]
	songlink = band_dir + r'/' + songname
	
	return render(request, 'mac/results.html', {'img':img_link, 'songlink':songlink, 'songname':songname, 'vapors':vapors})
