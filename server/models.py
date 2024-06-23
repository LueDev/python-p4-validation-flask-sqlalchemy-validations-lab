from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    
    '''
    Add validators to the Author and Post models such that:

        1. All authors have a name.
        2. No two authors have the same name.
        3. Author phone numbers are exactly ten digits.
        4. Post content is at least 250 characters long.
        5. Post summary is a maximum of 250 characters.
        6. Post category is either Fiction or Non-Fiction.
        7. Post title is sufficiently clickbait-y and must contain one of the following:
            "Won't Believe"
            "Secret"
            "Top"
            "Guess"
    '''
    # @validates('name')
    # def validate_name(self, key, name):
    #     if not name:
    #         raise ValueError("Author name is required.")
    #     return name

    # @validates('phone_number')
    # def validate_phone_number(self, key, phone_number):
    #     if not phone_number.isdigit() or len(phone_number) != 10:
    #         raise ValueError("Author phone number must be exactly ten digits.")
    #     return phone_number
    
    @validates('name', 'phone_number')
    def validate_author(self, key, value):
        if key == 'name':
            if not value:
                raise ValueError("Author name is required.")
            if Author.query.filter_by(name=value).first():
                raise ValueError("Author name must be unique.")
        
        if key == 'phone_number':
            if not value.isdigit() or len(value) != 10:
                raise ValueError("Author phone number must be exactly ten digits.")
            if Author.query.filter_by(phone_number=value).first():
                raise ValueError("Author phone number must be unique.")
            
        return value

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    
    '''
        4. Post content is at least 250 characters long.
        5. Post summary is a maximum of 250 characters.
        6. Post category is either Fiction or Non-Fiction.
        7. Post title is sufficiently clickbait-y and must contain one of the following:
            "Won't Believe"
            "Secret"
            "Top"
            "Guess"
    '''
    @validates('content', 'summary', 'category', 'title')
    def validate_author(self, key, value):
        if key == 'content':
            if not value:
                raise ValueError("Post content is required.")
            if len(value) < 250:
                raise ValueError("Post content must be at least 250 characters long.")
        
        if key == 'summary':
            if not value:
                raise ValueError("Post summary is required.")
            if len(value) > 250:
                raise ValueError("Post summary must be at most 250 characters long.")
            
        if key == 'category':
            if not value:
                raise ValueError("Post category is required.")
            if value not in ["Fiction", "Non-Fiction"]:
                raise ValueError("Post category must be either Fiction or Non-Fiction.")
            
        if key == 'title':
            if not value:
                raise ValueError("Post title is required.")
            if not any(phrase in value for phrase in ["Won't Believe", "Secret", "Top", "Guess"]):
                raise ValueError("Post title must be clickbait-y and contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'.")
            
        return value
        

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
