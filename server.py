from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
from pyFunc import song_search, sunday_search, member_search, artist_search, roster_search, month_sunday_search, month_roster_search
from pyFunc import show_sunday, show_members

# Defined Globals
TEMPLATE_DIR = os.path.abspath('/Users/paullee/Downloads/nlpt-database/templates')
STATIC_DIR = os.path.abspath('/Users/paullee/Downloads/nlpt-database/templates/static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

@app.route('/', methods=['GET'])
def index():
  return render_template('index.html')

@app.route('/search.html', methods=['POST','GET'])
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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


@app.route('/sundays.html', methods=['POST','GET'])
def sundays():
   sundayResult = show_sunday()
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <h2 class="center">Sundays</h2>
            <br>
            <pre style="height:450px; width=200px;">"""
   text2 = f"""{sundayResult}
            </pre>
            <form method="POST">
              <input type="text" name="sunday_search" size="50">
              <br>
              <br>
              <a href="http://127.0.0.1:5000/sunday_result.html"
                <button class="btn">Search</button>
              </a>
              
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">
                     <div class="item active">"""
   text3 = """ <img src="{{url_for('static',filename='praise.jpg')}}" alt="Slide">
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
  
  
   if request.method == 'POST':
      txt = request.form.get('sunday_search')
      if txt.startswith(('1','2','3','4','5','6','7','8','9','0')):
         sunday = sunday_search(txt)
         if sunday.startswith(txt):
            sunday_result(sunday)
         return render_template('sunday_result.html')
      else:
         monthSun = month_sunday_search(txt)
         sunday_result(monthSun)
         return render_template('sunday_result.html')

  
  
   with open('/Users/paullee/Downloads/nlpt-database/templates/sundays.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()
  
  
   return render_template('sundays.html')

def sunday_result(searchResult):
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <a href="http://127.0.0.1:5000/sundays.html">
            <h2 class="center">Sundays</h2>
            </a>
            <br>
            <pre style="height:450px; width=200px;">"""
   text2 = f"""{searchResult}
            </pre>
            <form method="POST">
              <input type="text" name="sunday_search" size="50">
              <br>
              <br>
              <a href="http://127.0.0.1:5000/sunday_result.html"
                <button class="btn">Search</button>
              </a>
              
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">"""
   text3 = """ <div class="item active"> <img src="{{url_for('static',filename='praise.jpg')}}" alt="Slide">
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

   with open('/Users/paullee/Downloads/nlpt-database/templates/sunday_result.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()
      
@app.route('/members.html')
def members():
   memberResult = show_members()
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <h2 class="center">Members</h2>
            <br>
            <pre style="height:450px; width=200px;">"""
   text2 = f"""{memberResult}
            <br>
            <br>
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">
                     <div class="item active">"""
   text3 = """<img src="{{url_for('static',filename='team.jpeg')}}" alt="Slide">
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
   
   with open('/Users/paullee/Downloads/nlpt-database/templates/members.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()
   
   return render_template('members.html')

@app.route('/roster.html', methods=['POST','GET'])
def roster():
   date = datetime.date.today()
   Months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
   mth = Months[date.month-1]
   mthRoster = month_roster_search(mth)

   if request.method == 'POST':
      txt = request.form.get('roster_search')
      if txt in Months or txt == 'all' or txt == 'All':
         searched_month = month_roster_search(txt)
         roster_result(searched_month)
         return render_template('roster_result.html')
      else:
         member_name = roster_search(txt)
         roster_result(member_name)
         return render_template('roster_result.html')
      
      
   
   
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <h2 class="center">Roster</h2>
            <pre style="height:450px; width=200px;">
            """
   text2 = f"""{mthRoster}
            </pre>
            <br>
            <form method= "POST">
               <input type="text" name="roster_search" size="50">
            <br>
            <br>
            <a href="http://127.0.0.1:5000/roster_result.html"
               <button class="btn">Search</button>
            </a>
            
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">
                     <div class="item active">"""
   text3 = """<img src="{{url_for('static',filename='roster.jpg')}}" alt="Slide">
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
  
   with open('/Users/paullee/Downloads/nlpt-database/templates/roster.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()
  
   return render_template('roster.html')

def roster_result(searchResult):
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <a href="http://127.0.0.1:5000/roster.html">
            <h2 class="center">Roster</h2>
            </a>
            <pre style="height:450px; width=200px;">"""
   text2 = f"""{searchResult}
            </pre>
            <br>
            <form method= "POST">
               <input type="text" name="roster_search" size="50">
            <br>
            <br>
            <a href="http://127.0.0.1:5000/roster_result.html"
               <button class="btn">Search</button>
            </a>
            
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">"""
   text3 = """<div class="item active"><img src="{{url_for('static',filename='roster.jpg')}}" alt="Slide">
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

   with open('/Users/paullee/Downloads/nlpt-database/templates/roster_result.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()

@app.route('/add.html', methods=['POST','GET'])
def add():
   if request.method == 'POST':
      txt = request.form.get('token')
      if txt == '2151':
         return redirect(url_for('add_options'))
      elif txt != '2151':
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <h2 class="center">Enter Passcode</h2>
            <pre width="80" style="height:50px;">"""
         text2 = """Try Again
         </pre>
         <form role="form" method="POST" action="">
                <div class="row my-4">
                    <div class="pinBox">
                        <input class="pinEntry" name="token" type=text maxlength=4 autocomplete=off >
                    </div>
                </div>
                <a href="http://127.0.0.1:5000/add_options.html">
                    <button class="btn">Enter</button>
                 </a>
            </form>
            <br>
            <br>
            <br>
            
            </div>

            <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='add.jpg')}}" alt="Slide">
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
         with open('/Users/paullee/Downloads/nlpt-database/templates/add.html', 'w', encoding='utf-8') as f:
            f.write(text1)
            f.write(text2)
            f.close()
         return render_template("add.html")
   else:
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/add.html">Add</a></li>
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
            <h2 class="center">Enter Passcode</h2>"""
      text2 = """<form role="form" method="POST" action="">
                <div class="row my-4">
                    <div class="pinBox">
                        <input class="pinEntry" name="token" type=text maxlength=4 autocomplete=off >
                    </div>
                </div>
                <a href="http://127.0.0.1:5000/add_options.html">
                    <button class="btn">Enter</button>
                 </a>
            </form>
            <br>
            <br>
            <br>
            
            </div>

            <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='add.jpg')}}" alt="Slide">
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

      with open('/Users/paullee/Downloads/nlpt-database/templates/add.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.close()
      
      return render_template("add.html")

@app.route('/add_options.html', methods=['POST','GET'])
def add_options():
   if request.method == 'POST':
      if request.form['button'] == 'Add Member':
         return redirect(url_for('add_member'))
      elif request.form['button'] == 'Add Sunday':
         return redirect(url_for('add_sunday'))
      elif request.form['button'] == 'Add Roster':
         return redirect(url_for('add_roster'))
   return render_template('add_options.html')

@app.route('/add_member.html', methods=['POST','GET'])
def add_member():
   return render_template('add_member.html')

@app.route('/add_sunday.hmtl', methods=['POST','GET'])
def add_sunday():
   return render_template('add_sunday.html')

@app.route('/add_roster.html', methods=['POST','GET'])
def add_roster():
   return render_template('add_roster.html')

if __name__ == '__main__':
  # bootstrap = Bootstrap(app)
  app.run(debug=True)