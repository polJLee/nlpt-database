from flask import Flask, render_template, request, redirect, url_for
import datetime
import os
from sundays import sundays
from pyFunc import song_search, sunday_search, member_search, artist_search, roster_search, month_sunday_search, month_roster_search
from pyFunc import show_sunday, show_members, rewind
from pyFunc import add_member, add_sunday, add_roster
from pyFunc import numWeeks
from pyFunc import replace_song, add_song, remove_song, change_passage, change_title, remove_member

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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
def sundays_post():
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
              <a href="http://127.0.0.1:5000/sunday_result.html">
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <pre style="height=450px; width=200px;">"""
   text2 = f"""{searchResult}
            </pre>
            <form method="POST">
              <input type="text" name="sunday_search" size="50">
              <br>
              <br>
              <a href="http://127.0.0.1:5000/sunday_result.html">
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
      print(txt)
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <pre style="height=450px; width=200px;">
            """
   text2 = f"""{mthRoster}
            </pre>
            <form method= "POST">
               <input type="text" name="roster_search" size="50">
            <br>
            <a href="http://127.0.0.1:5000/roster_result.html">
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <pre style="height=450px; width=200px;">"""
   text2 = f"""{searchResult}
            </pre>
            <br>
            <form method= "POST">
               <input type="text" name="roster_search" size="50">
            <br>
            <br>
            <a href="http://127.0.0.1:5000/roster_result.html">
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
         return redirect(url_for('add_member_post'))
      elif request.form['button'] == 'Add Sunday':
         return redirect(url_for('add_sunday_post'))
      elif request.form['button'] == 'Add Roster':
         return redirect(url_for('add_month'))
   return render_template('add_options.html')

@app.route('/add_member.html', methods=['POST','GET'])
def add_member_post():
   if request.method == 'POST':
      result = add_member(request.form.get('member'), request.form.get('role'))
      
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Add Members</h2><form role="form" method="POST" action="">"""
      text2 = f"""
            <pre width="80" style="height:100px;">
               {result}
            </pre>
            <br>
            <br>
            <br>
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
            </div>"""
      text3 = """<div class="col-md-6 no-gutter text-center">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_member_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template('add_member_result.html')
   
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Add Members</h2>
                <p>
                    What's the name of the new members?
                </p>
                <form method='POST'>
                    <input type="text" name="member" size="50">
                    <br>
                  <p>
                     What's the role of this member?
                  </p>
                    <input type="text" name="role" size="50">
                    <br>
                  <a href="http://127.0.0.1:5000/add_member_result.html">
                     <button class="btn">Submit</button> 
                  </a>
               </form>
            
            <br>
            <br>
            <br>
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_member.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('add_member.html')

@app.route('/add_sunday.hmtl', methods=['POST','GET'])
def add_sunday_post():
   if request.method == 'POST':
      songs = []
      artists = []
      songs.append(request.form['song_1'])
      songs.append(request.form['song_2'])
      songs.append(request.form['song_3'])
      artists.append(request.form['artist_1'])
      artists.append(request.form['artist_2'])
      artists.append(request.form['artist_3'])
      rVal = add_sunday(request.form['date'], request.form['sermon_title'], request.form['passage'], songs, artists)
   
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
                </ul>
            </div>
            </div>
        </nav>
        <!-- Header -->

        <div class="span12">
            <div class="col-md-6 no-gutter text-center fill">
            <br>
            <br> 
            <h2 class="center">Add Sunday</h2>"""
      text2 = f"""<pre style="height:450px; width=200px;">
                  {rVal}
                  </pre>
                  <a href="http://127.0.0.1:5000/add.html">
                     <button class-"btn">Back</button>
                  </a>
                  </div>
                  """
      text3 = """<div class="col-md-6 no-gutter text-center">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_sunday_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("add_sunday_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
                </ul>
            </div>
            </div>
        </nav>
        <!-- Header -->

        <div class="span12">
            <div class="col-md-6 no-gutter text-center fill">
            <br>
            <br> 
            <h2 class="center">Add Sunday</h2>
                <form method='POST'>
                    <p>
                        Add Date in the form [dd.mm.yy]
                    </p>
                    <input type="text" name="date" size="50">
                    <br>
                    <p>
                        Add Sermon Title
                    </p>
                    <input type="text" name="sermon_title" size="50">
                    <br>
                    <p>
                        Add Passage
                    </p>
                    <input type="text" name="passage" size="50">
                    <br>
                    <p>
                        Song 1
                    </p>
                    <input type="text" name="song_1" size="50">
                    <p>
                        Artist 1
                    </p>
                    <input type="text" name="artist_1" size="50">
                    <p>
                        Song 2
                    </p>
                    <input type="text" name="song_2" size="50">
                    <p>
                        Artist 2
                    </p>
                    <input type="text" name="artist_2" size="50">
                    <p>
                        Song 3
                    </p>
                    <input type="text" name="song_3" size="50">
                    <p>
                        Artist 3
                    </p>
                    <input type="text" name="artist_3" size="50">
                    <br>
                    <br>
                    <a href="http://127.0.0.1:5000/add_member_result.html">
                        <button class="btn">Submit</button>
                    </a>
                </form>
            <br>
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_sunday.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('add_sunday.html')

@app.route('/add_month.html', methods=['POST','GET'])
def add_month():
   today = datetime.date.today()
   if request.method == 'POST':
      Months = {
                "January"   : 1,
                "February" : 2,
                "March"     : 3,   #Good Friday
                "April"     : 4,   #Good Friday
                "May"       : 5,
                "June"      : 6,    #Wintercon
                "July"      : 7,    #Wintercon
                "August"    : 8,
                "September" : 9,
                "October"   : 10,
                "November"  : 11,
                "December"  : 12    #Christmas
               }
      print(request.form.get('mText'))
      numWeek = numWeeks(request.form.get('mText')) 
      sundayList = sundays(int(Months[request.form.get('mText')]), today.year)
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
                </ul>
            </div>
            </div>
        </nav>
        <!-- Header -->

        <div class="span12">
            <div class="col-md-6 no-gutter text-center fill">
            <br>
            """
      text2 = """<br>
            <br>
            <br>
            <br>
            <a href="http://127.0.0.1:5000/add_roster_result.html">
               <button class="btn">Submit</button>
            </a>
            <br>
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
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
   
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_roster.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         i = 0
         while i < numWeek:
            sunday = sundayList[i]
            input = f"""<form method='POST'>
                  <p>
                     Enter Roster for {sunday}
                  </p>
                  
                  <div class="col-md-12">
                  <p>
                     Song Leader 1
                  </p>
                  <input type="text" name="SL1_{i+1}" size=30>
                  <p>
                     Song Leader 2
                  </p>
                  <input type="text" name="SL2_{i+1}" size=30>
                  <p>
                     Vocal
                  </p>
                  <input type="text" name="V_{i+1}" size=30>
                  <p>
                     Guitar 1
                  </p>
                  <input type="text" name="G1_{i+1}" size=30>
                  <p>
                     Guitar 2
                  </p>
                  <input type="text" name="G2_{i+1}" size=30>
                  <p>
                     Keys
                  </p>
                  <input type="text" name="K_{i+1}" size=30>
                  <p>
                     Drums
                  </p>
                  <input type="text" name="D_{i+1}" size=30>
                  <p>
                     Pads
                  </p>
                  <input type="text" name="P_{i+1}" size=30>
                  <br>
                </div>"""
            f.write(input)
            i += 1
         f.write(text2)
         f.close()
      
      return redirect(url_for('add_roster_post', variable=numWeek, mText = request.form.get('mText')))
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Add Roster</h2>
                <p>
                    Which Month would you like to put into the database?
                </p>
                <form method='POST'>
                    <input type="text" name="mText" size="50">
                    <br>
                    <button class="btn">Submit</button>
                </form>
            
            <br>
            <br>
            <br>
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_month.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('add_month.html')

@app.route('/add_roster.html', methods=['POST','GET'])
def add_roster_post():
   
   if request.method == 'POST':
      numWeek = int(request.args.get('variable'))
      month = request.args.get('mText')
      print(numWeek)
      print(month)
      
      song_leader1 = []
      song_leader2 = []
      vocal = []
      Guitar_1 = []
      Guitar_2 = []
      Keys = []
      Drums = []
      Pads = []
      
      i = 0
      while i < numWeek:
         song_leader1.append(request.form.get(f'SL1_{i+1}'))
         song_leader2.append(request.form.get(f'SL2_{i+1}'))
         vocal.append(request.form.get(f'V_{i+1}'))
         Guitar_1.append(request.form.get(f'G1_{i+1}'))
         Guitar_2.append(request.form.get(f'G2_{i+1}'))
         Keys.append(request.form.get(f'K_{i+1}'))
         Drums.append(request.form.get(f'D_{i+1}'))
         Pads.append(request.form.get(f'P_{i+1}'))
         i += 1
      results = add_roster(month, song_leader1, song_leader2, vocal, Guitar_1, Guitar_2, Keys, Drums, Pads)
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            """
      text2 = f"""<pre>
                     {results}
                  </pre>
                  <br>"""
      text3 = """
            <a href="http://127.0.0.1:5000/add.html">
                <button class="btn">Back</button>
            </a>
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
   
      with open('/Users/paullee/Downloads/nlpt-database/templates/add_roster_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template('add_roster_result.html')
   
   else:
      return render_template('add_roster.html')

@app.route('/rewind.html', methods=['POST','GET'])
def rewind_post():
   rw = rewind()
   text1 = """
   <!DOCTYPE html>
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
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                  <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Rewind</h2>
            <br>
            <pre style="height:500px;">"""
   text2 = f"""
            {rw}
            </pre>
            <br>
            <br>
         </div>



         <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
               <div id="headslide" class="carousel slide" data-ride="carousel">
                  <div class="carousel-inner" role="listbox">"""
   text3 = """
   <div class="item active"><img src="{{url_for('static',filename='rewind.jpg')}}" alt="Slide">
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
   
   with open('/Users/paullee/Downloads/nlpt-database/templates/rewind.html', 'w', encoding='utf-8') as f:
      f.write(text1)
      f.write(text2)
      f.write(text3)
      f.close()
   
   return render_template('rewind.html')

@app.route('/edit.html', methods=['POST','GET'])
def edit():
   if request.method == 'POST':
      txt = request.form.get('token')
      if txt == '2151':
         return redirect(url_for('edit_options'))
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
                <a href="http://127.0.0.1:5000/edit_options.html">
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
         with open('/Users/paullee/Downloads/nlpt-database/templates/edit.html', 'w', encoding='utf-8') as f:
            f.write(text1)
            f.write(text2)
            f.close()
         return render_template("edit.html")
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
                <a href="http://127.0.0.1:5000/edit_options.html">
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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

      with open('/Users/paullee/Downloads/nlpt-database/templates/edit.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.close()
      return render_template("edit.html")

@app.route('/edit_options.html', methods=['POST','GET'])
def edit_options():
   if request.method == 'POST':
      if request.form['button'] == 'Replace Song':
         return redirect(url_for('edit_replace_song'))
      elif request.form['button'] == 'Add Song':
         return redirect(url_for('edit_add_song'))
      elif request.form['button'] == 'Remove Song':
         return redirect(url_for('edit_remove_song'))
      elif request.form['button'] == 'Edit Passage':
         return redirect(url_for('edit_passage'))
      elif request.form['button'] == 'Edit Sermon Title':
         return redirect(url_for('edit_sermon_title'))
      elif request.form['button'] == 'Remove Member':
         return redirect(url_for('remove_member_edit'))
   return render_template('edit_options.html')   

@app.route('/edit_replace_song.html', methods=['POST','GET'])
def edit_replace_song():
   if request.method == 'POST':
      result = replace_song(request.form.get('date'), request.form.get('song_title'), request.form.get('r_title'), request.form.get('r_artist'))
      result = result + '\n' + sunday_search(request.form.get('date'))
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>
                <p>
                    Insert the Sunday that you would like to Edit in the form [dd.mm.yy]
                </p>
                <form method='POST'>
                    <input type='text' name = 'date' size='50'
                    <br>
                    <p>
                        Insert the title of the song you would like to replace
                    </p>
                    <input type='text' name = 'song_title', size='50'>
                    <br>
                    <p>
                        Insert the title of the new song below
                    </p>
                    <input type='text' name = 'r_title', size='50'>
                    <br>
                    <p>
                        Insert the artist of the new song below
                    </p>
                    <input type='text' name = 'r_artist', size='50'>
                    <br>

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_replace_song.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('edit_replace_song.html')

@app.route('/edit_add_song.html', methods=['POST','GET'])
def edit_add_song():
   if request.method == 'POST':
      result = add_song(request.form.get('date'), request.form.get('r_title'), request.form.get('r_artist'))
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Add Song</h2>
                <p>
                    Insert the Sunday that you would like to Edit in the form [dd.mm.yy]
                </p>
                <form method='POST'>
                    <input type='text' name = 'date' size='50'
                    <br>
                    <p>
                        Insert the title of the new song below
                    </p>
                    <input type='text' name = 'r_title', size='50'>
                    <br>
                    <p>
                        Insert the artist of the new song below
                    </p>
                    <input type='text' name = 'r_artist', size='50'>
                    <br>

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_add_song.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('edit_add_song.html')

@app.route('/edit_remove_song.html', methods=['POST','GET'])
def edit_remove_song():
   if request.method == 'POST':
      result = remove_song(request.form.get('date'), request.form.get('r_title'), request.form.get('r_artist'))
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Remove Song</h2>
                <p>
                    Insert the Sunday that you would like to Edit in the form [dd.mm.yy]
                </p>
                <form method='POST'>
                    <input type='text' name = 'date' size='50'
                    <br>
                    <p>
                        Insert the title of the song you would like to remove
                    </p>
                    <input type='text' name = 'r_title', size='50'>
                    <br>
                    <p>
                        Insert the artist of the song you would like to remove
                    </p>
                    <input type='text' name = 'r_artist', size='50'>
                    <br>

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_remove_song.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('edit_remove_song.html')

@app.route('/edit_passage.html', methods=['POST','GET'])
def edit_passage():
   if request.method == 'POST':
      result = change_passage(request.form.get('date'), request.form.get('passage'))
      
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Edit Passage</h2>
                <p>
                    Insert the Sunday that you would like to Edit in the form [dd.mm.yy]
                </p>
                <form method='POST'>
                    <input type='text' name = 'date' size='50'
                    <br>
                    <p>
                        Insert the new passage to replace the current passage
                    </p>
                    <input type='text' name = 'passage', size='50'>
                    <br>
                    

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_passage.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('edit_passage.html')

@app.route('/edit_sermon_title.html', methods=['POST','GET'])
def edit_sermon_title():
   if request.method == 'POST':
      result = change_title(request.form.get('date'), request.form.get('title'))
      
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Edit Sermon Title</h2>
                <p>
                    Insert the Sunday that you would like to Edit in the form [dd.mm.yy]
                </p>
                <form method='POST'>
                    <input type='text' name = 'date' size='50'
                    <br>
                    <p>
                        Insert the new title to replace the current sermon title
                    </p>
                    <input type='text' name = 'title', size='50'>
                    <br>
                    

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_sermon_title.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('edit_sermon_title.html')

@app.route('/remove_member.html', methods=['POST','GET'])
def remove_member_edit():
   if request.method == 'POST':
      result = remove_member(request.form.get('name'), request.form.get('role'))
      
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Replace Song</h2>"""
      text2 = f"""
      <pre style="height:450px;width=200px;">
         {result}
      </pre>
      <br>
      <br>
      <a href="http://127.0.0.1:5000/edit.html">
         <button class-"btn">Back</button>
      </a>
      </div>
      """
      text3 = """
      <div class="col-md-6 no-gutter text-center">
            <div id="header" data-speed="2" data-type="background">
                <div id="headslide" class="carousel slide" data-ride="carousel">
                    <div class="carousel-inner" role="listbox">
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      
      with open('/Users/paullee/Downloads/nlpt-database/templates/edit_result.html', 'w', encoding='utf-8') as f:
         f.write(text1)
         f.write(text2)
         f.write(text3)
         f.close()
      return render_template("edit_result.html")
   else:
      text = """<!DOCTYPE html>
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
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/edit.html">Edit</a></li>
                    <li class="nav-item"><a class="item-anchor" href="http://127.0.0.1:5000/rewind.html">Rewind</a></li>
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
            <h2 class="center">Remove Member</h2>
                <p>
                    Who would you like to remove from Praise Team?
                </p>
                <form method='POST'>
                    <input type='text' name = 'name' size='50'
                    <br>
                    <p>
                        What is their role?
                        Vocal | Vocal + Guitar | Vocal + Keys | Keys | Drum | Sound
                    </p>
                    <input type='text' name = 'role', size='50'>
                    <br>
                    

               <a href="http://127.0.0.1:5000/edit_result.html">
                  <button class="btn">Submit</button>
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
                        <div class="item active"><img src="{{url_for('static',filename='edit.jpg')}}" alt="Slide">
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
      with open('/Users/paullee/Downloads/nlpt-database/templates/remove_member.html', 'w', encoding='utf-8') as f:
         f.write(text)
         f.close()
      return render_template('remove_member.html')


if __name__ == '__main__':
  # bootstrap = Bootstrap(app)
  app.run (host= '0.0.0.0', port=5000, debug=True)