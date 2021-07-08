from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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