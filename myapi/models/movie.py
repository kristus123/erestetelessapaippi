from myapi.extensions import db
    
 
class movies(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(40))
	desc = db.Column(db.String(255), nullable=False, default=False)
	category = db.Column(db.String(40), nullable=False, default=False)


	rental = db.relationship('rental_info', backref='rental_info', uselist=False)
 
class rental_info(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	movie = db.Column(db.Integer, db.ForeignKey('movies.id'))

	rented_by = db.Column(db.Integer,db.ForeignKey('user_v2.id'))


	rented_to_date   = db.Column(db.DateTime, nullable=False, default=False)