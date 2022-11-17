from flask import Flask, render_template, request
import os
from pyFunc import song_search, sunday_search, member_search, artist_search, roster_search


# Defined Globals
TEMPLATE_DIR = os.path.abspath('/Users/paullee/Downloads/nlpt-database/templates')
STATIC_DIR = os.path.abspath('/Users/paullee/Downloads/nlpt-database/templates/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')


@app.route('/search.html', methods=['POST', 'GET'])
def search_post():
  if request.method == 'POST':
    txt = request.form.get('search')
    member = member_search(txt)
    song = song_search(txt)
    artist = artist_search(txt)
    
    if txt.startswith(('1','2','3','4','5','6','7','8','9','0')):
      sunday = sunday_search(txt)
      if sunday.startswith(txt):
        search_result(sunday)
      return render_template('search_result.html')

    if not song.startswith("No songs matching") and not song.startswith("No title included"):
      search_result(song)
      return render_template('search_result.html')
    if member.startswith("\nMember Name"):
      roster = roster_search(txt)
      search_result(member + '\n\nRoster for the month\n' + roster)
      return render_template('search_result.html')
    if artist.startswith('\nArtist'):
      search_result(artist)
      return render_template('search_result.html')
    else:
      search_result("\nNo Result")
      return render_template('search_result.html')
    
  return render_template('search.html')  

@app.route('/sundays.html')
def sundays():
  return render_template('sundays.html')

@app.route('/members.html')
def members():
  return render_template('members.html')

@app.route('/roster.html')
def roster():
  return render_template('roster.html')


def search_result(searchResult):
      
  
  text1 = """<!DOCTYPE html>
<html lang="en">
   <head>
      <meta charset="utf-8">
      <meta http-equiv="X-UA-Compatible" content="IE=edge">
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <meta name="description" content="">
      <meta name="author" content="">
      <title>NLPT22</title>
      <!-- Css -->
      <link rel="stylesheet" href="{{ url_for('static',filename='bootstrap.css') }}">
      <link rel="stylesheet" href="{{ url_for('static',filename='style.css') }}">
   </head>
   <body>
      <nav class="navbar navbar-default navbar-fixed-top">
         <div class="col-md-12">
            <div class="nav">
               <button class="btn-nav">
               <span class="icon-bar inverted top"></span>
               <span class="icon-bar inverted middle"></span>
               <span class="icon-bar inverted bottom"></span>
               </button>
            </div>
            <a class="navbar-brand" href="http://127.0.0.1:5000/">
            <img class="logo" src="{{url_for('static', filename='logo.png')}}" alt="logo">
            </a>
            <div class="nav-content hideNav hidden">
               <ul class="nav-list vcenter">
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/">Home</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/search.html">Search</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/sundays.html">Sundays</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/members.html">Members</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/roster.html">Roster</a></li>
               </ul>
            </div>
         </div>
      </nav>
      <!-- Header -->
 
      <div class="span12">
         <div class="col-md-6 no-gutter text-center fill">
            <br>
            <br>
            <br>
            <br>
            <br>
            <br> 
            <a href="http://127.0.0.1:5000/search.html">
            <h2 class="center">Search</h2>
            </a>
            <br>
			  <pre width="80" style="height:1000px;">
			  """
  text2 = f"""{searchResult}
			  </pre>
			  <br>
			  <br>
			</div>
			<div class="col-md-6 no-gutter text-center">
			  <div id="header" data-speed="2" data-type="background">
				 <div id="headslide" class="carousel slide" data-ride="carousel">
					<div class="carousel-inner" role="listbox">
					  <div class="item active">
		 """
  text3 = """<img src="{{ url_for('static',filename='search.jpg')}}" alt="Slide">
					  </div>
					</div>
				 </div>
			  </div>
			</div>
		 </div>
		 <div style="clear:both;"></div>
   <!-- script -->
		 <script src="{{url_for('static',filename='jquery.js') }}"> </script>
		 <script src="{{url_for('static',filename='bootstrap.min.js') }}"> </script> 
		 <script src="{{url_for('static',filename='menu-color.js') }}"> </script>
		 <script src="{{url_for('static',filename='modernizer.js') }}"> </script>
		 <script src="{{url_for('static',filename='script.js') }}"> </script>
	  </body>
	</html>"""
  with open('/Users/paullee/Downloads/nlpt-database/templates/search_result.html', 'w', encoding='utf-8') as f:
    f.write(text1)
    f.write(text2)
    f.write(text3)
    f.close()

if __name__ == '__main__':
  # bootstrap = Bootstrap(app)
  app.run(debug=True)