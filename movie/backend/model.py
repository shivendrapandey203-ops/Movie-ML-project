import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import requests
import ast

class MovieRecommender:
    def __init__(self):
        self.df = None
        self.tfidf = None
        self.similarity = None
        self.tmdb_api_key = "5e75ed03a9c1414df7ecca8260d51a1f"  # Public TMDB API key
        
    def load_data(self):
        """Load and preprocess movie dataset"""
        # Sample dataset (in real project, replace with your CSV)
        data = {
            'title': [
                'Inception', 'The Dark Knight', 'Interstellar', 'The Matrix', 'Fight Club',
                'Pulp Fiction', 'Forrest Gump', 'The Shawshank Redemption', 'Titanic',
                'La La Land', 'The Godfather', 'Goodfellas', 'Whiplash', 'Spider-Man: No Way Home',
                'Avengers: Endgame', 'The Wolf of Wall Street', 'Deadpool', 'Joker',
                'Parasite', '1917', 'Dune', 'Tenet', 'The Prestige', 'Memento',
                'Shutter Island', 'The Silence of the Lambs', 'Se7en', 'Zodiac', 'Gone Girl',
                'The Departed', 'Catch Me If You Can', 'The Grand Budapest Hotel', 'Her',
                'Birdman', 'Moonlight', 'Get Out', 'Knives Out', 'The Invisible Man',
                'A Quiet Place', 'John Wick', 'Mad Max: Fury Road', 'Baby Driver'
            ],
            'genres': [
                'Action,Adventure,Sci-Fi', 'Action,Crime,Drama', 'Adventure,Drama,Sci-Fi',
                'Action,Sci-Fi', 'Drama', 'Crime,Drama', 'Drama,Romance',
                'Drama', 'Drama,Romance', 'Comedy,Drama,Music', 'Crime,Drama',
                'Biography,Crime,Drama', 'Drama,Music', 'Action,Adventure,Fantasy',
                'Action,Adventure,Drama', 'Biography,Crime,Drama', 'Action,Adventure,Comedy',
                'Crime,Drama,Thriller', 'Drama,Thriller', 'Action,Drama,War',
                'Action,Adventure,Drama', 'Action,Sci-Fi,Thriller', 'Drama,Mystery,Sci-Fi',
                'Mystery,Thriller', 'Drama,Mystery,Thriller', 'Crime,Drama,Thriller',
                'Crime,Drama,Mystery', 'Drama,Mystery,Thriller', 'Crime,Drama,Thriller',
                'Biography,Crime,Drama', 'Comedy,Drama', 'Drama,Romance,Sci-Fi',
                'Comedy,Drama', 'Drama', 'Horror,Mystery', 'Comedy,Crime,Mystery',
                'Horror,Mystery,Sci-Fi', 'Horror', 'Action,Crime,Thriller',
                'Action,Adventure,Sci-Fi', 'Action,Crime,Music'
            ],
            'overview': [
                'A thief who steals corporate secrets through dream-sharing technology.',
                'When the menace known as the Joker wreaks havoc and chaos on the people of Gotham.',
                'A team of explorers travel through a wormhole in space in an attempt to ensure humanitys survival.',
                'A computer hacker learns from mysterious rebels about the true nature of his reality.',
                'An insomniac office worker and a devil-may-care soap maker form a mens sewing circle.',
                'The lives of two mob hitmen, a boxer, a gangster and others intertwine in four tales of violence.',
                'The history of the US from the perspective of an Alabama man who lives through many decades.',
                'Two imprisoned men bond over a number of years, finding solace and eventual redemption.',
                'A seventeen-year-old aristocrat falls in love with a kind hearted working class girl onboard the RMS Titanic.',
                'A musician and an aspiring actress fall in love while living together in LA.',
                'The aging patriarch of an organized crime dynasty transfers control of his clandestine empire.',
                'The story of Henry Hill and his life in the mob, covering his relationship with his wife Karen.',
                'A promising young drummer enrolls at a cut-throat music conservatory.',
                'With Spider-Mans identity now revealed, Peter asks Doctor Strange for help.',
                'After the devastating events of Infinity War, the universe is in ruins.',
                'Based on the true story of Jordan Belfort, from his rise to a wealthy stock-broker living the high life.',
                'A wisecracking mercenary gets experimented on and becomes immortal but ugly.',
                'A mentally troubled stand-up comedian is driven insane and turns to a life of crime and chaos.',
                'Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family.',
                'April 6th, 1917. 1600 hours. Two British soldiers are sent to no mans land.',
                'A noble family on the planet Arrakis, where they try to take control of the spice production.',
                'Armed with only one word, Tenet, and fighting for the survival of the entire world.',
                'After a tragic accident, a powerful psychic wakes up from a coma unable to remember the past.',
                'A man who suffers from short-term memory loss, as well as an inability to form new memories.',
                'A man builds a supercar. Behind the car he designs a new life, filled with challenges and adrenaline.',
                'A census taker who talks to the madman who has murdered eleven young women.',
                'Two detectives, a rookie and a veteran, hunt a serial killer who uses the seven deadly sins as his motives.',
                'A serial killer targets the three reporters who tried to catch him years earlier.',
                'A woman searches for the truth about her husband.',
                'An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang.',
                'A con man offers to forge checks to a desperate bank employee in exchange for a cut.',
                'A writer encounters the owner of an aging high-class hotel, who tells him of her glory days.',
                'A lonely Roman letter writer develops a relationship with an engaged LA radio host.',
                'A fading actor best known for his portrayal of a popular superhero attempts a comeback.',
                'A young African-American, Chiron, experiences the tragedy of life too soon.',
                'A young man buys a house from a family he believes to be possessed.',
                'A detective investigates the death of a patriarch of an eccentric, wealthy family.',
                'When Cecilia Cass, a woman of troubled family pedigree, notices a vague figure lurking.',
                'A family is forced into silence when a parasitic alien finds refuge in their mouths.',
                'John Wick is forced out of retirement by a former associate looking to seize control.',
                'In a post-apocalyptic wasteland, a woman rebels against a tyrannical ruler.',
                'After being coerced into working for a crime boss, a talented getaway driver finds himself.'
            ],
            'keywords': [
                'dream,thief,heist', 'batman,joker,chaos', 'space,wormhole,time',
                'matrix,hacker,reality', 'fight,club,insomnia', 'pulp,fiction,mob',
                'forrest,gump,life', 'prison,redemption,hope', 'titanic,love,disaster',
                'la,la,land,music', 'godfather,mob,family', 'goodfellas,mob,crime',
                'whiplash,drum,music', 'spider,man,superhero', 'avengers,endgame,superhero',
                'wolf,wall,street,stock', 'deadpool,mercenary,immortal', 'joker,clown,chaos',
                'parasite,rich,poor', '1917,war,soldier', 'dune,spice,desert',
                'tenet,time,inversion', 'prestige,magic,rival', 'memento,memory,revenge',
                'shutter,island,mystery', 'silence,lambs,serial,killer', 'se7en,sins,murder',
                'zodiac,killer,san,francisco', 'gone,girl,mystery', 'departed,undercover,mob',
                'catch,me,fraud', 'grand,budapest,hotel', 'her,ai,love',
                'birdman,actor,superhero', 'moonlight,growing,up', 'get,out,horror',
                'knives,out,mystery', 'invisible,man,horror', 'quiet,place,silence',
                'john,wick,revenge', 'mad,max,fury,road', 'baby,driver,getaway'
            ],
            'cast': [
                'Leonardo DiCaprio,Joseph Gordon-Levitt,Ellen Page', 'Christian Bale,Heath Ledger,Aaron Eckhart',
                'Matthew McConaughey,Anne Hathaway,Jessica Chastain', 'Keanu Reeves,Laurence Fishburne,Carrie-Anne Moss',
                'Brad Pitt,Edward Norton,Helena Bonham Carter', 'John Travolta,Uma Thurman,Samuel L. Jackson',
                'Tom Hanks,Robin Wright,Gary Sinise', 'Tim Robbins,Morgan Freeman,Bob Gunton',
                'Leonardo DiCaprio,Kate Winslet,Billy Zane', 'Ryan Gosling,Emma Stone,Finnegan Sutton',
                'Marlon Brando,Al Pacino,James Caan', 'Robert De Niro,Ray Liotta,Joe Pesci',
                'Miles Teller,J.K. Simmons,Melissa Benoist', 'Tom Holland,Zendaya,Benedict Cumberbatch',
                'Robert Downey Jr.,Chris Evans,Scarlett Johansson', 'Leonardo DiCaprio,Jonah Hill,Margot Robbie',
                'Ryan Reynolds,Morena Baccarin,Ed Skrein', 'Joaquin Phoenix,Zazie Beetz,Robert De Niro',
                'Song Kang-ho,Lee Sun-kyun,Cho Yeo-jeong', 'George MacKay,Dean-Charles Chapman,Mark Strong',
                'Timothée Chalamet,Zendaya,Oscar Isaac', 'John David Washington,Robert Pattinson,Elizabeth Debicki',
                'Christian Bale,Hugh Jackman,Scarlett Johansson', 'Guy Pearce,Carrie-Anne Moss,Joe Pantoliano',
                'Leonardo DiCaprio,Mark Ruffalo,Ben Kingsley', 'Jodie Foster,Anthony Hopkins,Scott Glenn',
                'Brad Pitt,Morgan Freeman,Kevin Spacey', 'Jake Gyllenhaal,Robert Downey Jr.,Mark Ruffalo',
                'Ben Affleck,Rosamund Pike,Neil Patrick Harris', 'Leonardo DiCaprio,Matt Damon,Jack Nicholson',
                'Leonardo DiCaprio,Tom Hanks,Christopher Walken', 'Ralph Fiennes,Tilda Swinton,Adrien Brody',
                'Joaquin Phoenix,Amy Adams,Rooney Mara', 'Michael Keaton,Edward Norton,Emma Stone',
                'Alex R. Hibbert,Mahershala Ali,Janelle Monáe', 'Daniel Kaluuya,Allison Williams,Bradley Whitford',
                'Daniel Craig,Chris Evans,Ana de Armas', 'Elisabeth Moss,Oliver Jackson-Cohen,Aldis Hodge',
                'John Krasinski,Emily Blunt,Millicent Simmonds', 'Keanu Reeves,Michael Nyqvist,Alfie Allen',
                'Tom Hardy,Charlize Theron,Nicholas Hoult', 'Ansel Elgort,Lily James,Jamie Foxx'
            ],
            'crew': [
                'Christopher Nolan,Emma Thomas,Charles Roven', 'Christopher Nolan,Emma Thomas,Charles Roven',
                'Christopher Nolan,Emma Thomas,Lyndon Balcourt', 'Lana Wachowski,Lilly Wachowski,Joel Silver',
                'David Fincher,Ross Grayson Bell,Art Linson', 'Quentin Tarantino,Lawrence Bender,Richard N. Gladstein',
                'Robert Zemeckis,Wendy Finerman,Steve Starkey', 'Frank Darabont,Niki Marvin', 'James Cameron,Jon Landau',
                'Damien Chazelle,Marc Platt,David Klopn', 'Francis Ford Coppola,Gray Frederickson,Fred Roos',
                'Martin Scorsese,Irwin Winkler,Barbara De Fina', 'Damien Chazelle,Jason Blum,Helen Estabrook',
                'Kevin Feige,Amy Pascal', 'Kevin Feige', 'Martin Scorsese,Randa Haines', 'Tim Miller,Kinberg Genre',
                'Todd Phillips,Scott Silver,Bruce Berman', 'Bong Joon Ho,Moon Yang-kwon', 'Sam Mendes',
                'Mary Parent,Denis Villeneuve', 'Emma Thomas,Christopher Nolan', 'Christopher Nolan,Emma Thomas',
                'Leonard Goldberg,Jonathan Nolan', 'Suzanne Todd,Jennifer Todd', 'Leonardo DiCaprio,Brad Pitt',
                'Scott Rudin,Brad Pitt', 'David Fincher,Ceán Chaffin', 'Martin Scorsese,Brad Pitt',
                'Steven Spielberg,Amblin Entertainment', 'Wes Anderson,Jeremy Dawson', 'Spike Jonze,Spike Jonze',
                'Alejandro G. Iñárritu,Arnon Milchan', 'Barry Jenkins,Adele Romanski', 'Jordan Peele,Sean McKittrick',
                'Rian Johnson,Rian Johnson', 'Blumhouse Productions', 'John Krasinski', 'Chad Stahelski,David Leitch',
                'George Miller,George Miller', 'Edgar Wright,Niki Roosevelt'
            ]
        }
         # FIX FOR ARRAY LENGTH ERROR
        min_len = min(len(v) for v in data.values())

        for key in data:
            data[key] = data[key][:min_len]
            
        self.df = pd.DataFrame(data)
        
        # Combine features
        self.df['features'] = (
            self.df['title'].astype(str) + ' ' +
            self.df['genres'].astype(str) + ' ' +
            self.df['overview'].astype(str) + ' ' +
            self.df['keywords'].astype(str) + ' ' +
            self.df['cast'].astype(str) + ' ' +
            self.df['crew'].astype(str)
        )
        
    def build_model(self):
        """Build TF-IDF and similarity matrix"""
        self.tfidf = TfidfVectorizer(max_features=5000, stop_words='english')
        tfidf_matrix = self.tfidf.fit_transform(self.df['features'].values.astype('U'))
        self.similarity = cosine_similarity(tfidf_matrix)
        
        # Save model files
        with open('vectorizer.pkl', 'wb') as f:
            pickle.dump(self.tfidf, f)
        with open('similarity.pkl', 'wb') as f:
            pickle.dump(self.similarity, f)
            
    def get_tmdb_data(self, movie_title):
        """Get TMDB data for movie"""
        url = f"https://api.themoviedb.org/3/search/movie?api_key={self.tmdb_api_key}&query={movie_title}"
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data['results']:
                    movie = data['results'][0]
                    return {
                        'poster': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie['poster_path'] else None,
                        'backdrop': f"https://image.tmdb.org/t/p/w1280{movie['backdrop_path']}" if movie['backdrop_path'] else None,
                        'rating': movie['vote_average'],
                        'overview': movie['overview'][:200] + '...'
                    }
        except:
            pass
        return {}
        
    def recommend_similar_movies(self, movie_title, n=12):
        """Recommend similar movies"""
        if self.df is None:
            self.load_data()
            
        idx = self.get_closest_match(movie_title)
        if idx == -1:
            return []
            
        distances = sorted(list(enumerate(self.similarity[idx])), reverse=True, key=lambda x: x[1])[1:n+1]
        
        recommendations = []
        for i, dist in distances:
            movie_data = self.df.iloc[i]
            tmdb_data = self.get_tmdb_data(movie_data['title'])
            
            recommendations.append({
                'title': movie_data['title'],
                'genres': movie_data['genres'],
                'overview': tmdb_data.get('overview', movie_data['overview']),
                'rating': tmdb_data.get('rating', 0),
               'poster': tmdb_data.get(
    'poster'
) or 'https://dummyimage.com/300x450/1a1a1a/ffffff&text=No+Poster',
                'backdrop': tmdb_data.get('backdrop'),
                'similarity': float(dist)
            })
        return recommendations
        
    def recommend_movies_by_mood(self, mood, n=12):
        """Recommend movies by mood"""
        mood_keywords = {
            'happy': ['comedy', 'music', 'romance', 'family'],
            'sad': ['drama', 'tragedy', 'emotional'],
            'romantic': ['romance', 'love', 'couple'],
            'thrilling': ['thriller', 'suspense', 'mystery'],
            'excited': ['action', 'adventure', 'superhero'],
            'chill': ['drama', 'slice of life', 'relaxing']
        }
        
        keywords = mood_keywords.get(mood.lower(), ['drama'])
        scores = []
        
        for idx, row in self.df.iterrows():
            score = sum(1 for kw in keywords if kw.lower() in row['genres'].lower())
            scores.append((idx, score))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:n*2]]
        
        recommendations = []
        for idx in top_indices[:n]:
            movie_data = self.df.iloc[idx]
            tmdb_data = self.get_tmdb_data(movie_data['title'])
            
            recommendations.append({
                'title': movie_data['title'],
                'genres': movie_data['genres'],
                'overview': tmdb_data.get('overview', movie_data['overview']),
                'rating': tmdb_data.get('rating', 0),
'poster': tmdb_data.get(
    'poster'
) or 'https://dummyimage.com/300x450/1a1a1a/ffffff&text=No+Poster',
                'backdrop': tmdb_data.get('backdrop'),
                'similarity': 0.9
            })
        return recommendations
        
    def recommend_movies_by_genre(self, genre, n=12):
        """Recommend movies by genre"""
        scores = []
        
        for idx, row in self.df.iterrows():
            score = 1 if genre.lower() in row['genres'].lower() else 0
            scores.append((idx, score))
            
        scores.sort(key=lambda x: x[1], reverse=True)
        top_indices = [idx for idx, _ in scores[:n]]
        
        recommendations = []
        for idx in top_indices:
            movie_data = self.df.iloc[idx]
            tmdb_data = self.get_tmdb_data(movie_data['title'])
            
            recommendations.append({
                'title': movie_data['title'],
                'genres': movie_data['genres'],
                'overview': tmdb_data.get('overview', movie_data['overview']),
                'rating': tmdb_data.get('rating', 0),
'poster': tmdb_data.get(
    'poster'
) or 'https://dummyimage.com/300x450/1a1a1a/ffffff&text=No+Poster',
                'backdrop': tmdb_data.get('backdrop'),
                'similarity': 0.95
            })
        return recommendations
        
    def random_recommendation(self, n=12):
        """Get random movie recommendations"""
        indices = np.random.choice(len(self.df), n, replace=False)
        
        recommendations = []
        for idx in indices:
            movie_data = self.df.iloc[idx]
            tmdb_data = self.get_tmdb_data(movie_data['title'])
            
            recommendations.append({
                'title': movie_data['title'],
                'genres': movie_data['genres'],
                'overview': tmdb_data.get('overview', movie_data['overview']),
                'rating': tmdb_data.get('rating', 0),
'poster': tmdb_data.get(
    'poster'
) or 'https://dummyimage.com/300x450/1a1a1a/ffffff&text=No+Poster',
                'backdrop': tmdb_data.get('backdrop'),
                'similarity': 0.8
            })
        return recommendations
        
    def get_closest_match(self, title,n=12):
        """Find closest matching movie title"""
        title = title.lower()
        for idx, movie_title in enumerate(self.df['title']):
            if title in movie_title.lower():
                return idx
        return -1
        
    def search_movies(self, query, n=12):
     """Search movies by title or keywords"""

     query = query.lower().strip()

     results = []

     for idx, row in self.df.iterrows():

            title = str(row['title']).lower()
            genres = str(row['genres']).lower()
            overview = str(row['overview']).lower()

            if (
                query in title or
                query in genres or
                query in overview
            ):

                tmdb_data = self.get_tmdb_data(row['title'])

                results.append({
                    'title': row['title'],
                    'genres': row['genres'],
                    'overview': tmdb_data.get(
                        'overview',
                        row['overview']
                    ),
                    'rating': tmdb_data.get('rating', 8.0),

                    'poster': tmdb_data.get(
                        'poster'
                    ) or 'https://dummyimage.com/300x450/1a1a1a/ffffff&text=No+Poster',

                    'backdrop': tmdb_data.get('backdrop'),

                    'similarity': 0.85
                })

            if len(results) >= n:
                break

     return results

# Initialize and save model
if __name__ == "__main__":
    recommender = MovieRecommender()
    recommender.load_data()
    recommender.build_model()
    print("Model created and saved!")