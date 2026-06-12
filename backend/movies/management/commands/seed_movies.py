from django.core.management.base import BaseCommand
from movies.models import Movie

class Command(BaseCommand):
    help = 'Seeds the database with initial movie data'

    def handle(self, *args, **kwargs):
        # لیست فیلم‌های نمونه
        movies_data = [
            {
                "title": "Inception",
                "genre": "Action, Sci-Fi, Thriller",
                "year": 2010,
                "director": "Christopher Nolan",
                "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
                "plot": "A thief who steals corporate secrets through the use of dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O.",
                "poster_url": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500",
                "rating": 8.8
            },
            {
                "title": "The Dark Knight",
                "genre": "Action, Crime, Drama",
                "year": 2008,
                "director": "Christopher Nolan",
                "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
                "plot": "When the menace known as the Joker wreaks havoc and chaos on the people of Gotham, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.",
                "poster_url": "https://images.unsplash.com/photo-1478760329108-5c3ed9d495a0?w=500",
                "rating": 9.0
            },
            {
                "title": "Interstellar",
                "genre": "Adventure, Drama, Sci-Fi",
                "year": 2014,
                "director": "Christopher Nolan",
                "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
                "plot": "When Earth becomes uninhabitable, a team of explorers travels through a wormhole in space in an attempt to ensure humanity's survival.",
                "poster_url": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=500",
                "rating": 8.7
            },
            {
                "title": "Pulp Fiction",
                "genre": "Crime, Drama",
                "year": 1994,
                "director": "Quentin Tarantino",
                "cast": "John Travolta, Uma Thurman, Samuel L. Jackson",
                "plot": "The lives of two mob hitmen, a boxer, a gangster and his wife, and a pair of diner bandits intertwine in four tales of violence and redemption.",
                "poster_url": "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?w=500",
                "rating": 8.9
            },
            {
                "title": "The Matrix",
                "genre": "Action, Sci-Fi",
                "year": 1999,
                "director": "Lana Wachowski, Lilly Wachowski",
                "cast": "Keanu Reeves, Laurence Fishburne, Carrie-Anne Moss",
                "plot": "When a beautiful stranger leads computer hacker Neo to a forbidding underworld, he discovers the shocking truth--the life he knows is the elaborate deception of an evil cyber-intelligence.",
                "poster_url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=500",
                "rating": 8.7
            },
            {
                "title": "Spirited Away",
                "genre": "Animation, Adventure, Fantasy",
                "year": 2001,
                "director": "Hayao Miyazaki",
                "cast": "Daveigh Chase, Suzanne Pleshette, Miyu Irino",
                "plot": "During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods, witches, and spirits, and where humans are changed into beasts.",
                "poster_url": "https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?w=500",
                "rating": 8.6
            },
            {
                "title": "The Hangover",
                "genre": "Comedy",
                "year": 2009,
                "director": "Todd Phillips",
                "cast": "Bradley Cooper, Ed Helms, Zach Galifianakis",
                "plot": "Three buddies wake up from a bachelor party in Las Vegas, with no memory of the previous night and the bachelor missing. They make their way around the city in order to find their friend before his wedding.",
                "poster_url": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=500",
                "rating": 7.7
            },
            {
                "title": "The Conjuring",
                "genre": "Horror, Mystery, Thriller",
                "year": 2013,
                "director": "James Wan",
                "cast": "Patrick Wilson, Vera Farmiga, Ron Livingston",
                "plot": "Paranormal investigators Ed and Lorraine Warren work to help a family terrorized by a dark presence in their farmhouse.",
                "poster_url": "https://images.unsplash.com/photo-1509248961158-e54f6934749c?w=500",
                "rating": 7.5
            }
        ]

        # پاک کردن داده‌های قبلی برای جلوگیری از تکرار (اختیاری)
        Movie.objects.all().delete()

        # ثبت فیلم‌ها در دیتابیس
        for movie in movies_data:
            Movie.objects.create(**movie)

        self.stdout.write(self.style.SUCCESS('Successfully seeded database with movies!'))