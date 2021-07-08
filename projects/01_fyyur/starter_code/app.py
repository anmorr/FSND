#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#
import json
import logging
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import * # git test
from flask_migrate import Migrate
import model

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#


app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# TODO: connect to a local postgresql database ------- DONE!


#----------------------------------------------------------------------------#
# Helper Methods
#----------------------------------------------------------------------------#
def postgres_list_to_py_list(src_list):
  """ Helper method to transform psql list to python list"""
  return src_list.genres.strip("}").strip("{").split(",")


def get_form_errors(form):
  for message in form.errors.keys():
    flash(form.errors[message][0])


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#



class Shows(db.Model):
    __tablename__ = 'shows'
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), primary_key=True)
    start_time = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Show venue_id={self.venue_id} artist_id={self.artist_id}>'


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    genres = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    website_link = db.Column(db.String(120))
    seeking_description = db.Column(db.String(120))
    looking_for_talent = db.Column(db.Boolean)

    def __repr__(self):
        return f'<Venue id={self.id} name={self.name} city={self.city} state={self.state} address={self.address} \
                  phone={self.phone} image_link={self.image_link} facebook_link={self.facebook_link} website_link={self.website_link} seeking_description={self.seeking_description}\
                  looking_for_talent={self.looking_for_talent}>'

# #     # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    website_link = db.Column(db.String(120))
    facebook_link = db.Column(db.String(120))
    looking_for_venues = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))

    def __repr__(self):
        return f'<Artist id={self.id} name={self.name} city={self.city} state={self.state}\
                  phone={self.phone} image_link={self.image_link} genres={self.genres}, facebook_link={self.facebook_link} seeking_description={self.seeking_description}\
                  looking_for_venues={self.looking_for_venues}>'
    

#     # TODO: implement any missing fields, as a database migration using Flask-Migrate

# # TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  # 1. Query the DB for a list of all the venues.
  # 2. Iterate through the list and create list of dicts
  # 3. For each of the venues, query the list of shows where the date is after the current date
  # 
  venue_data = []
  venue_locations = {}
  venues = Venue.query.order_by('id').all()
  # print(venues)
  for venue in venues:
    venue_locations
    current_venue = {}
    current_venue["city"] = venue.city
    current_venue["state"] = venue.state
    current_venue["id"] = venue.id
    current_venue["name"] = venue.name
    current_venue["num_upcoming_shows"] = 0
    current_location = venue.city + venue.state
    if venue_locations.get(current_location):
      # print("=> Printing Venue_locations: "+ current_location + " " + str(venue_locations[current_location]))
      current_venue_details = {"id": current_venue["id"], "name" : current_venue["name"], "num_upcoming_shows": 0}
      venue_locations[current_location][0]["venues"].append(current_venue_details)
      print("=> Current Venue: " + str(venue_locations[current_location][0]["venues"]))
    else:
      venue_locations[current_location] = [{"city": current_venue["city"], "state": current_venue["state"], 
                                            "venues" : [{"id": current_venue["id"], "name" : current_venue["name"], "num_upcoming_shows": 0}]}]
      

  # print("**********" + str(venue_locations))

  # print("+++++++++++++++++++++++")
  for location in venue_locations.values():
    venue_data.append(location[0])
  # print(venue_data)
  return render_template('pages/venues.html', areas=venue_data)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  # print("Hello from the search button")
  
  try:
    response = {}
    search_term = request.form.get('search_term')
    search_term = "%" + search_term + "%"
    # print(search_term)
    venue_search_results = Venue.query.filter(Venue.name.ilike(search_term)).all()
    print(venue_search_results)

    if venue_search_results:
      response["count"] = len(venue_search_results)
      response["data"] =[]
      for venue in venue_search_results:
        response["data"].append(
          {"id": venue.id, 
          "name": venue.name,
          "num_upcoming_shows": 0,
          })
    print(response)
  except:
    flash("An error occurred while searching for " + search_term + ".")

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  current_venue = Venue.query.filter_by(id=venue_id).first()
  current_genres = postgres_list_to_py_list(current_venue)
  # current_genres = current_venue.genres.strip("}").strip("{").split(",")
  
  # print(current_genres)
  past_shows = []
  shows = Shows.query.filter_by(venue_id=venue_id).all()
  print(shows)
  if shows:
    for show in shows:
      current_artist = Artist.query.filter_by(id=show.artist_id).first()
      past_shows.append({
        "artist_id": current_artist.id,
        "artist_name": current_artist.name,
        "artist_image_link": current_artist.image_link,
        "start_time": str(show.start_time)
      })
  
  data1={
    "id": current_venue.id,
    "name": current_venue.name,
    "genres": current_genres,
    "address": current_venue.address,
    "city": current_venue.city,
    "state": current_venue.state,
    "phone": current_venue.phone,
    "website": current_venue.website_link,
    "facebook_link": current_venue.facebook_link,
    "seeking_talent": current_venue.looking_for_talent,
    "seeking_description": current_venue.seeking_description,
    "image_link": current_venue.image_link,
    "past_shows_count": len(past_shows),
    "past_shows": past_shows,
    "upcoming_shows_count": len(past_shows),
    "upcoming_shows": past_shows
    }
  return render_template('pages/show_venue.html', venue=data1)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  current_genres = []
  try:
    form = VenueForm()
    current_genres = form.genres.data
    # for item,val in request.form.items():
    #   print(item, val)
    if form.validate_on_submit():
      name = form.name.data 
      city = form.city.data
      state = form.state.data
      address = form.address.data
      phone = form.phone.data
      image_link = form.image_link.data
      if not image_link:
        image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
      print("Image Link: " + image_link)
      genres = current_genres
      # print("=========== > Genres: " + genres)
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      print(website_link)
      seeking_description = form.seeking_description.data 
      looking_for_talent = form.seeking_talent.data
      # TODO: modify data to be the data object returned from db insertion
      current_venue = Venue(name=name,city=city,state=state,address=address,phone=phone,image_link=image_link, genres=genres, facebook_link=facebook_link,seeking_description=seeking_description,website_link=website_link, looking_for_talent=looking_for_talent)
      # TODO: insert form data as a new Venue record in the db, instead  
      print(current_venue)
      db.session.add(current_venue)
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + request.form['name'] + ' was successfully listed!')
      return redirect(url_for('index'))
  except:
        db.session.rollback()
  finally:
        db.session.close()
  # print(form.errors)
  # TODO: on unsuccessful db insert, flash an error instead.
  flash('An error occurred. Venue ' + form.name.data + ' could not be listed.')
  # for message in form.errors.keys():
  #   flash(form.errors[message][0])
  get_form_errors(form)
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  artists = Artist.query.all()
  print(artists)
  data = []
  for artist in artists:
    data.append({"id": artist.id, "name": artist.name})
  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  try:
    response = {}
    search_term = request.form.get('search_term')
    search_term = "%" + search_term + "%"
    artist_search_results = Artist.query.filter(Artist.name.ilike(search_term)).all()
    print(artist_search_results)

    if artist_search_results:
      response["count"] = len(artist_search_results)
      response["data"] =[]
      for artist in artist_search_results:
        response["data"].append(
          {"id": artist.id, 
          "name": artist.name,
          "num_upcoming_shows": 0,
          })
    print(response)
  except:
    flash("An error occurred while searching for " + search_term + ".")
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id


  current_artist = Artist.query.filter_by(id=artist_id).first()
  print(current_artist)
  print(current_artist.genres)
  # current_genres = postgres_list_to_py_list(current_artist.genres)
  
  current_genres = current_artist.genres.strip("}").strip("{").split(",")
  print(current_genres)
  # print(current_genres)
  past_shows = []
  shows = Shows.query.filter_by(artist_id=artist_id).all()
  print(shows)
  if shows:
    for show in shows:
      current_venue = Venue.query.filter_by(id=show.venue_id).first()
      past_shows.append({
        "venue_id": current_venue.id,
        "venue_name": current_venue.name,
        "venue_image_link": current_venue.image_link,
        "start_time": str(show.start_time)
      })

  data={
    "id": current_artist.id,
    "name": current_artist.name,
    "genres": current_genres,
    "city": current_artist.city,
    "state": current_artist.state,
    "phone": current_artist.phone,
    "website": current_artist.website_link,
    "facebook_link": current_artist.facebook_link,
    "seeking_venue": current_artist.looking_for_venues,
    "seeking_description": current_artist.seeking_description,
    "image_link": current_artist.image_link,
    "past_shows_count": len(past_shows),
    "past_shows": past_shows,
    "upcoming_shows_count": len(past_shows),
    "upcoming_shows": past_shows
  }
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  # TODO: populate form with fields from artist with ID <artist_id>
  artist = {}
  
  try:
    form = ArtistForm()
    current_artist = Artist.query.filter_by(id=artist_id).first()
    print(current_artist)
    current_genres = postgres_list_to_py_list(current_artist)
    
    artist={
      "id": current_artist.id,
      "name": current_artist.name,
      "genres": current_genres,
      "city": current_artist.city,
      "state": current_artist.state,
      "phone": current_artist.phone,
      "website": current_artist.website_link,
      "facebook_link": current_artist.facebook_link,
      "seeking_venue": current_artist.looking_for_venues,
      "seeking_description": current_artist.seeking_description,
      "image_link": current_artist.image_link,
    }
    print(artist)
    # TODO: populate form with values from venue with ID <venue_id>
    form = ArtistForm(name=current_artist.name, city=current_artist.city, state=current_artist.state, 
                      genres=current_genres, website_link=current_artist.website_link, facebook_link=current_artist.facebook_link, 
                      seeking_talent=current_artist.looking_for_venues, seeking_description=current_artist.seeking_description,
                      image_link=current_artist.image_link)
  except:
        flash('An error occurred retrieving Artist with id ' + str(artist_id) + ' to the database.')
  finally:
        db.session.close()
  get_form_errors(form)
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  try:
    form = ArtistForm()
    if form.validate_on_submit():
      name = form.name.data
      city = form.city.data
      state = form.state.data 
      print(state)
      phone = form.phone.data
      image_link = form.image_link.data
      genres = form.genres.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
      print(seeking_description)
      
      current_artist = Artist(name=name,city=city, state=state, phone=phone, image_link=image_link, genres=genres,
                            facebook_link=facebook_link, website_link=website_link, looking_for_venues=seeking_venue,
                            seeking_description=seeking_description)
      db.session.add(current_artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully updated!')
  except:
        db.session.rollback()
        flash('An error occurred updating ' + form.name.data + ' to the database.')
  finally:
        db.session.close()
  get_form_errors(form)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  current_venue = Venue.query.filter_by(id=venue_id).first()
  current_genres = postgres_list_to_py_list(current_venue)
  
  venue={
    "id": current_venue.id,
    "name": current_venue.name,
    "genres": current_genres,
    "address": current_venue.address,
    "city": current_venue.city,
    "state": current_venue.state,
    "phone": current_venue.phone,
    "website": current_venue.website_link,
    "facebook_link": current_venue.facebook_link,
    "seeking_talent": current_venue.looking_for_talent,
    "seeking_description": current_venue.seeking_description,
    "image_link": current_venue.image_link,
  }
  # TODO: populate form with values from venue with ID <venue_id>
  form = VenueForm(name=current_venue.name, city=current_venue.city, state=current_venue.state, address=current_venue.address, 
                    genres=current_genres, website_link=current_venue.website_link, facebook_link=current_venue.facebook_link, 
                    seeking_talent=current_venue.looking_for_talent, seeking_description=current_venue.seeking_description,
                    image_link=current_venue.image_link)
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes

  try:
    current_venue = Venue.query.filter_by(id=venue_id).first()

    form = VenueForm()
    # print("I got to pre-validation!")
    if form.validate_on_submit():
      # print("I got to post-validation!")
      current_venue.name = form.name.data
      # print("======> " + form.name.data) 
      current_venue.city = form.city.data
      current_venue.state = form.state.data
      current_venue.address = form.address.data
      current_venue.phone = form.phone.data
      current_venue.image_link = form.image_link.data
      if not form.image_link.data:
        current_venue.image_link = "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80"
        
      print("Image Link: " + current_venue.image_link)
      current_venue.genres = form.genres.data
      # print("=========== > Genres: " + genres)
      current_venue.facebook_link = form.facebook_link.data
      current_venue.website_link = form.website_link.data
      print(current_venue.website_link)
      current_venue.seeking_description = form.seeking_description.data 
      current_venue.looking_for_talent = form.seeking_talent.data
      # TODO: modify data to be the data object returned from db insertion
      # TODO: insert form data as a new Venue record in the db, instead  
      print(current_venue)
      db.session.add(current_venue)
      db.session.commit()
      flash('Venue ' + form.name.data + ' was successfully updated!')
  except:
        db.session.rollback()
        flash('An error occurred updating ' + form.name.data + ' to the database.')
  finally:
        db.session.close()
  get_form_errors(form)
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

  try:
    form = ArtistForm()
    if form.validate_on_submit():
      name = form.name.data
      city = form.city.data
      state = form.state.data 
      print(state)
      phone = form.phone.data
      image_link = form.image_link.data
      if not image_link:
        image_link = "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"

      genres = form.genres.data
      facebook_link = form.facebook_link.data
      website_link = form.website_link.data
      seeking_venue = form.seeking_venue.data
      seeking_description = form.seeking_description.data
      print(seeking_description)
      
      current_artist = Artist(name=name,city=city, state=state, phone=phone, image_link=image_link, genres=genres,
                            facebook_link=facebook_link, website_link=website_link, looking_for_venues=seeking_venue,
                            seeking_description=seeking_description)
      db.session.add(current_artist)
      db.session.commit()
      flash('Artist ' + form.name.data + ' was successfully listed!')
      return redirect(url_for('index'))
  except:
        db.session.rollback()
  finally:
        db.session.close()

  # on successful db insert, flash success
  flash('An error occurred. Artist ' + form.name.data + ' could not be listed.')
  print(form.errors.keys())
  for message in form.errors.keys():
    flash(form.errors[message][0])
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  data = []
  list_of_shows = Shows.query.all()
  print(list_of_shows)
  if list_of_shows:
    for show in list_of_shows:
      current_venue = Venue.query.filter_by(id=show.venue_id).first()
      current_artist = Artist.query.filter_by(id=show.artist_id).first()
      data.append({
        "venue_id": current_venue.id,
        "venue_name": current_venue.name,
        "artist_id": current_artist.id,
        "artist_name": current_artist.name,
        "artist_image_link": current_artist.image_link,
        "start_time": str(show.start_time)
      })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():

  try:
    form = ShowForm()
    if form.validate_on_submit():
      artist_id = form.artist_id.data
      venue_id = form.venue_id.data
      start_time = form.start_time.data
  
      current_show = Shows(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
      print(current_show)
      db.session.add(current_show)
      db.session.commit()
      flash('Show was successfully listed!')
      return redirect(url_for('index'))
  except:
      db.session.rollback()
  finally:
      db.session.close()

  # on successful db insert, flash success
  flash('An error occurred. Show could not be listed.')
  print(form.errors.keys())
  for message in form.errors.keys():
    flash(form.errors[message][0])
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')




  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead

  # on successful db insert, flash success
  # flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  # return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Venue=Artist, Artist=Artist, Shows=Shows)

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
