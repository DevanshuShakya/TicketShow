import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask import redirect
from flask import render_template
from flask import url_for
from flask import flash

current_dir=os.path.abspath(os.path.dirname(__file__))

db = SQLAlchemy()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(current_dir,"database.sqlite3")
db.init_app(app)
app.app_context().push()

# defining models

class User(db.Model):
    __tablename__='user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String,unique=True, nullable=False)
    password=db.Column(db.String, nullable=False )

class Admin(db.Model):
    __tablename__='admin'
    admin_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_name = db.Column(db.String, nullable=False)
    admin_password=db.Column(db.String, nullable=False )

class Venue(db.Model):
    __tablename__='venue'
    venue_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    venue_name=db.Column(db.String, nullable=False)
    place=db.Column(db.String, nullable=False)
    location=db.Column(db.String, nullable=False)
    capacity=db.Column(db.Integer, nullable=False)

class AdminVenues(db.Model):
    __tablename__='admin_venues'
    av_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    av_admin_id=db.Column(db.Integer,db.ForeignKey("admin.admin_id"))
    av_venue_id=db.Column(db.Integer,db.ForeignKey("venue.venue_id"))

class Show(db.Model):
    __tablename__='show'
    show_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    show_name=db.Column(db.String, nullable=False)
    rating=db.Column(db.Float, nullable=False)
    appt1=db.Column(db.Integer, nullable=False)
    appt2=db.Column(db.Integer, nullable=False)
    tags=db.Column(db.String, nullable=False)
    price=db.Column(db.Integer, nullable=False)

class VenueShows(db.Model):
    __tablename__='venue_shows'
    vs_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    vs_venue_id=db.Column(db.Integer, db.ForeignKey("venue.venue_id"))
    vs_show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"))

class UserShows(db.Model):
    __tablename__='user_shows'
    us_id=db.Column(db.Integer, primary_key=True, autoincrement= True)
    us_user_id=db.Column(db.Integer, db.ForeignKey("user.user_id"))
    us_show_id=db.Column(db.Integer, db.ForeignKey("show.show_id"))
    us_seats=db.Column(db.Integer, nullable=False)
    us_rating=db.Column(db.Integer)




@app.route("/")
def index():
    if request.method=="GET":
        return render_template("index.html")
    
    

@app.route('/user/register', methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template("register.html")
    
    elif request.method=='POST':
        users=User.query.all()
        name=request.form['name']
        password=request.form['password']

        for user in users:
            if name==user.username:
                flash('Username already exists.')
                return redirect('/user/register')

        

        user=User(username=name,password=password)
         
        db.session.add(user)
        db.session.flush()
        db.session.commit()
        return redirect("/user/login")


@app.route('/user/login', methods=['GET','POST'])
def user_login():
    if request.method=="GET":
        return render_template("user_login.html")
    elif request.method=='POST':
        users=User.query.all()
        # print(User)
        username=request.form['name']
        password=request.form['password']

        if users:
            flag=False
            for user in users:
                if username==user.username and password==user.password:
                        return redirect(url_for('user_dashboard',user_id=user.user_id))
                else:
                    flag=True
                   
                   
            if flag:
                flash('Please check your login details and try again.')
                return redirect('/user/login')
                
                   
        else:
            flash('Please check your login details and try again.')
            return redirect('/user/login')
        
        
        
                    
    

    
@app.route('/admin/login', methods=['GET','POST'])
def admin_login():
    if request.method=="GET":
        return render_template("admin_login.html")
    
    elif request.method=="POST":
        admins=Admin.query.all()
        admin_name=request.form['name']
        admin_password=request.form['password']
        for admin in admins:
            if admin_name==admin.admin_name:
                if admin_password==admin.admin_password:
                    # print(admin.admin_id)
                    return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))
            else:
                flash('Please check your login details and try again.')
                return redirect('/admin/login')
    
@app.route('/admin/<int:admin_id>/dashboard',methods=['GET','POST'])
def admin_dashboard(admin_id):
    if request.method=="GET":
        admin=Admin.query.get_or_404(admin_id)
        admin_venues=AdminVenues.query.filter(AdminVenues.av_admin_id==admin_id).all()

        if len(admin_venues)==0:
            return render_template("admin_dashboard_no_shows.html",admin=admin)
        
        venues=[]
        for admin_venue in admin_venues:
            venues.append(Venue.query.filter(Venue.venue_id==admin_venue.av_venue_id).all())
        # print(venues)
        # venue[0]

        # showspervenue=[]
        # venue_shows=[]

        all_venue_showList=[]
        for venue in venues:
            venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue[0].venue_id).all()
            # print(venue_shows)
            venue_showList=[]
            for venue_show in venue_shows:
                venue_showList.append(Show.query.filter(Show.show_id==venue_show.vs_show_id).all())

            # print(venue_showList)
            all_venue_showList.append(venue_showList)

        # print(all_venue_showList)
        # print(all_venue_showList[3])
        
        #     venue_shows.append([])

        #     for show in shows:
        #         venue_shows[shows.index(show)].append(Show.query.filter(Show.show_id==show.vs_show_id).all())
        #     print(shows)
            # showspervenue.append(shows)
        # print(shows)   
        # print(venue_shows)
        # print(showspervenue)
        # print(venue_shows)
        l=len(all_venue_showList)
        
        # for show in venue_shows:
        #     shows.append(Show.query.filter(Show.show_id==show.vs_show_id).all())

        return render_template("admin_dashboard.html",admin=admin,venues=venues,all_venue_showList=all_venue_showList,l=l)


    
    # elif request.method=='POST':

        
        
@app.route('/admin/<int:admin_id>/create_venue',methods=['GET','POST'])
def create_venue(admin_id):
    if request.method=='GET':
        admin=Admin.query.get_or_404(admin_id)
        return render_template('create_venue.html',admin=admin)
   
    elif request.method=='POST':
        venue_name=request.form['name']
        place=request.form['place']
        location=request.form['location']
        capacity=request.form['capacity']
        admin=Admin.query.get_or_404(admin_id)

        
        
        admin_venues=AdminVenues.query.filter(AdminVenues.av_admin_id==admin_id).all()
        venues=[]
        for admin_venue in admin_venues:
            venues.append(Venue.query.filter(Venue.venue_id==admin_venue.av_venue_id).all())
        # print(venues)

        # all_venues=Venue.query.all()
        for venue in venues:
            if venue_name==venue[0].venue_name:
                if place==venue[0].place:
                    if location==venue[0].location:
                        return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))     
                       
        venue=Venue(venue_name=venue_name,place=place,location=location,capacity=capacity)

        db.session.add(venue)
        db.session.flush()
        admin_venue=AdminVenues(av_admin_id=admin_id,av_venue_id=venue.venue_id)
        
        # print(venue.venue_id)        
        db.session.add(admin_venue)
        db.session.commit()       

        return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))

                    
@app.route('/admin/<int:admin_id>/<int:venue_id>/edit',methods=['GET','POST'])
def edit_venue(admin_id,venue_id):
    admin=Admin.query.get_or_404(admin_id)
    venue=Venue.query.get_or_404(venue_id)


    if request.method=='GET':
        return render_template("edit_venue.html",admin=admin,venue=venue)
    
    elif request.method=='POST':
        venue.venue_name=request.form['name']
        venue.place=request.form['place']
        venue.location=request.form['location']
        venue.capacity=request.form['capacity']

        db.session.commit()

        return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))
        
@app.route("/admin/<int:admin_id>/<int:venue_id>/delete")
def delete_venue(admin_id, venue_id):
    if request.method=='GET':
        # venue=Venue.query.get_or_404(venue_id)
        admin=Admin.query.get_or_404(admin_id)
        
        AdminVenues.query.filter(AdminVenues.av_venue_id==venue_id and AdminVenues.av_admin_id==admin_id).delete()
        # print('printing venue_id',venue_id)
        # print('printing admin_id',admin_id)
        # print(admin_venues)
        # db.session.delete(admin_venue)
        db.session.commit()
        return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))

@app.route("/admin/<int:admin_id>/<int:venue_id>/create_show",methods=['GET','POST'])
def create_show(admin_id,venue_id):
    admin=Admin.query.get_or_404(admin_id)
    venue=Venue.query.get_or_404(venue_id)
    if request.method=='GET':
        return render_template('create_show.html',admin=admin,venue=venue)
    
    if request.method=='POST':
        name=request.form['name']
        rating=request.form['rating']
        appt1=request.form['appt1']
        appt2=request.form['appt2']
        tags=request.form['tags']
        price=request.form['price']

        # print("tags",tags)
        # print("price",price)
        # print("appt1",appt1)
        # print("rating",rating)

        show=Show(show_name=name,rating=rating,appt1=appt1,appt2=appt2,tags=tags,price=price)

        db.session.add(show)
        db.session.flush()

        

        venue_show=VenueShows(vs_venue_id=venue_id,vs_show_id=show.show_id)
        db.session.add(venue_show)

        db.session.commit()

        # venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue_id).all()

        # shows=[]
        # # print(venue_shows)

        # for show in venue_shows:
        #     shows.append(Show.query.filter(Show.show_id==show.vs_show_id).all())

        # # print(shows)
    

        return redirect(url_for('admin_dashboard',admin_id=admin.admin_id))
    
@app.route('/admin/<int:admin_id>/<int:venue_id>',methods=['GET','POST'])
def venue(admin_id,venue_id):
    admin=Admin.query.get_or_404(admin_id)
    venue=Venue.query.get_or_404(venue_id)
    if request.method=='GET':

        venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue_id).all()
        print(venue_shows)
        
        shows=[]
        for venue_show in venue_shows:
            shows.append(Show.query.filter(Show.show_id==venue_show.vs_show_id).all())
        
        return render_template("venue.html",admin=admin,venue=venue,shows=shows)
    

@app.route('/admin/<int:admin_id>/<int:venue_id>/<int:show_id>/edit_show',methods=['GET','POST'])

def edit_show(admin_id,venue_id,show_id):

    if request.method=='POST':
        show=Show.query.get_or_404(show_id)
        # show.name=request.form['name']
        show.rating=request.form['rating']
        show.appt1=request.form['appt1']
        show.appt2=request.form['appt2']
        show.tags=request.form['tags']
        show.price=request.form['price']

        db.session.commit()

        return redirect(url_for('venue',admin_id=admin_id,venue_id=venue_id))


    
@app.route('/admin/<int:admin_id>/<int:venue_id>/<int:show_id>/delete_show',methods=['GET','POST'])
def delete_show(admin_id,venue_id,show_id):
    if request.method=='GET':
        VenueShows.query.filter(VenueShows.vs_show_id==show_id and VenueShows.vs_venue_id==venue_id ).delete()
        db.session.flush()
        Show.query.filter(Show.show_id==show_id).delete()
        db.session.commit()
        return redirect(url_for('venue',admin_id=admin_id,venue_id=venue_id))
    

    
@app.route('/user/<int:user_id>/dashboard',methods=['GET','POST','PUT'])

def user_dashboard(user_id):

    user=User.query.get_or_404(user_id)
    admin_venues=AdminVenues.query.all()
    venues=[]
    for admin_venue in admin_venues:
        venues.append(Venue.query.filter(Venue.venue_id==admin_venue.av_venue_id).all())
   
    for venue in venues:
        if venue==[]:
            venues.remove(venue)
    # print(venues)


    all_venue_showList=[]
    all_venue_showBSeats=[]
    all_venue_showFGenre=[]
    for venue in venues:
        venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue[0].venue_id).all()
        venue_showList=[]
        venue_showBSeats=[]
        venue_showFGenre=[]
        for venue_show in venue_shows:
            show=Show.query.filter(Show.show_id==venue_show.vs_show_id).all()
            venue_showList.append(show)
            show_seats=0
            F_genre=[]
            genre=show[0].tags
            genre_list=genre.split(',')
            F_genre=[]
            for tag in genre_list:
                # print(tag)
                # print(tag.capitalize())
                capitalized_tag=tag.title()
                capitalized_tag=capitalized_tag.strip(' ')
                F_genre.append(capitalized_tag)
            # print(F_genre)


            for user_show in UserShows.query.filter(UserShows.us_show_id==show[0].show_id).all():
                show_seats=show_seats+user_show.us_seats

            venue_showBSeats.append(show_seats)
            venue_showFGenre.append(F_genre)
            
        if venue_showList!=[]:
            all_venue_showList.append(venue_showList)
        
        if venue_showBSeats!=[]:
            all_venue_showBSeats.append(venue_showBSeats)

        if venue_showFGenre!=[]:
            all_venue_showFGenre.append(venue_showFGenre)

    # print(all_venue_showList)
    # print(all_venue_showFGenre)


    


    # print(all_venue_showBSeats)

    
    # left_seats=



    if request.method=='GET':
        return render_template('user_dashboard.html',user=user,venues=venues,all_venue_showList=all_venue_showList,all_venue_showBSeats=all_venue_showBSeats,all_venue_showFGenre=all_venue_showFGenre)
    
    elif request.method=='POST':
        seats=request.form['seats']
        details=request.form['details']

        # genre=request.form['genre']
        # print(genre)


        num_str = details.split('|')       # list of numbers represented as strings
        numbers = [ ]                   
        for item in num_str:
            numbers.append((item))   # append to list

       


       
        return redirect(url_for('book_show',user_id=user_id,venue_id=numbers[0],show_id=numbers[1],seats=seats))
    
   


@app.route('/user/<int:user_id>/<int:venue_id>/<int:show_id>/book_show/<int:seats>',methods=['GET','POST'])

def book_show(user_id,venue_id,show_id,seats):

    user=User.query.get_or_404(user_id)
    venue=Venue.query.get_or_404(venue_id)
    show=Show.query.get_or_404(show_id)

    tags=show.tags.split(',')
    tag_list=[]
    for tag in tags:
        tag_list.append((tag.title().strip(' ')))

    # print(tag_list)
    

    if request.method=='GET':
        return render_template("book_show.html",user=user,venue=venue,show=show,tags=tag_list,seats=seats)
    
    elif request.method=='POST':
        # seats=request.form['seats']
        # print(seats)
        all_seats=0

        user_shows=UserShows.query.filter(UserShows.us_user_id==user_id).all()
        
        flag=True
        if user_shows:
            print("user_shows")
            for user_show in user_shows:
                print(show_id)
                print(user_show.us_show_id)
                if int(show_id)==int(user_show.us_show_id):
                    print("if")
                    user_show.us_seats=seats+user_show.us_seats
                    flag=False
                    break
            if flag:  
                print("else")
                user_show=UserShows(us_user_id=user.user_id,us_show_id=show.show_id,us_seats=seats)
                db.session.add(user_show)
                db.session.flush()
                
                                       
                        

        else:
            print("! user_shows")
            user_show=UserShows(us_user_id=user.user_id,us_show_id=show.show_id,us_seats=seats)
            db.session.add(user_show)
            db.session.flush()


        db.session.commit()

        return redirect(url_for('user_dashboard',user_id=user_id))

    
@app.route('/user/<int:user_id>/genre_chose/<string:genre_chose>',methods=['GET','POST'])

def genre_chose(user_id,genre_chose):

    if request.method=='GET':

        user=User.query.get_or_404(user_id)
        capitalized_genre=genre_chose.title()
        genre_chose=capitalized_genre.strip(' ')

        search=genre_chose
        


        admin_venues=AdminVenues.query.all()
        venues=[]
        for admin_venue in admin_venues:
            venues.append(Venue.query.filter(Venue.venue_id==admin_venue.av_venue_id).all())

     
        dict={}
        genre_dict={}
        seat_dict={}

        for venue in venues:
            venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue[0].venue_id).all()
           


            show_list=[]
            dict[venue[0]]=[]

            for venue_show in venue_shows:
                show=Show.query.filter(Show.show_id==venue_show.vs_show_id).all()
                seats=0
                F_genre=[]
                genre=show[0].tags
                genre_list=genre.split(',')


                flag=False
                
                for tag in genre_list:
                 
                    capitalized_tag=tag.title()
                    F_tag=capitalized_tag.strip(' ')
                    F_genre.append(F_tag)
                    if genre_chose in F_tag:
                        flag=True
                        
                
                if flag:
                
                    show=Show.query.filter(Show.show_id==venue_show.vs_show_id).all()
                    show_list.append(show[0])
                    dict[venue[0]].append(show[0])
                    genre_dict[show[0]]=[]
                    genre_dict[show[0]].append(F_genre)
                    for user_show in UserShows.query.filter(UserShows.us_show_id==show[0].show_id).all():
                        seats=seats+user_show.us_seats
                    
                    seat_dict[show[0]]=seats
                    
        del_list=[]

        for venue in dict:
            if dict[venue]==[]:
                del_list.append(venue)
                print(dict[venue])
        
        for del_venue in del_list:
            del dict[del_venue]
        
        print(dict)
        
        if dict=={}:
            return redirect(url_for('location',user_id=user.user_id,location=search))

                
             

        return render_template('search.html',genre_chose=genre_chose,user=user,dict=dict,genre_dict=genre_dict,seat_dict=seat_dict)
    
@app.route('/user/<int:user_id>/location/<string:location>',methods=['GET','POST'])

def location(user_id,location):

    user=User.query.get_or_404(user_id)

    admin_venues=AdminVenues.query.all()

    venues_dict={}
    seat_dict={}
    genre_dict={}

    for admin_venue in admin_venues:
        venue=Venue.query.filter(Venue.venue_id==admin_venue.av_venue_id).all()
        if venue[0].location==location:
            venue_shows=VenueShows.query.filter(VenueShows.vs_venue_id==venue[0].venue_id).all()
            venues_dict[venue[0]]=[]

            for venue_show in venue_shows:
                show=Show.query.filter(Show.show_id==venue_show.vs_show_id).all()

                seats=0
                F_genre=[]
                genre=show[0].tags
                genre_list=genre.split(',')
                for tag in genre_list:
                 
                    capitalized_tag=tag.title()
                    F_tag=capitalized_tag.strip(' ')
                    F_genre.append(F_tag)
                genre_dict[show[0]]=[]
                genre_dict[show[0]].append(F_genre)

                for user_show in UserShows.query.filter(UserShows.us_show_id==show[0].show_id).all():
                    seats=seats+user_show.us_seats
                    
                seat_dict[show[0]]=seats
                venues_dict[venue[0]].append(show[0])        
    

    print(venues_dict)
    print(seat_dict)
    print(genre_dict)
    if venues_dict=={}:
        return render_template('noshows.html',genre_chose=location,user=user)

    
    
    return render_template('search.html',genre_chose=location,user=user,dict=venues_dict,genre_dict=genre_dict,seat_dict=seat_dict)





@app.route('/user/<int:user_id>/search',methods=['GET','POST'])

def search(user_id):    
    search=request.args.get('search')
    return redirect(url_for('genre_chose',user_id=user_id,genre_chose=search))


@app.route('/user/<int:user_id>/bookings')
def bookings(user_id):
    user=User.query.get_or_404(user_id)
    user_shows=UserShows.query.filter(UserShows.us_user_id==user_id).all()
    shows={}
    seats={}
    rating={}
    venues=Venue.query.all()
    for venue in venues:
        shows[venue]=[]
    if user_shows:
        for user_show in user_shows:
            show=Show.query.filter(Show.show_id==user_show.us_show_id).first()
            print(show)
            show_seats=user_show.us_seats
            rated=user_show.us_rating
            venue_shows=VenueShows.query.filter(VenueShows.vs_show_id==show.show_id).first()
            venue=Venue.query.filter(Venue.venue_id==venue_shows.vs_venue_id).first()

            
             
            shows[venue].append(show)
            seats[show]=show_seats
            rating[show]=rated
    print(shows)
    print(seats)
    print(rating)
    return render_template('user_bookings.html',user=user,shows=shows,seats=seats,rating=rating)


@app.route('/user/<int:user_id>/show/<show_id>/rating',methods=['POST'])

def rating(user_id,show_id):
    user_shows=UserShows.query.filter(UserShows.us_user_id==user_id).all()
    show=Show.query.filter(Show.show_id==show_id).first()
    print(show.show_name)

    rating=request.form['rating']
    rate_show=None
    for user_show in user_shows:
        print(user_show.us_show_id)
        print(show_id)
        if int(user_show.us_show_id)==int(show_id):
            rate_show=user_show
            break
    print(user_show)

    print(rate_show)
    print(rating)
    user_show.us_rating=rating
    db.session.commit()
    return redirect(url_for('bookings',user_id=user_id))



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)


