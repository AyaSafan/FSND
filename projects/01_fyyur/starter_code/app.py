#----------------------------------------------------------------------------#
# Imports
from flask_migrate import Migrate
from datetime import datetime
import re
from itertools import groupby
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

# TODO: connect to a local postgresql database
migrate = Migrate(app, db)
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

   # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean, default = True, nullable=False)
    seeking_description = db.Column(db.String(500))

    #genres = db.relationship('Genre', secondary=venues_genres__association_table, backref=db.backref('venues'))
    
    shows = db.relationship('Show', backref = 'venue', lazy = True , cascade="all, delete-orphan" )



    def __repr__(self):
        return f'<({self.id}) {self.name}>'

    

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))

   # TODO: implement any missing fields, as a database migration using Flask-Migrate
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean, default = True, nullable=False)
    seeking_description = db.Column(db.String(500))

    #genres = db.relationship('Genre', secondary=artists_genres_association_table, backref=db.backref('artists'))

    shows = db.relationship('Show', backref = 'artist', lazy = True , cascade="all, delete-orphan" )

    def __repr__(self):
        return f'<({self.id}) {self.name}>'

   

class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable = False)    
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable = False)      
    start_time = db.Column(db.DateTime, default=datetime.utcnow , nullable = False)
    def __repr__(self):
        return f'<({self.id}) Artist:({self.artist_id}), Venue:({self.venue_id})>'

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

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
  venues = Venue.query.order_by(Venue.name).all() 
  data=[]

  def grouper( item ): 
    return item.city, item.state 

  for ( (city, state), items ) in groupby( venues, grouper ):
        
       data_venues =[]
       for item in items:
          
          num_upcoming_shows = 0 
          now = datetime.now()                    
          for show in item.shows:
            if show.start_time > now:
              num_upcoming_shows += 1
          
          data_venues.append({
                    "id": item.id,
                    "name": item.name,
                    "num_upcoming_shows": num_upcoming_shows
              })

       data.append({
         "city": city,
         "state": state,
         "venues": data_venues
        })
      
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  
  search_term = request.form.get('search_term', '')

  venues = Venue.query.filter(Venue.name.ilike('%' + search_term + '%')).all()  
  
  data = []
  now = datetime.now()
  for venue in venues:
    shows = venue.shows
    num_upcoming_shows = 0
    for show in shows:
      if show.start_time > now:
        num_upcoming_shows += 1

    data.append({
      "id": venue.id,
      "name": venue.name,
      "num_upcoming_shows": num_upcoming_shows  
    })

  response = {
        "count": len(data),
        "data": data
    }

  return render_template('pages/search_venues.html', results=response, search_term= search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):

    venue = Venue.query.get(venue_id)  
    if not venue:
      flash('Venue ID: ' + (str(venue_id)) + ' does not exist.')        
      return redirect(url_for('index'))

     
    upcoming_shows_count = 0   
    upcoming_shows = []
    past_shows_count = 0
    past_shows = []
    now = datetime.now()

    past_shows_objs = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time < now
    ). all()


    for obj in past_shows_objs:
      past_shows_count += 1
      past_shows.append({
                      "artist_id":  obj[1].artist_id,
                      "artist_name":  obj[0].name,
                      "artist_image_link":  obj[0].image_link,
                      "start_time": format_datetime(str( obj[1].start_time))
        })

    upcoming_shows_objs = db.session.query(Artist, Show).join(Show).join(Venue).\
    filter(
    Show.venue_id == venue_id,
    Show.artist_id == Artist.id,
    Show.start_time >= now
    ). all()

    for obj in upcoming_shows_objs:
      upcoming_shows_count += 1
      upcoming_shows.append({
                      "artist_id":  obj[1].artist_id,
                      "artist_name":  obj[0].name,
                      "artist_image_link":  obj[0].image_link,
                      "start_time": format_datetime(str( obj[1].start_time))
        })

        
    
    venue.genres = venue.genres.split(',')
    venue.phone = (venue.phone[:3] + '-' + venue.phone[3:6] + '-' + venue.phone[6:])
    venue.upcoming_shows_count = upcoming_shows_count
    venue.upcoming_shows = upcoming_shows
    venue.past_shows_count = past_shows_count
    venue.past_shows = past_shows     

  
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    address = form.address.data.strip()
    phone = re.sub('\D', '', form.phone.data) 
    image_link = form.image_link.data.strip()    
    facebook_link = form.facebook_link.data.strip()

    website = form.website.data.strip()
    seeking_talent = form.seeking_talent.data
    seeking_description = form.seeking_description.data.strip()

    genres_list = form.genres.data               

    genres = ",".join(genres_list)
               
    
    if not form.validate():
        flash( form.errors )
        return redirect(url_for('create_venue_form'))

    else:
        Error = False
        try:
            venue_obj = Venue(name=name, city=city, state=state, address=address, phone=phone, genres = genres,  image_link=image_link, facebook_link=facebook_link , website=website , seeking_talent=seeking_talent, seeking_description=seeking_description)
            db.session.add(venue_obj)
            db.session.commit()
        except Exception as e:
            Error = True
            db.session.rollback()
        finally:
            db.session.close()
            
        if not Error:
            flash('Venue ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))
        else:
            flash('An error occurred. Venue ' + name + ' could not be listed.')
            return redirect(url_for('index'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  success = True
  try:
    venue = Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()
  except:
    db.session.rollback()
    success = False
  finally:
    db.session.close()
  return jsonify({ 'success': success,  'url': url_for('venues') })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.order_by(Artist.name).all()  

  data = []
  for artist in artists:
        data.append({
            "id": artist.id,
            "name": artist.name
        })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')

  artists = Artist.query.filter(Artist.name.ilike('%' + search_term + '%')).all()  
  
  data = []
  now = datetime.now()
  for artist in artists:
    shows = artist.shows
    num_upcoming_shows = 0
    for show in shows:
      if show.start_time > now:
        num_upcoming_shows += 1

    data.append({
      "id": artist.id,
      "name": artist.name,
      "num_upcoming_shows": num_upcoming_shows  
    })

  response = {
        "count": len(data),
        "data": data
    }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist = Artist.query.get(artist_id)   
  if not artist:
    flash('Artist ID: ' + (str(artist_id)) + ' does not exist.')        
    return redirect(url_for('index'))

 
  upcoming_shows_count = 0   
  upcoming_shows = []
  past_shows_count = 0
  past_shows = []
  now = datetime.now()

  past_shows_objs = db.session.query(Venue, Show).join(Show).join(Artist).\
  filter(
  Show.venue_id == Venue.id,
  Show.artist_id == artist_id,
  Show.start_time < now
  ). all()


  for obj in past_shows_objs:
    past_shows_count += 1
    past_shows.append({
                    "venue_id": obj[1].venue_id,
                    "venue_name": obj[0].name,
                    "venue_image_link": obj[0].image_link,
                    "start_time": format_datetime(str(obj[1].start_time))
      })

  upcoming_shows_objs = db.session.query(Venue, Show).join(Show).join(Artist).\
  filter(
  Show.venue_id == Venue.id,
  Show.artist_id == artist_id,
  Show.start_time >= now
  ). all()

  for obj in upcoming_shows_objs:
    upcoming_shows_count += 1
    upcoming_shows.append({
                    "venue_id": obj[1].venue_id,
                    "venue_name": obj[0].name,
                    "venue_image_link": obj[0].image_link,
                    "start_time": format_datetime(str(obj[1].start_time))
      })

  artist.genres = artist.genres.split(',')
  artist.phone = (artist.phone[:3] + '-' + artist.phone[3:6] + '-' + artist.phone[6:])
  artist.upcoming_shows_count = upcoming_shows_count
  artist.upcoming_shows = upcoming_shows
  artist.past_shows_count = past_shows_count
  artist.past_shows = past_shows     

  return render_template('pages/show_artist.html', artist=artist)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist = Artist.query.get(artist_id)   
  if not artist:
    flash('Artist ID: ' + (str(artist_id)) + ' does not exist.')        
    return redirect(url_for('index'))
  else:
    artist.phone = (artist.phone[:3] + '-' + artist.phone[3:6] + '-' + artist.phone[6:]) 
    artist.genres = artist.genres.split(',')
    return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  form = ArtistForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  phone = re.sub('\D', '', form.phone.data) 
  image_link = form.image_link.data.strip()    
  facebook_link = form.facebook_link.data.strip()

  website = form.website.data.strip()
  seeking_venue = form.seeking_venue.data
  seeking_description = form.seeking_description.data.strip()

  genres_list = form.genres.data          

  genres = ",".join(genres_list)
    
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('edit_artist_submission', artist_id=artist_id))

  else:
    Error = False

    try:
      artist = Artist.query.get(artist_id)

      artist.name = name
      artist.city = city
      artist.state = state
      artist.phone = phone
      artist.image_link = image_link
      artist.facebook_link = facebook_link      
            
      artist.website = website
      artist.seeking_venue = seeking_venue
      artist.seeking_description = seeking_description
      artist.genres = genres 
          
      db.session.commit()
    except Exception as e:
      Error = True
      db.session.rollback()
    finally:
      db.session.close()

    if not Error:
      flash('Artist ' + request.form['name'] + ' was successfully updated!')
    else:
      flash('An error occurred. Artist ' + name + ' could not be updated.')

  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue = Venue.query.get(venue_id)  
  if not venue:
    flash('Venue ID: ' + (str(venue_id)) + ' does not exist.')        
    return redirect(url_for('index'))
  else:
    venue.phone = (venue.phone[:3] + '-' + venue.phone[3:6] + '-' + venue.phone[6:]) 
    venue.genres = venue.genres.split(',')
    return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  form = VenueForm()

  name = form.name.data.strip()
  city = form.city.data.strip()
  state = form.state.data
  address = form.address.data.strip()
  phone = re.sub('\D', '', form.phone.data) 
  image_link = form.image_link.data.strip()    
  facebook_link = form.facebook_link.data.strip()

  website = form.website.data.strip()
  seeking_talent = form.seeking_talent.data
  seeking_description = form.seeking_description.data.strip()

  genres_list = form.genres.data          

  genres = ",".join(genres_list)
    
  if not form.validate():
    flash( form.errors )
    return redirect(url_for('edit_venue_submission', venue_id=venue_id))

  else:
    Error = False

    try:
      venue = Venue.query.get(venue_id)

      venue.name = name
      venue.city = city
      venue.state = state
      venue.address= address
      venue.phone = phone
      venue.image_link = image_link
      venue.facebook_link = facebook_link      
            
      venue.website = website
      venue.seeking_talent = seeking_talent
      venue.seeking_description = seeking_description
      venue.genres = genres 
          
      db.session.commit()
    except Exception as e:
      Error = True
      db.session.rollback()
    finally:
      db.session.close()

    if not Error:
      flash('Venue ' + request.form['name'] + ' was successfully updated!')
    else:
      flash('An error occurred. Venue ' + name + ' could not be updated.')

  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
      
    form = ArtistForm()
    name = form.name.data.strip()
    city = form.city.data.strip()
    state = form.state.data
    phone = re.sub('\D', '', form.phone.data) 
    image_link = form.image_link.data.strip()    
    facebook_link = form.facebook_link.data.strip()

    website = form.website.data.strip()
    seeking_venue = form.seeking_venue.data
    seeking_description = form.seeking_description.data.strip()

    genres_list = form.genres.data               

    genres = ",".join(genres_list)
               
    
    if not form.validate():
        flash( form.errors )
        return redirect(url_for('create_artist_form'))

    else:
        Error = False
        try:
            artist_obj = Artist(name=name, city=city, state=state, phone=phone, genres = genres,  image_link=image_link, facebook_link=facebook_link , website=website , seeking_venue=seeking_venue, seeking_description=seeking_description)
            db.session.add(artist_obj)
            db.session.commit()
        except Exception as e:
            Error = True
            db.session.rollback()
        finally:
            db.session.close()

        if not Error:
            flash('Artist ' + request.form['name'] + ' was successfully listed!')
            return redirect(url_for('index'))
        else:
            flash('An error occurred. Artist ' + name + ' could not be listed.')
            return redirect(url_for('index'))

@app.route('/artists/<artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
  success = True
  try:
    artist = Artist.query.get(artist_id)
    db.session.delete(artist)
    db.session.commit()
  except:
    db.session.rollback()
    success = False
  finally:
    db.session.close()
  return jsonify({ 'success': success,  'url': url_for('artists') })

#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():    
  shows = Show.query.all()
  data = []
    
  for show in shows:
    data.append({
            "venue_id": show.venue.id,
            "venue_name": show.venue.name,
            "artist_id": show.artist.id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
    })
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  form = ShowForm()
  artist_id = form.artist_id.data.strip()
  venue_id = form.venue_id.data.strip()
  start_time = form.start_time.data

  artist = Artist.query.get(artist_id)   
  if not artist:
    flash('Artist ID: ' + (str(artist_id)) + ' does not exist.')        
    return redirect(url_for('index'))

  venue = Venue.query.get(venue_id)  
  if not venue:
    flash('Venue ID: ' + (str(venue_id)) + ' does not exist.')        
    return redirect(url_for('index'))

  Error = False
    
  try:
    show_obj = Show(artist_id=artist_id, venue_id=venue_id, start_time=start_time)
    db.session.add(show_obj)
    db.session.commit()
  except:
    Error = True
    db.session.rollback()
  finally:
    db.session.close()

    if Error:
      flash(f'An error occurred.  Show could not be listed.')
    else:
      flash('Show was successfully listed!')
  return redirect(url_for('index'))
    
    

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
