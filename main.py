#main
from kivy.config import Config

Config.set('graphics','width','450')
Config.set('graphics','height','800')

import random
import json
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, NumericProperty, BooleanProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.input.motionevent import MotionEvent
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.core.text import LabelBase
from kivy.storage.jsonstore import JsonStore
import uuid 
import os
import datetime


# Register Poppins fonts using the fixed filenames you provided.
font_dir = os.path.join(os.path.dirname(__file__), 'assets')
LabelBase.register(
    name='Poppins',
    fn_regular=os.path.join(font_dir, 'Poppins-Regular.ttf'),
    fn_bold=os.path.join(font_dir, 'Poppins-Bold.ttf'),
    fn_italic=os.path.join(font_dir, 'Poppins-Italic.ttf'),
)
# Also register lowercase alias (optional)
LabelBase.register(
    name='poppins',
    fn_regular=os.path.join(font_dir, 'Poppins-Regular.ttf'),
    fn_bold=os.path.join(font_dir, 'Poppins-Bold.ttf'),
    fn_italic=os.path.join(font_dir, 'Poppins-Italic.ttf'),
)

# --- Game Data (Easy to Add More) ---
# Each key is a category. The value is a list of word/clue pairs.
# To add a new category, just add a new dictionary entry.
GAME_DATA = {
"Clash Royale": [
        {"word": "P.E.K.K.A", "clue": "7 Elixir."},
        {"word": "Giant", "clue": "Tower target."},
        {"word": "Hog Rider", "clue": "Fast rush."},
        {"word": "Suspicious Bush", "clue": "Invisible."},
        {"word": "Bandit", "clue": "Legendary."},
        {"word": "Skeleton Army", "clue": "Swarm."},
        {"word": "Sparky", "clue": "Slow blast."},
        {"word": "Tesla", "clue": "Hides."},
        {"word": "Inferno Tower", "clue": "Fire beam."},
        {"word": "Zap", "clue": "2 Elixir spell."},
        {"word": "Mini P.E.K.K.A", "clue": "4 Elixir."},
        {"word": "Wizard", "clue": "5 Elixir."},
        {"word": "Valkyrie", "clue": "4 Elixir."},
        {"word": "Miner", "clue": "Digs anywhere."},
        {"word": "Electro Wizard", "clue": "Two targets."},
        {"word": "Ice Wizard", "clue": "Slows."},
        {"word": "Princess", "clue": "Long range."},
        {"word": "The Log", "clue": "Rolls."},
        {"word": "Fireball", "clue": "4 Elixir."},
        {"word": "Arrows", "clue": "3 Elixir."},
        {"word": "Minions", "clue": "Flying."},
        {"word": "Mega Knight", "clue": "Jumps."},
        {"word": "Golem", "clue": "Splits."},
        {"word": "Lava Hound", "clue": "Pups."},
        {"word": "Royal Giant", "clue": "6 Elixir."},
        {"word": "Goblin Barrel", "clue": "Surprise spell."},
        {"word": "Witch", "clue": "Spawns."},
        {"word": "Prince", "clue": "Charges."},
        {"word": "Dark Prince", "clue": "Shield."},
        {"word": "Baby Dragon", "clue": "Flying splash."},
        {"word": "Archer Queen", "clue": "Cloaking ability."},
        {"word": "Golden Knight", "clue": "Dash ability."},
        {"word": "Little Prince", "clue": "Guardian."},
        {"word": "Mighty Miner", "clue": "Drill ability."},
        {"word": "Monk", "clue": "Reflects attacks."},
        {"word": "Skeleton King", "clue": "Summon ability."},
        {"word": "Graveyard", "clue": "Spell swarm."},
        {"word": "Inferno Dragon", "clue": "Flying beam."},
        {"word": "Lumberjack", "clue": "Drops Rage."},
        {"word": "Magic Archer", "clue": "Piercing arrow."},
        {"word": "Mother Witch", "clue": "Cursed hogs."},
        {"word": "Night Witch", "clue": "Spawns Bats."},
        {"word": "Phoenix", "clue": "Rebirth egg."},
        {"word": "Ram Rider", "clue": "Snare."},
        {"word": "Fisherman", "clue": "Hooks enemies."},
        {"word": "Balloon", "clue": "Drops bomb."},
        {"word": "Bowler", "clue": "Rolls rock."},
        {"word": "Cannon Cart", "clue": "Becomes building."},
        {"word": "Electro Dragon", "clue": "Three chains."},
        {"word": "Electro Giant", "clue": "7 Elixir."},
        {"word": "Executioner", "clue": "Returning axe."},
        {"word": "Goblin Giant", "clue": "Gobs on back."},
        {"word": "Guards", "clue": "Armored."},
        {"word": "Hunter", "clue": "Shotgun."},
        {"word": "Tornado", "clue": "Pull spell."},
        {"word": "Wall Breakers", "clue": "2 Elixir."},
        {"word": "Battle Healer", "clue": "Heals nearby."},
        {"word": "Battle Ram", "clue": "Barbarian building."},
        {"word": "Dart Goblin", "clue": "Fast range."},
        {"word": "Elixir Collector", "clue": "Generates Elixir."},
        {"word": "Royal Hogs", "clue": "Four piglets."},
        {"word": "Three Musketeers", "clue": "9 Elixir."},
        {"word": "Ice Golem", "clue": "2 Elixir tank."},
        {"word": "Mega Minion", "clue": "Single flier."},
        {"word": "Zappies", "clue": "Twin stunners."},
        {"word": "Archers", "clue": "Pair of girls."},
        {"word": "Barbarians", "clue": "Five men."},
        {"word": "Bomber", "clue": "Skeleton bomb."},
        {"word": "Bats", "clue": "Air swarm."},
        {"word": "Elite Barbarians", "clue": "6 Elixir."},
        {"word": "Fire Spirit", "clue": "1 Elixir."},
        {"word": "Goblins", "clue": "2 Elixir swarm."},
        {"word": "Goblin Gang", "clue": "Mixed troop."},
        {"word": "Ice Spirit", "clue": "Freezes."},
        {"word": "Knight", "clue": "3 Elixir tank."},
        {"word": "Mortar", "clue": "Siege."},
        {"word": "Rascals", "clue": "5 Elixir."},
        {"word": "Skeletons", "clue": "Four bones."},
        {"word": "Spear Goblins", "clue": "Ranged."},
        {"word": "Firecracker", "clue": "Recoils."},
        {"word": "Royal Recruits", "clue": "Six shields."},
        {"word": "Barbarian Barrel", "clue": "Drops Barb."},
        {"word": "Clone", "clue": "Duplicates."},
        {"word": "Earthquake", "clue": "Damages buildings."},
        {"word": "Freeze", "clue": "Stops everything."},
        {"word": "Heal Spirit", "clue": "1 Elixir heal."},
        {"word": "Poison", "clue": "Area damage."},
        {"word": "Rage", "clue": "Speed buff."},
        {"word": "Rocket", "clue": "6 Elixir."},
        {"word": "Royal Delivery", "clue": "Drops Recruit."},
        {"word": "Barbarian Hut", "clue": "Spawner building."},
        {"word": "Bomb Tower", "clue": "4 Elixir."},
        {"word": "Cannon", "clue": "3 Elixir."},
        {"word": "Furnace", "clue": "Spawns Spirits."},
        {"word": "Goblin Cage", "clue": "Releases Brawler."},
        {"word": "Tombstone", "clue": "3 Elixir spawner."},
        {"word": "X-Bow", "clue": "Siege."},
    ],
    "Food": [
        {"word": "Ramen", "clue": "Noodles."},
        {"word": "Butter Chicken", "clue": "Rich gravy."},
        {"word": "Pizza", "clue": "Flatbread."},
        {"word": "Hot Dog", "clue": "Bun."},
        {"word": "Biriyani", "clue": "Rice."},
        {"word": "Paneer", "clue": "Milk."},
        {"word": "Fish and Chips", "clue": "British."},
        {"word": "Momo", "clue": "Dumpling."},
        {"word": "French Fries", "clue": "Potato."},
        {"word": "Samosa", "clue": "Triangular."},
        {"word": "Dosa", "clue": "Crispy."},
        {"word": "Vada Pav", "clue": "Mumbai."},
        {"word": "Jalebi", "clue": "Sweet."},
        {"word": "Gulab Jamun", "clue": "Syrup."},
        {"word": "Sushi", "clue": "Raw."},
        {"word": "Taco", "clue": "Folded."},
        {"word": "Burger", "clue": "Patty."},
        {"word": "Pasta", "clue": "Italian."},
        {"word": "Croissant", "clue": "Flaky."},
        {"word": "Salad", "clue": "Greens."},
        {"word": "Steak", "clue": "Grilled."},
        {"word": "Kebab", "clue": "Skewered."},
        {"word": "Idli", "clue": "Steamed."},
        {"word": "Pani Puri", "clue": "Water."},
    ],
    "Animals": [
        {"word": "Tiger", "clue": "Stripes."},
        {"word": "Wolf", "clue": "Packs."},
        {"word": "Blue Whale", "clue": "Large."},
        {"word": "Giraffe", "clue": "Tall."},
        {"word": "Elephant", "clue": "Trunk."},
        {"word": "Shark", "clue": "Fins."},
        {"word": "Lion", "clue": "Mane."},
        {"word": "Dragonfly", "clue": "Hovers."},
        {"word": "Spider", "clue": "Web."},
        {"word": "Mosquito", "clue": "Bites."},
        {"word": "Peacock", "clue": "Feathers."},
        {"word": "Cobra", "clue": "Hood."},
        {"word": "Kangaroo", "clue": "Pouch."},
        {"word": "Penguin", "clue": "Waddles."},
        {"word": "Dolphin", "clue": "Intelligent."},
        {"word": "Octopus", "clue": "Eight."},
        {"word": "Camel", "clue": "Hump."},
        {"word": "Parrot", "clue": "Repeats."},
        {"word": "Bear", "clue": "Hibernates."},
        {"word": "Fox", "clue": "Cunning."},
        {"word": "Deer", "clue": "Antlers."},
        {"word": "Owl", "clue": "Night."},
        {"word": "Rabbit", "clue": "Hops."},
        {"word": "Horse", "clue": "Ridden."},
        {"word": "Goat", "clue": "Climbs."},
    ],
    "Companies": [
        {"word": "Apple", "clue": "Fruit."},
        {"word": "Shell", "clue": "Petroleum."},
        {"word": "Boost", "clue": "Energy."},
        {"word": "NASA", "clue": "Space."},
        {"word": "Walmart", "clue": "Retail."},
        {"word": "McDonalds", "clue": "Arches."},
        {"word": "Dominos", "clue": "Pizza."},
        {"word": "Yamaha", "clue": "Music."},
        {"word": "Redbull", "clue": "Wings."},
        {"word": "Lamborghini", "clue": "Bull."},
        {"word": "Google", "clue": "Search."},
        {"word": "Microsoft", "clue": "Windows."},
        {"word": "Amazon", "clue": "River."},
        {"word": "Tesla", "clue": "Electric."},
        {"word": "Facebook", "clue": "Social."},
        {"word": "Netflix", "clue": "Streaming."},
        {"word": "Toyota", "clue": "Cars."},
        {"word": "Samsung", "clue": "Phones."},
        {"word": "Reliance", "clue": "Indian."},
        {"word": "Tata", "clue": "India"},
        {"word": "Nike", "clue": "Sports"},
        {"word": "Adidas", "clue": "Stripes."},
        {"word": "Coca-Cola", "clue": "Red."},
    ],
    "Cars": [
        {"word": "Indica", "clue": "Value."},
        {"word": "Bugatti Chiron", "clue": "Fast."},
        {"word": "Swift Dezire", "clue": "Common."},
        {"word": "Hennessey Venom", "clue": "Record."},
        {"word": "Koenigsegg Jesko Absolut", "clue": "Record breaker."},
        {"word": "Thar", "clue": "Off-road."},
        {"word": "Lamborghini Sesto Elemento", "clue": "Rare."},
        {"word": "Maruti 800", "clue": "First car."},
        {"word": "Ambassador", "clue": "Classic."},
        {"word": "Scorpio", "clue": "SUV."},
        {"word": "Creta", "clue": "Popular."},
        {"word": "Ferrari 488", "clue": "Red."},
        {"word": "Porsche 911", "clue": "Iconic."},
        {"word": "Rolls-Royce Phantom", "clue": "Luxury."},
        {"word": "Jeep Wrangler", "clue": "Off-road."},
        {"word": "Honda City", "clue": "Sedan."},
        {"word": "Toyota Fortuner", "clue": "Large."},
        {"word": "BMW M5", "clue": "Sporty."},
        {"word": "Mercedes-Benz S-Class", "clue": "Comfort."},
        {"word": "Audi R8", "clue": "Superhero."},
        {"word": "Volkswagen Beetle", "clue": "Bug."},
        {"word": "Ford Mustang", "clue": "Muscle."},
        {"word": "Tesla Model 3", "clue": "Electric."},
        {"word": "Range Rover", "clue": "Luxury SUV."},
        {"word": "Nano", "clue": "Small."},
    ],
    "Famous People": [
        {"word": "Jeff Bezos", "clue": "Entrepreneur."},
        {"word": "LeBron James", "clue": "Basketball."},
        {"word": "Venkat", "clue": "Specific."},
        {"word": "Satish Sir", "clue": "Teacher."},
        {"word": "Rinku Bhai", "clue": "Local."},
        {"word": "Da Vinci", "clue": "Painter."},
        {"word": "Narendra Modi", "clue": "Leader."},
        {"word": "Spider-Man", "clue": "Swing."},
        {"word": "Sachin Tendulkar", "clue": "Cricket."},
        {"word": "Virat Kohli", "clue": "Cricket."},
        {"word": "MS Dhoni", "clue": "Captain."},
        {"word": "Shah Rukh Khan", "clue": "Actor."},
        {"word": "Amitabh Bachchan", "clue": "Actor."},
        {"word": "Deepika Padukone", "clue": "Actress."},
        {"word": "Elon Musk", "clue": "Rockets."},
        {"word": "Mark Zuckerberg", "clue": "Social."},
        {"word": "Taylor Swift", "clue": "Singer."},
        {"word": "Arijit Singh", "clue": "Singer."},
        {"word": "Albert Einstein", "clue": "Genius."},
        {"word": "Mahatma Gandhi", "clue": "Peace."},
        {"word": "Nelson Mandela", "clue": "Leader."},
        {"word": "Steve Jobs", "clue": "Apple."},
        {"word": "Bill Gates", "clue": "Windows."},
        {"word": "Ratan Tata", "clue": "Industrialist."},
        {"word": "A. P. J. Abdul Kalam", "clue": "President."},
    ],
    "Places": [
        {"word": "India", "clue": "Spices."},
        {"word": "America", "clue": "Movies."},
        {"word": "England", "clue": "Queen."},
        {"word": "Japan", "clue": "Culture."},
        {"word": "China", "clue": "Wall."},
        {"word": "France", "clue": "Tower."},
        {"word": "Mumbai", "clue": "Coastal."},
        {"word": "Delhi", "clue": "Capital."},
        {"word": "Bangalore", "clue": "Silicon."},
        {"word": "Himalayas", "clue": "Mountains."},
        {"word": "Ganges", "clue": "River."},
        {"word": "Taj Mahal", "clue": "Wonder."},
        {"word": "Mount Everest", "clue": "Highest."},
        {"word": "Amazon Rainforest", "clue": "Lungs."},
        {"word": "Sahara Desert", "clue": "Dry."},
        {"word": "Nile River", "clue": "Longest."},
        {"word": "Eiffel Tower", "clue": "Paris."},
        {"word": "Statue of Liberty", "clue": "New York."},
        {"word": "Pyramids of Giza", "clue": "Ancient."},
        {"word": "Goa", "clue": "Beaches."},
        {"word": "London", "clue": "Bridge."},
        {"word": "Tokyo", "clue": "Crowded."},
        {"word": "Sydney", "clue": "Opera."},
        {"word": "Dubai", "clue": "Tallest."},
        {"word": "Russia", "clue": "Largest."},
        {"word": "Australia", "clue": "Continent."},
        {"word": "Brazil", "clue": "Football."},
        {"word": "Canada", "clue": "Maple."},
        {"word": "Italy", "clue": "Boot."},
        {"word": "South Africa", "clue": "Three capitals."},
    ],
    "Sports": [
        {"word": "Cricket", "clue": "Bat ball."},
        {"word": "Football", "clue": "Goal."},
        {"word": "Basketball", "clue": "Hoop."},
        {"word": "Tennis", "clue": "Racket."},
        {"word": "Badminton", "clue": "Shuttle."},
        {"word": "Hockey", "clue": "Stick."},
        {"word": "Kabaddi", "clue": "Raid."},
        {"word": "Swimming", "clue": "Lap."},
        {"word": "Athletics", "clue": "Track."},
        {"word": "Boxing", "clue": "Ring."},
        {"word": "Wrestling", "clue": "Mat."},
        {"word": "Golf", "clue": "Hole."},
        {"word": "Chess", "clue": "Checkmate."},
        {"word": "Carrom", "clue": "Board."},
        {"word": "Volleyball", "clue": "Net."},
        {"word": "Table Tennis", "clue": "Small."},
        {"word": "Archery", "clue": "Target."},
        {"word": "Shooting", "clue": "Target."},
        {"word": "Formula 1", "clue": "Fast."},
        {"word": "Baseball", "clue": "Diamond."},
        {"word": "Rugby", "clue": "Oval."},
        {"word": "Cycling", "clue": "Wheels."},
        {"word": "Gymnastics", "clue": "Flexible."},
        {"word": "Snooker", "clue": "Cues."},
        {"word": "Kho Kho", "clue": "Tag."},
    ],
    "Movies": [
        {"word": "3 Idiots", "clue": "College."},
        {"word": "Sholay", "clue": "Classic."},
        {"word": "Baahubali", "clue": "Epic."},
        {"word": "Dangal", "clue": "Wrestling."},
        {"word": "Lagaan", "clue": "Cricket."},
        {"word": "RRR", "clue": "Friendship."},
        {"word": "KGF", "clue": "Gold."},
        {"word": "Avatar", "clue": "Blue."},
        {"word": "Avengers: Endgame", "clue": "Finale."},
        {"word": "Titanic", "clue": "Ship."},
        {"word": "Inception", "clue": "Dreams."},
        {"word": "The Dark Knight", "clue": "Joker."},
        {"word": "Jurassic Park", "clue": "Dinosaurs."},
        {"word": "Harry Potter", "clue": "Magic."},
        {"word": "Star Wars", "clue": "Force."},
        {"word": "The Matrix", "clue": "Pills."},
        {"word": "Pulp Fiction", "clue": "Briefcase."},
        {"word": "Forrest Gump", "clue": "Running."},
        {"word": "The Lion King", "clue": "Pride."},
        {"word": "Finding Nemo", "clue": "Lost."},
        {"word": "Interstellar", "clue": "Space."},
        {"word": "Gangs of Wasseypur", "clue": "Revenge."},
        {"word": "Zindagi Na Milegi Dobara", "clue": "Road trip."},
        {"word": "Parasite", "clue": "Basement."},
        {"word": "Oppenheimer", "clue": "Bomb."},
    ],
    "Occupations": [
        {"word": "Doctor", "clue": "Heals."},
        {"word": "Teacher", "clue": "Educates."},
        {"word": "Engineer", "clue": "Builds."},
        {"word": "Lawyer", "clue": "Argues."},
        {"word": "Police Officer", "clue": "Law."},
        {"word": "Chef", "clue": "Cooks."},
        {"word": "Farmer", "clue": "Grows."},
        {"word": "Pilot", "clue": "Flies."},
        {"word": "Artist", "clue": "Creates."},
        {"word": "Musician", "clue": "Plays."},
        {"word": "Actor", "clue": "Performs."},
        {"word": "Dancer", "clue": "Moves."},
        {"word": "Scientist", "clue": "Researches."},
        {"word": "Writer", "clue": "Writes."},
        {"word": "Journalist", "clue": "Reports."},
        {"word": "Mechanic", "clue": "Fixes."},
        {"word": "Plumber", "clue": "Pipes."},
        {"word": "Electrician", "clue": "Wires."},
        {"word": "Carpenter", "clue": "Wood."},
        {"word": "Firefighter", "clue": "Fire."},
        {"word": "Soldier", "clue": "Defends."},
        {"word": "Architect", "clue": "Designs."},
        {"word": "Accountant", "clue": "Numbers."},
        {"word": "Driver", "clue": "Drives."},
        {"word": "Shopkeeper", "clue": "Sells."},
    ],
    "Activities": [
        {"word": "Reading", "clue": "Books."},
        {"word": "Writing", "clue": "Pen."},
        {"word": "Cooking", "clue": "Food."},
        {"word": "Eating", "clue": "Hungry."},
        {"word": "Sleeping", "clue": "Tired."},
        {"word": "Running", "clue": "Fast."},
        {"word": "Walking", "clue": "Slow."},
        {"word": "Swimming", "clue": "Water."},
        {"word": "Dancing", "clue": "Music."},
        {"word": "Singing", "clue": "Voice."},
        {"word": "Painting", "clue": "Colors."},
        {"word": "Drawing", "clue": "Pencil."},
        {"word": "Gaming", "clue": "Screen."},
        {"word": "Watching TV", "clue": "Screen."},
        {"word": "Listening", "clue": "Ears."},
        {"word": "Talking", "clue": "Mouth."},
        {"word": "Thinking", "clue": "Brain."},
        {"word": "Studying", "clue": "Exams."},
        {"word": "Working", "clue": "Job."},
        {"word": "Travelling", "clue": "Places."},
        {"word": "Driving", "clue": "Car."},
        {"word": "Shopping", "clue": "Money."},
        {"word": "Cleaning", "clue": "Dirty."},
        {"word": "Gardening", "clue": "Plants."},
        {"word": "Cycling", "clue": "Wheels."},
    ],
    "Video Games": [
        {"word": "PUBG", "clue": "Battle royale."},
        {"word": "Free Fire", "clue": "Mobile."},
        {"word": "Minecraft", "clue": "Blocks."},
        {"word": "Grand Theft Auto V", "clue": "Stealing."},
        {"word": "Valorant", "clue": "Agents."},
        {"word": "CS:GO", "clue": "Counter-Terrorists."},
        {"word": "FIFA", "clue": "Football."},
        {"word": "Call of Duty", "clue": "Warfare."},
        {"word": "Among Us", "clue": "Imposter."},
        {"word": "Pokemon", "clue": "Catching."},
        {"word": "Super Mario", "clue": "Plumber."},
        {"word": "Red Dead Redemption 2", "clue": "Cowboy."},
        {"word": "Fortnite", "clue": "Building."},
        {"word": "League of Legends", "clue": "MOBA."},
        {"word": "Candy Crush", "clue": "Sweet."},
        {"word": "Drifto", "clue": "Rush"},
    ],
    "Superheroes": [
        {"word": "Iron Man", "clue": "Suit."},
        {"word": "Captain America", "clue": "Shield."},
        {"word": "Thor", "clue": "Hammer."},
        {"word": "Hulk", "clue": "Green."},
        {"word": "Spider-Man", "clue": "Webs."},
        {"word": "Black Widow", "clue": "Spy."},
        {"word": "Doctor Strange", "clue": "Magic."},
        {"word": "Black Panther", "clue": "King."},
        {"word": "Superman", "clue": "Kryptonite."},
        {"word": "Batman", "clue": "Rich."},
        {"word": "Wonder Woman", "clue": "Lasso."},
        {"word": "Flash", "clue": "Fast."},
        {"word": "Aquaman", "clue": "Water."},
        {"word": "Green Lantern", "clue": "Ring."},
        {"word": "Shaktimaan", "clue": "Indian."},
        {"word": "Krrish", "clue": "Mask."},
        {"word": "Wolverine", "clue": "Claws."},
        {"word": "Deadpool", "clue": "Fourth wall."},
        {"word": "Thanos", "clue": "Snap."},
        {"word": "Loki", "clue": "Trickster."},
        {"word": "Goku", "clue": "Saiyan."},
        {"word": "Vegeta", "clue": "Prince."},
        {"word": "One-Punch Man", "clue": "Single hit."},
        {"word": "Naruto", "clue": "Ninja."},
        {"word": "Luffy", "clue": "Pirate."},
    ]
}

# --- Category Icons ---
# To add icons, place your .png files in an 'assets/icons/' directory
# and map the category name to the filename here.
ICONS_DIR = os.path.join(os.path.dirname(__file__), 'assets', 'icons')
CATEGORY_ICONS = {
    "Clash Royale": os.path.join(ICONS_DIR, "clash_royale.png"),
    "Food": os.path.join(ICONS_DIR, "food.png"),
    "Animals": os.path.join(ICONS_DIR, "animals.png"),
    "Companies": os.path.join(ICONS_DIR, "companies.png"),
    "Cars": os.path.join(ICONS_DIR, "cars.png"),
    "Famous People": os.path.join(ICONS_DIR, "famous_people.png"),
    "Places": os.path.join(ICONS_DIR, "places.png"),
    "Sports": os.path.join(ICONS_DIR, "sports.png"),
    "Movies": os.path.join(ICONS_DIR, "movies.png"),
    "Occupations": os.path.join(ICONS_DIR, "occupations.png"),
    "Activities": os.path.join(ICONS_DIR, "activities.png"),
    "Video Games": os.path.join(ICONS_DIR, "video_games.png"),
    "Superheroes": os.path.join(ICONS_DIR, "superheroes.png"),
}

# --- Title Icon ---
# Define the path for the main title icon
TITLE_ICON_PATH = os.path.join(ICONS_DIR, "imposter_icon.png")


# --- Kivy Language Definition ---
KV_CODE = """
#:import hex kivy.utils.get_color_from_hex

# --- Color Palette (Pastels) ---
# Background: Off-White
# Text: Dark Grey
# Primary (Blue): #AEC6CF (Approx 0.68, 0.78, 0.81)
# Action (Green): #77DD77 (Approx 0.47, 0.87, 0.47)
# Danger (Red): #FF6961 (Approx 1.0, 0.41, 0.38)
# Highlight (Gold): #FDFD96 (Approx 0.99, 0.99, 0.59) - slightly darker for visibility: #F0E68C

<MainLabel@Label>:
    font_name: 'Poppins'
    text_size: self.width, None
    size_hint_y: None
    height: self.texture_size[1]
    font_size: '20sp'
    color: 0.25, 0.25, 0.25, 1  # Dark Grey Text
    halign: 'center'
    valign: 'middle'

<SetupInput@TextInput>:
    font_name: 'Poppins'
    background_normal: ''
    background_active: ''
    foreground_color: .12, .12, .14, 1
    cursor_color: 1, 0, 0, 1
    cursor_width: 4
    cursor_blink: True
    # center the text vertically by computing top/bottom padding from height and line_height
    line_height: self.font_size * 1.2
    padding: [14, (self.height - self.line_height) / 2, 14, (self.height - self.line_height) / 2]
    font_size: '16sp'
    multiline: False
    canvas.before:
        Color:
            rgba: (0.96, 0.92, 0.98, 1) if not self.focus else (0.98, 0.97, 1, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12]
        Color:
            rgba: (0.85, 0.78, 0.90, 1) if not self.focus else (0.35, 0.65, 0.95, 1)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
            width: 2 if self.focus else 1

# ADDED: Special TextInput for the player names screen
<NameInput@TextInput>:
    font_name: 'Poppins'
    background_normal: ''
    background_active: ''
    foreground_color: .12, .12, .14, 1
    cursor_color: 1, 0, 0, 1
    cursor_width: 4
    cursor_blink: True
    line_height: self.font_size * 1.2
    padding: [14, (self.height - self.line_height) / 2, 14, (self.height - self.line_height) / 2]
    font_size: '16sp'
    multiline: False
    canvas.before:
        Color:
            rgba: (0.96, 0.92, 0.98, 1) if not self.focus else (0.98, 0.97, 1, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [12]
        Color:
            rgba: (0.85, 0.78, 0.90, 1) if not self.focus else (0.35, 0.65, 0.95, 1)
        Line:
            rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
            width: 2 if self.focus else 1

# --- Rounded Button Definition ---
<RoundedButton@Button>:
    font_name: 'Poppins'
    background_normal: ''
    background_color: 0, 0, 0, 0 # Transparent default
    b_color: 0.6, 0.8, 0.95, 1 # Default Pastel Bcolourlue
    color: 0.2, 0.2, 0.2, 1 # Dark Text
    font_size: '20sp'
    bold: True
    size_hint_y: None
    height: '60dp'
    canvas.before:
        Color:
            # Darken slightly on press
            rgba: (self.b_color[0]*0.9, self.b_color[1]*0.9, self.b_color[2]*0.9, self.b_color[3]) if self.state == 'down' else self.b_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]

<CategoryButton@ButtonBehavior+BoxLayout>:
    b_color: 0.6, 0.8, 0.95, 1 # Default Pastel Blue
    height: '50dp'
    size_hint_y: None
    padding: [15, 0, 15, 0]
    spacing: 15
    canvas.before:
        Color:
            # Darken slightly on press
            rgba: (self.b_color[0]*0.9, self.b_color[1]*0.9, self.b_color[2]*0.9, self.b_color[3]) if self.state == 'down' else self.b_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [20,]
    Image:
        source: root.icon_source or ''
        size_hint_x: None
        width: self.height * 0.6
        opacity: 1 if root.icon_source else 0
        pos_hint: {'center_y': 0.5}
    Label:
        text: root.text
        font_name: 'Poppins'
        font_size: '18sp'
        color: 0.2, 0.2, 0.2, 1
        halign: 'left'
        valign: 'middle'
        text_size: self.width, None

<StartScreen>:
    name: 'start'
    BoxLayout: 
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1 # Off-White Background
            Rectangle:
                pos: self.pos
                size: self.size
        
        # --- Title ---
        MainLabel:
            text: 'Imposter!'
            font_size: '36sp'
            color: 0.4, 0.4, 0.4, 1 # Softer Grey Title
            size_hint_y: None
            height: '80dp'
            padding: [0, 20, 0, 20]

        ScrollView:
            bar_width: 5
            bar_color: 0.8, 0.8, 0.8, 1
            bar_inactive_color: 0.9, 0.9, 0.9, 1
            padding: 30, 0, 30, 0 
            
            BoxLayout: 
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 20
                padding: [20, 0, 20, 30]

                RoundedButton:
                    text: 'Setup Players'
                    on_release: root.go_to_player_setup()
                    b_color: 0.6, 0.8, 0.95, 1 # Pastel Blue

                MainLabel:
                    id: player_count_label
                    text: '0 Players Registered'
                    size_hint_y: None
                    height: '40dp'
                    color: 0.5, 0.5, 0.5, 1

                # Imposter Count Setup
                BoxLayout:
                    size_hint_y: None
                    height: '50dp'
                    MainLabel:
                        text: 'Number of Imposters:'
                        size_hint_x: 0.7
                        halign: 'left'
                    SetupInput:
                        id: imposter_count_input
                        text: root.imposter_count_str
                        on_text: root.update_imposter_count(self.text)

                # Joker Count Setup
                BoxLayout:
                    size_hint_y: None
                    height: '50dp'
                    MainLabel:
                        text: 'Number of Jokers:'
                        size_hint_x: 0.7
                        halign: 'left'
                    SetupInput:
                        id: joker_count_input
                        text: root.joker_count_str
                        on_text: root.update_joker_count(self.text)

                # No Clue Checkbox (aligned + hint)
                BoxLayout:
                    size_hint_y: None
                    height: '56dp'
                    padding: [0, 0, 0, 0]
                    spacing: 12

                    CheckBox:
                        id: no_clue_checkbox
                        active: root.hide_imposter_clue
                        on_active: root.hide_imposter_clue = self.active
                        size_hint: None, None
                        size: '28dp', '28dp'
                        pos_hint: {'center_y': 0.5}
                        color: 0.55, 0.20, 0.25, 1

                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 1
                        spacing: 2

                        MainLabel:
                            text: 'Hard Mode'
                            halign: 'left'
                            font_size: '16sp'
                            size_hint_y: None
                            height: '28dp'
                            color: 0.55, 0.20, 0.25, 1

                        Label:
                            text: 'Imposters will NOT see the clue'
                            font_size: '12sp'
                            color: 0.55, 0.20, 0.25, 1
                            halign: 'left'
                            valign: 'middle'
                            text_size: self.width, self.height
                            size_hint_y: None
                            height: '20dp'

                MainLabel:
                    text: 'Select Category:'
                    font_size: '20sp'
                    size_hint_y: None
                    height: '40dp'
                    color: 0.4, 0.4, 0.4, 1

                # Category Selection Grid
                GridLayout:
                    id: category_grid
                    cols: 2
                    spacing: 15
                    size_hint_y: None
                    height: self.minimum_height
                    row_default_height: '55dp'
                    row_force_default: True

                MainLabel:
                    id: status_message
                    text: ''
                    color: 1.0, 0.4, 0.4, 1  # Soft Red for error

                RoundedButton:
                    text: 'Debug'
                    on_release: root.manager.current = 'debug'
                    b_color: 0.95, 0.85, 0.5, 1 # Pastel Gold
                    size_hint_y: None
                    height: '50dp'
                    font_size: '16sp'

        # --- Start Button ---
        BoxLayout:
            size_hint_y: None
            height: '90dp'
            padding: [30, 15, 30, 15]
            
            RoundedButton:
                text: 'Start Game'
                on_release: root.start_game()
                # Pastel Green if ready, Grey if not
                b_color: (0.6, 0.9, 0.6, 1) if root.is_ready else (0.9, 0.9, 0.9, 1)
                # Dark grey text if ready, light grey if disabled
                color: (0.2, 0.2, 0.2, 1) if root.is_ready else (0.7, 0.7, 0.7, 1)
                disabled: not root.is_ready

# ADDED: New PlayerNamesScreen
<PlayerNamesScreen>:
    name: 'player_names'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size
        
        MainLabel:
            text: 'Enter Names'
            font_size: '32sp'
            color: 0.4, 0.4, 0.4, 1
            size_hint_y: None
            height: '60dp'
        
        ScrollView:
            size_hint_y: 1
            bar_width: 5
            BoxLayout:
                id: names_layout
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 15
                padding: [0, 10, 0, 10]
        
        # MODIFIED: Button layout
        BoxLayout:
            size_hint_y: None
            height: '140dp'
            orientation: 'vertical'
            spacing: 15
            
            RoundedButton:
                text: 'Add Player Slot'
                on_release: root.add_new_player_button_press()
                b_color: 0.6, 0.8, 0.95, 1 # Pastel Blue

            BoxLayout:
                size_hint_y: None
                height: '60dp'
                spacing: 15
                RoundedButton:
                    text: 'Clear'
                    on_release: root.clear_all_players()
                    b_color: 1.0, 0.65, 0.65, 1 # Pastel Red
                RoundedButton:
                    text: 'Save'
                    on_release: root.save_and_go_back()
                    b_color: 0.6, 0.9, 0.6, 1 # Pastel Green

<WordScreen>:
    name: 'word'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 30
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        MainLabel:
            # MODIFIED: Show player name
            text: root.player_name + "'s Turn"
            font_size: '36sp'
            color: 0.4, 0.4, 0.4, 1
            size_hint_y: None
            height: '80dp'

        BoxLayout:
            orientation: 'vertical'
            padding: 20
            spacing: 20
            # Card background
            canvas.before:
                Color:
                    rgba: 0.93, 0.93, 0.93, 1
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [20,]

            MainLabel:
                text: root.role_text if root.word_visible else "Role Hidden"
                font_size: '28sp'
                color: (0.6, 0.2, 0.8, 1) if root.role_text == 'JOKER' and root.word_visible else (0.4, 0.6, 0.8, 1)
                height: '50dp'
                bold: True


            MainLabel:
                text: root.word_clue_text if root.word_visible else "Tap 'Show' below"
                font_size: '32sp'
                color: 0.2, 0.2, 0.2, 1
                size_hint_y: 1

        # MODIFIED: Added Show/Hide button and put both buttons in a layout
        BoxLayout:
            size_hint_y: None
            height: '70dp'
            spacing: 20
            RoundedButton:
                text: 'Hide' if root.word_visible else 'Show'
                on_release: root.word_visible = not root.word_visible
                # Pastel Green vs Pastel Green
                b_color: 0.6, 0.9, 0.6, 1
            RoundedButton:
                text: 'Next'
                on_release: root.next_player()
                b_color: (0.95, 0.85, 0.5, 1) if root.word_visible else (0.6, 0.8, 0.95, 1) # Pastel Gold vs Pastel Blue

<DiscussionScreen>:
    name: 'discussion'
    BoxLayout:
        orientation: 'vertical'
        padding: 40
        spacing: 40
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        MainLabel:
            text: 'DISCUSS!'
            font_size: '50sp'
            color: 0.9, 0.4, 0.4, 1 # Soft Red
            size_hint_y: 0.4
            bold: True

        MainLabel:
            text: root.starting_player_text
            font_size: '24sp'
            size_hint_y: 0.4
            color: 0.2, 0.2, 0.2, 1

        RoundedButton:
            text: 'Reveal Results'
            on_release: root.go_to_reveal()
            b_color: 1.0, 0.65, 0.65, 1 # Pastel Red

# ADDED: New RevealScreen
<RevealScreen>:
    name: 'reveal'
    BoxLayout:
        orientation: 'vertical'
        padding: 30
        spacing: 15
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        MainLabel:
            text: 'RESULTS'
            font_size: '42sp'
            color: 0.6, 0.9, 0.6, 1
            size_hint_y: None
            height: '80dp'
            bold: True

        ScrollView:
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height
                spacing: 20
                padding: [0, 20, 0, 20]

                MainLabel:
                    text: root.chaos_text
                    font_size: '22sp'
                    color: 0.9, 0.4, 0.4, 1
                    size_hint_y: None
                    height: '40dp'
                
                BoxLayout:
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    canvas.before:
                        Color:
                            rgba: 0.86, 0.78, 0.95, 1   # Pastel purple background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    Label:
                        text: root.imposters_text
                        font_size: '24sp'
                        bold: True
                        color: 0.08, 0.08, 0.08, 1   # Dark text for contrast
                        size_hint_y: 1
                        text_size: self.width, self.height
                        halign: 'center'
                        valign: 'middle'
                BoxLayout:
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    canvas.before:
                        Color:
                            rgba: 0.6, 0.9, 0.6, 1      # Pastel green background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    Label:
                        text: root.word_text
                        font_size: '24sp'
                        bold: True
                        color: 0.08, 0.08, 0.08, 1   # Dark text for contrast
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.width, self.height
                    
                # Category panel (yellow)
                BoxLayout:
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    canvas.before:
                        Color:
                            rgba: 0.95, 0.85, 0.5, 1    # Pastel yellow background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    Label:
                        text: root.category_text
                        font_size: '24sp'
                        bold: True
                        color: 0.08, 0.08, 0.08, 1   # Dark text for contrast
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.width, self.height
                                # Joker panel (pastel blue, only if jokers present)
                                
                BoxLayout:
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    canvas.before:
                        Color:
                            rgba: 1.0, 0.65, 0.65, 1    # Pastel red background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    Label:
                        text: root.clue_text
                        font_size: '24sp'
                        bold: True
                        color: 0.08, 0.08, 0.08, 1   # Dark text for contrast
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.width, self.height

                # Winner selection panel (orange)
                BoxLayout:
                    orientation: 'horizontal'
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    spacing: 12
                    canvas.before:
                        Color:
                            rgba: 0.98, 0.78, 0.48, 1    # Pastel orange outer background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_x: 0.6
                        Label:
                            text: 'Who won?'
                            font_size: '24sp'
                            bold: True
                            color: 0.08, 0.08, 0.08, 1
                            halign: 'center'
                            valign: 'middle'
                            text_size: self.width, self.height
                    BoxLayout:
                        size_hint_x: 0.4
                        padding: [6, 6, 6, 6]
                        # Draw the rounded two-tone background and border on this container
                        canvas.before:
                            Color:
                                rgba: 1.0, 0.9, 0.7, 1   # Lighter orange inside
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [12,]
                            Color:
                                rgba: 0.9, 0.6, 0.2, 1   # Darker orange outline
                            Line:
                                rounded_rectangle: (self.x, self.y, self.width, self.height, 12)
                                width: 1.5
                        Spinner:
                            id: winner_spinner
                            text: root.winner
                            values: ['Imposter', 'Crewmates']
                            size_hint: 1, 1
                            font_name: 'Poppins'
                            font_size: '20sp'
                            background_normal: ''
                            background_down: ''
                            color: 0.08, 0.08, 0.08, 1
                            size_hint_y: None
                            height: '54dp'
                            pos_hint: {'center_y': 0.5}
                            on_text: root.on_winner_change(self.text)
                BoxLayout:
                    size_hint_y: None
                    height: '90dp'
                    padding: [12, 12, 12, 12]
                    opacity: 1 if root.joker_visible else 0
                    disabled: not root.joker_visible
                    canvas.before:
                        Color:
                            rgba: 0.6, 0.8, 0.95, 1    # Pastel blue background
                        RoundedRectangle:
                            pos: self.pos
                            size: self.size
                            radius: [12,]
                    Label:
                        text: root.jokers_text
                        font_size: '24sp'
                        bold: True
                        color: 0.08, 0.08, 0.08, 1   # Dark text for contrast
                        halign: 'center'
                        valign: 'middle'
                        text_size: self.width, self.height

        
        RoundedButton:
            text: 'Play Again'
            on_release: root.reset_game()
            b_color: 0.6, 0.9, 0.6, 1 
            size_hint_y: None
            height: '70dp'

<DebugScreen>:
    name: 'debug'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10
        canvas.before:
            Color:
                rgba: 0.98, 0.98, 0.98, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: None
            height: '56dp'
            spacing: 10

            RoundedButton:
                text: 'Back'
                on_release: root.manager.current = 'start'
                size_hint_x: None
                width: '90dp'
                b_color: 0.9, 0.9, 0.9, 1

            MainLabel:
                text: 'Debug'
                font_size: '28sp'
                halign: 'left'
                valign: 'middle'

        Label:
            id: user_id_label
            text: 'User ID: ' + root.user_id
            size_hint_y: None
            height: '28dp'
            color: 0.2, 0.2, 0.2, 1

        RoundedButton:
            text: 'Refresh'
            size_hint_y: None
            height: '44dp'
            on_release: root.load_debug_info()
            b_color: 0.6, 0.8, 0.95, 1

        TextInput:
            id: logs_input
            text: root.logs_text
            readonly: True
            background_color: 1,1,1,1
            foreground_color: 0.08,0.08,0.08,1
            font_name: 'Poppins'
            font_size: '14sp'
            multiline: True
            size_hint_y: 1

        # Button to clear logs and the uploaded archive (with confirmation)
        RoundedButton:
            text: 'Clear Logs & Uploaded Archive'
            size_hint_y: None
            height: '52dp'
            b_color: 1.0, 0.65, 0.65, 1
            on_release: root.confirm_clear_uploaded()

"""

def printtologs(text:str):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)
    file_path = os.path.join(data_dir,"logs.txt")
    
    current_time = datetime.datetime.now().strftime("%a %b %d %H:%M:%S %Y")
    
    try :
        with open(file_path, "a") as f:
            f.write(f"[{current_time}] : {text}\n")
    except Exception as e:
        print(f"failed to write log with : {e}")
    
RENDER_URL = "https://imposterbackend.onrender.com"
UPLOAD_URL = f"{RENDER_URL}/upload"
WAKE_URL = f"{RENDER_URL}/health"
    
def get_device_user_id():
    store = JsonStore("assets//device.json")
    if not store.exists("user_id"):
        store.put("user_id", value=str(uuid.uuid4()))
    return store.get("user_id")["value"]

def wake_backend():
    try:
        requests.get(WAKE_URL, timeout=3)
    except:
        pass

def upload_saved_games():
    user_id = get_device_user_id()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    saved_path = os.path.join(base_dir,"/data/","saved_games.json")
    uploaded_path = os.path.join(base_dir,"/data/", "saved_uploaded_games.json")

    if not os.path.exists(saved_path):
        printtologs("No saved games to upload")
        return

    try:
        with open(saved_path, "r", encoding="utf-8") as f:
            games = json.load(f) or {}
    except Exception as e:
        printtologs(f"Failed to load saved_games.json:{e}")
        return

    if not games:
        printtologs("No saved games to upload")
        return

    # Load previously uploaded games (if any)
    uploaded_games = {}
    if os.path.exists(uploaded_path):
        try:
            with open(uploaded_path, "r", encoding="utf-8") as f:
                uploaded_games = json.load(f) or {}
        except Exception as e:
            printtologs(f"Warning: could not read saved_uploaded_games.json: {e}")

    any_uploaded = False

    # Upload games one-by-one so we can move only those that succeed
    for game_id, game_data in list(games.items()):
        payload = {"user_id": user_id, "games": {game_id: game_data}}
        try:
            r = requests.post(UPLOAD_URL, json=payload, timeout=10)
            if 200 <= r.status_code < 300:
                printtologs(f"Uploaded game {game_id}: {r.status_code} {r.text}")
                uploaded_games[game_id] = game_data
                del games[game_id]
                any_uploaded = True
            else:
                printtologs(f"Upload failed for {game_id}: {r.status_code} {r.text}")
        except Exception as e:
            printtologs(f"Upload failed for {game_id}: {e}")

    # Save remaining (not-yet-uploaded) games back to saved_games.json
    try:
        with open(saved_path, "w", encoding="utf-8") as f:
            json.dump(games, f, indent=2, ensure_ascii=False)
    except Exception as e:
        printtologs(f"Warning: failed to write saved_games.json: {e}")

    # If any were uploaded, persist the uploaded archive
    if any_uploaded:
        try:
            with open(uploaded_path, "w", encoding="utf-8") as f:
                json.dump(uploaded_games, f, indent=2, ensure_ascii=False)
        except Exception as e:
            printtologs(f"Warning: failed to write saved_uploaded_games.json: {e}")


class RoundedButton(Button):
    # This property is required because your KV code references 'self.b_color'
    b_color = ListProperty([0.2, 0.6, 1, 1])  # Default Blue
    
    # You might also be missing this if you used it in the KV for text color
    t_color = ListProperty([1, 1, 1, 1])      # Default White
    
    # You might be missing this for radius control
    radius = ListProperty([20])

class CategoryButton(ButtonBehavior, BoxLayout):
    """A clickable BoxLayout that displays text and an optional icon."""
    text = StringProperty('')
    icon_source = StringProperty('')
    b_color = ListProperty([0.6, 0.8, 0.95, 1]) # Default Pastel Blue
    category_name = StringProperty('') # To hold the category name for logic

    def on_touch_move(self, touch):
        # This resolves a Pylance reportIncompatibleMethodOverride error
        # by explicitly matching the ButtonBehavior signature.
        return super().on_touch_move(touch)

    def on_touch_down(self, touch: MotionEvent) -> bool:
        # This resolves a Pylance reportIncompatibleMethodOverride error
        # by explicitly matching the ButtonBehavior signature.
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        # This resolves a Pylance reportIncompatibleMethodOverride error
        # by explicitly matching the ButtonBehavior signature.
        return super().on_touch_up(touch)
    
# --- Python Application Logic ---
class GameState:
    """Singleton class to hold and manage game state."""
    def __init__(self):
        # MODIFIED: These are now persistent
        self.player_names = []
        self.total_players = 0
        # Store completed games: sequential id -> dict of game data
        self.saved_games = {}
        self.next_game_id = 1
        self.reset()
        # Attempt to load existing saved games from disk
        try:
            self.load_saved_games()
        except Exception:
            # Don't fail initialization if loading fails
            pass

    def get_saved_games_path(self):
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(data_dir, exist_ok=True)
        return os.path.join(data_dir, 'saved_games.json')

    def load_saved_games(self):
        path = self.get_saved_games_path()
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                # Keys in JSON will be strings; convert to int keys internally if desired
                # We'll keep them as strings for JSON compatibility but update next_game_id
                self.saved_games = data
                # compute next_game_id
                try:
                    keys = [int(k) for k in data.keys()]
                    self.next_game_id = max(keys) + 1
                except Exception:
                    self.next_game_id = max([int(k) for k in data.keys()]) + 1 if data else 1
            except Exception:
                # If file is corrupt, ignore it
                self.saved_games = {}
                self.next_game_id = 1

    def save_saved_games(self):
        path = self.get_saved_games_path()
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(self.saved_games, f, indent=2, ensure_ascii=False)
        except Exception as e:
            printtologs(f"Warning: failed to save saved_games.json: {e}")

    def reset(self):
        """MODIFIED: Resets game logic, but NOT player names."""
        # self.total_players and self.player_names are NOT reset
        self.imposter_count = 1
        self.joker_count = 0
        self.chaos_mode = False
        self.selected_categories = []
        self.word = ""
        self.clue = ""
        self.imposter_ids = []
        self.joker_ids = []
        self.current_player_index = 0
        self.game_started = False
        self.hide_imposter_clue = False
        self.starting_player_id = 1
        self.is_chaos_game = False
        # Track per-category pools so we don't repeat words until exhausted
        # Keys: category name -> list of remaining word/clue dicts (shuffled)
        self.available_words = {}
    
    def clear_player_names(self):
        """ADD: Resets the player list and count."""
        self.player_names = []
        self.total_players = 0

    def setup_game(self, category_keys): # MODIFIED: receives a list
        self.game_started = True
        self.is_chaos_game = False
        
        # 1. Select Category from the list
        if not category_keys:
            # Fallback if list is empty
            self.word = "No Category Selected"
            self.clue = "Please select a category"
            printtologs("ERROR: No categories selected.")
            return
        
        self.selected_category = random.choice(category_keys)

        # 2. Select Word/Clue
        # Use a list of keys to prevent iteration issues if dictionary changes
        category_list = list(GAME_DATA[self.selected_category])
        if not category_list:
            # Fallback if a category is somehow empty
            self.word = "No Word Found"
            self.clue = "No Clue Found"
            printtologs(f"ERROR: Category '{self.selected_category}' is empty.")
            return

        # Improved randomness: use a per-category shuffled pool and pop from it
        pool = self.available_words.get(self.selected_category)
        if not pool:
            # Recreate and shuffle pool when empty or not present
            pool = list(GAME_DATA[self.selected_category])
            random.shuffle(pool)
            self.available_words[self.selected_category] = pool

        # Pop an item from the pool to avoid repeats until exhausted
        word_clue_pair = self.available_words[self.selected_category].pop()
        # If pop leaves pool empty, it'll be recreated next round
        self.word = word_clue_pair["word"]
        self.clue = word_clue_pair["clue"]

        # 3. Determine Imposter and Joker IDs
        total = self.total_players
        imposters = self.imposter_count
        jokers = getattr(self, 'joker_count', 0)

        # Check for chaos mode (1% chance)
        if random.random() < 0.01:
            self.imposter_ids = list(range(1, total + 1))
            self.joker_ids = []
            self.is_chaos_game = True
        else:
            # Ensure imposter + joker count is never more than players
            available_ids = list(range(1, total + 1))
            actual_imposters = min(imposters, total - 1) if total >= 2 else 0
            # Remove imposter IDs from available for jokers
            self.imposter_ids = []
            self.joker_ids = []
            if actual_imposters > 0:
                self.imposter_ids = sorted(random.sample(available_ids, actual_imposters))
            # Now pick jokers from those not imposters
            joker_pool = [pid for pid in available_ids if pid not in self.imposter_ids]
            actual_jokers = min(jokers, len(joker_pool))
            if actual_jokers > 0 and joker_pool:
                self.joker_ids = sorted(random.sample(joker_pool, actual_jokers))

        # 4. Set starting player
        if self.total_players > 0:
            self.starting_player_id = random.randint(1, self.total_players)
        else:
            self.starting_player_id = 1

        printtologs(f"Game Setup: Category={self.selected_category}, Word='{self.word}', Clue='{self.clue}'")
        printtologs(f"Imposter IDs: {self.imposter_ids}")
        printtologs(f"Joker IDs: {self.joker_ids}")
        printtologs(f"Starting Player: {self.starting_player_id}")

    def get_role_data(self, player_id):
        """Returns the role and text for a given player ID."""
        if player_id in getattr(self, 'imposter_ids', []):
            # Imposter Role
            if self.is_chaos_game:
                role = "IMPOSTER"
                text =  f"Your CLUE is: {self.clue}"
            else:
                role = "IMPOSTER"
                if self.hide_imposter_clue:
                    text = "You are the IMPOSTER!"
                else:
                    text = f"Your CLUE is: {self.clue}"
            role_color = [1, 0.3, 0.3, 1] # Red
        elif player_id in getattr(self, 'joker_ids', []):
            # Joker Role
            role = "JOKER"
            text = f"The WORD is: {self.word}\n(Act suspicious! Try to get voted out.)"
            role_color = [0.6, 0.2, 0.8, 1] # Purple
        else:
            # Normal Player Role
            role = "NORMAL PLAYER"
            text = f"The WORD is: {self.word}"
            role_color = [0.3, 0.8, 0.9, 1] # Blue

        return role, text, role_color
    
    def get_player_name(self, player_id):
        """ADD: Safely gets a player name by their 1-based ID."""
        # player_id is 1-based, list is 0-based
        if player_id > 0 and player_id <= len(self.player_names):
            return self.player_names[player_id - 1]
        return f"Player {player_id}" # Fallback

GAME = GameState()

class StartScreen(Screen):
    """Screen for game setup: player/imposter count, chaos mode, category selection."""
    # MODIFIED: Removed total_players_str
    imposter_count_str = StringProperty("1")
    joker_count_str = StringProperty("0")  # Joker count property
    chaos_mode = BooleanProperty(False)
    selected_categories = ListProperty([]) # MODIFIED: from category to categories
    hide_imposter_clue = BooleanProperty(False) # ADDED
    is_ready = BooleanProperty(False)
    title_icon_path = StringProperty('') # Path for the title icon

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(selected_categories=self.check_ready) # MODIFIED
        # MODIFIED: Removed total_players_str binding
        self.bind(imposter_count_str=self.check_ready)
        self.bind(joker_count_str=self.check_ready)
        # MODIFIED: Populate categories on entering the screen
        self.on_enter = self.refresh_player_count
        # Set the icon path, checking if the file exists
        if os.path.exists(TITLE_ICON_PATH):
            self.title_icon_path = TITLE_ICON_PATH


    def refresh_player_count(self, *args):
        """ADD: Called on_enter to update player count label and re-validate."""
        self.populate_categories() # Ensures categories are drawn
        self.ids.player_count_label.text = f"{len(GAME.player_names)} Players Registered"
        self.check_ready() # Re-run validation

    def go_to_player_setup(self):
        """ADD: Switches to the player name setup screen."""
        self.manager.current = 'player_names'

    def populate_categories(self, *args):
        """Dynamically create category buttons."""
        grid = self.ids.category_grid
        # Clear existing widgets to handle re-entry
        grid.clear_widgets()

        # MODIFIED: Iterate through categories and create buttons with icons
        for category in sorted(GAME_DATA.keys()):
            icon_path = CATEGORY_ICONS.get(category)
            btn = Factory.CategoryButton(
                text=category,
                icon_source=icon_path if icon_path and os.path.exists(icon_path) else ''
            )
            btn.bind(on_release=self.select_category)
            btn.category_name = category  # Store the category name on the button itself
            grid.add_widget(btn)

        # Re-highlight all previously selected categories
        self.highlight_categories()

    def select_category(self, button):
        """MODIFIED: Handles category button presses by adding/removing from list."""
        category_name = button.category_name
        if category_name in self.selected_categories:
            self.selected_categories.remove(category_name)
        else:
            self.selected_categories.append(category_name)
        
        # Re-run highlight logic
        self.highlight_categories()

    def highlight_categories(self):
        """Updates the button color based on selection."""
        for widget in self.ids.category_grid.children:
            if widget.category_name in self.selected_categories:
                # Pastel Gold for selected
                widget.b_color = [0.95, 0.85, 0.5, 1] 
            else:
                # Pastel Blue for unselected
                widget.b_color = [0.6, 0.8, 0.95, 1]

    def update_imposter_count(self, text):
        """Updates imposter_count_str property and validates."""
        self.imposter_count_str = text or "0"
        self.validate_settings()

    def update_joker_count(self, text):
        """Updates joker_count_str property and validates."""
        self.joker_count_str = text or "0"
        self.validate_settings()

    def check_ready(self, *args):
        """Checks if the game is ready to be started."""
        self.is_ready = (self.validate_settings() is True)

    def validate_settings(self):
        """Performs validation checks for player, imposter, and joker counts."""
        try:
            total = len(GAME.player_names)
            GAME.total_players = total
            imposters = int(self.imposter_count_str or "0")
            jokers = int(self.joker_count_str or "0")
        except ValueError:
            self.ids.status_message.text = "Error: Counts must be whole numbers."
            return False

        if total < 3:
            self.ids.status_message.text = "Add at least 3 players to start."
            return False
        if imposters < 1:
            self.ids.status_message.text = "Minimum 1 imposter required."
            return False
        if imposters + jokers > total:
            self.ids.status_message.text = "Imposters + Jokers must not exceed total players."
            return False
        if imposters >= total:
            self.ids.status_message.text = "Imposters must be fewer than total players."
            return False

        if not self.selected_categories:
            self.ids.status_message.text = "Please select a category."
            return False
        for cat in self.selected_categories:
            if cat not in GAME_DATA or not GAME_DATA[cat]:
                self.ids.status_message.text = f"Error: Category '{cat}' is empty or invalid."
                return False

        self.ids.status_message.text = ""
        GAME.imposter_count = imposters
        GAME.joker_count = jokers
        return True

    def start_game(self):
        """MODIFIED: Initializes game state and moves to the first WordScreen."""
        if not self.is_ready:
            return

        GAME.reset() # Reset game logic (but not players)

        # Re-set settings for this round
        GAME.total_players = len(GAME.player_names)
        GAME.imposter_count = int(self.imposter_count_str)
        GAME.joker_count = int(self.joker_count_str)  # FIX: Set joker_count after reset
        GAME.chaos_mode = self.chaos_mode
        GAME.hide_imposter_clue = self.hide_imposter_clue

        # The game state is reset and set up using the validated properties
        GAME.setup_game(self.selected_categories) # MODIFIED

        # Check if setup failed (e.g., if category was empty, though validation should catch this)
        if not GAME.game_started:
            self.ids.status_message.text = "Game setup failed. Please check categories."
            return

        # MODIFIED: Go directly to word screen
        word_screen = self.manager.get_screen('word')
        word_screen.init_player_view(1)
        self.manager.current = 'word'
    
    upload_saved_games()

# ADDED: New Screen for entering player names
class PlayerNamesScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name_inputs = [] # Keep track of the text inputs

    def on_enter(self, *args):
        """Dynamically create TextInput fields based on saved player names."""
        self.name_inputs.clear()
        layout = self.ids.names_layout
        layout.clear_widgets()

        if not GAME.player_names:
            # If no players are saved, default to 3 empty slots
            for i in range(3):
                self.add_player_field()
        else:
            # If players are saved, create a field for each one
            for name in GAME.player_names:
                self.add_player_field(name)

    def add_player_field(self, name=""):
        """Adds a new text input row to the layout."""
        layout = self.ids.names_layout
        
        hbox = BoxLayout(size_hint_y=None, height='55dp', spacing=10)
        hbox.add_widget(Label(
            text=f"Player {len(self.name_inputs) + 1}:",
            size_hint_x=0.3,
            font_size='18sp',
            color=(0.2, 0.2, 0.2, 1) # Dark Text
        ))
        
        # Using factory to create the styled NameInput
        text_input = Factory.NameInput(text=name)
        self.name_inputs.append(text_input)
        hbox.add_widget(text_input)
        
        layout.add_widget(hbox)

    def add_new_player_button_press(self):
        """Adds one new empty player slot."""
        self.add_player_field()
    
    def clear_all_players(self):
        """Clears names from GAME state and refreshes the screen."""
        GAME.clear_player_names()
        self.on_enter() # Re-run on_enter to show the 3 default empty slots

    def save_and_go_back(self):
        """Save non-empty names to game state and return to StartScreen."""
        names = []
        for text_input in self.name_inputs:
            name = text_input.text.strip()
            if name: # Only save non-empty names
                names.append(name)
        
        GAME.player_names = names
        GAME.total_players = len(GAME.player_names) # Update total players
        printtologs(f"Player names saved: {GAME.player_names}")

        self.manager.current = 'start'


class WordScreen(Screen):
    """Screen for individual players to view their role, word, or clue."""
    current_player_id = NumericProperty(0)
    player_name = StringProperty("") # ADDED
    role_text = StringProperty("")
    word_clue_text = StringProperty("")
    word_visible = BooleanProperty(False) # ADDED

    def init_player_view(self, player_id):
        """Set up the screen for a specific player."""
        self.current_player_id = player_id
        self.player_name = GAME.get_player_name(player_id) # ADDED
        # Role color is not used in the KV binding but is returned for completeness
        role, text, role_color = GAME.get_role_data(player_id)
        self.role_text = role
        self.word_clue_text = text
        self.word_visible = False # ADDED: Ensure word is hidden for new player

    def next_player(self):
        """Advances to the next player's view or to the discussion screen."""
        if self.current_player_id < GAME.total_players:
            next_id = self.current_player_id + 1
            self.init_player_view(next_id)
        else:
            # All players have seen their role, start discussion
            self.manager.get_screen('discussion').on_enter()
            self.manager.current = 'discussion'


class DiscussionScreen(Screen):
    """MODIFIED: Screen to signal the discussion phase and who starts."""
    starting_player_text = StringProperty("")

    def on_enter(self, *args):
        """Update results when entering the screen."""
        # MODIFIED: Use player name
        self.starting_player_text = f"{GAME.get_player_name(GAME.starting_player_id)} starts the discussion!"

    def go_to_reveal(self):
        """MODIFIED: Moves to the reveal screen without resetting."""
        self.manager.get_screen('reveal').on_enter()
        self.manager.current = 'reveal'

# ADDED: New Screen for revealing all answers
class RevealScreen(Screen):
    """Screen to show all results at the end of the game."""
    chaos_text = StringProperty("")
    imposters_text = StringProperty("")
    word_text = StringProperty("")
    clue_text = StringProperty("")
    category_text = StringProperty("")
    winner = StringProperty('Crewmates')
    jokers_text = StringProperty("")
    joker_visible = BooleanProperty(False)

    def on_enter(self, *args):
        """Populate all the answer fields."""
        if GAME.is_chaos_game:
            self.chaos_text = "CHAOS MODE WAS ACTIVE!"
            self.imposters_text = "Everyone was an Imposter!"
        else:
            self.chaos_text = "Chaos Mode was Inactive"
            if not GAME.imposter_ids:
                self.imposters_text = "ERROR: No Imposters"
            else:
                # MODIFIED: Use player names
                names_list = [GAME.get_player_name(pid) for pid in GAME.imposter_ids]
                self.imposters_text = "Imposters: " + ", ".join(names_list)

        self.word_text = f"Word: {GAME.word or 'N/A'}"

        # Populate category text
        self.category_text = f"Category: {getattr(GAME, 'selected_category', 'N/A') or 'N/A'}"

        # Joker panel logic
        if hasattr(GAME, 'joker_count') and GAME.joker_count > 0 and hasattr(GAME, 'joker_ids') and GAME.joker_ids:
            joker_names = [GAME.get_player_name(pid) for pid in GAME.joker_ids]
            self.jokers_text = "Joker: " + ", ".join(joker_names)
            self.joker_visible = True
        else:
            self.jokers_text = ""
            self.joker_visible = False
        
        # Populate winner from saved GAME value or default
        self.winner = getattr(GAME, 'winner', 'Crewmates')
        GAME.winner = self.winner

        if GAME.hide_imposter_clue:
            self.clue_text = "The Clue was: Hidden (Hard Mode)"
        else:
            self.clue_text = f"Clue: {GAME.clue or 'N/A'}"

    def on_winner_change(self, text):
        """Called from KV when the spinner changes - save selection to GAME."""
        self.winner = text
        GAME.winner = text

    def reset_game(self):
        """MODIFIED: Resets round state and returns to the start screen."""
        # Save this game's summary before resetting
        try:
            game_id = GAME.next_game_id
        except AttributeError:
            GAME.next_game_id = 1
            game_id = 1

        summary = {
            'category': getattr(GAME, 'selected_category', None),
            'word': GAME.word,
            'clue': GAME.clue,
            'imposters': list(GAME.imposter_ids),
            'imposter_names': [GAME.get_player_name(pid) for pid in GAME.imposter_ids],
            'joker_names':[GAME.get_player_name(pid) for pid in GAME.joker_ids],
            'player_names': list(GAME.player_names),
            'total_players': GAME.total_players,
            'winner': getattr(GAME, 'winner', None),
            'is_chaos_game': GAME.is_chaos_game,
            'ended_at': datetime.datetime.now().isoformat()
        }

        # Ensure the saved_games dict exists
        if not hasattr(GAME, 'saved_games'):
            GAME.saved_games = {}
            GAME.next_game_id = game_id + 1

        # Save under string key for JSON compatibility
        GAME.saved_games[str(game_id)] = summary
        GAME.next_game_id = game_id + 1

        # Persist to disk
        try:
            GAME.save_saved_games()
        except Exception:
            printtologs("Warning: could not write saved_games.json")
        
        upload_saved_games()
        
        # Now reset round state (but keep saved_games and player list)
        GAME.reset() # Does not clear players
        self.manager.current = 'start'


class DebugScreen(Screen):
    """Debug screen showing logs and user id."""
    logs_text = StringProperty('')
    user_id = StringProperty('')

    def on_enter(self, *args):
        self.load_debug_info()

    def load_debug_info(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        logs_path = os.path.join(data_dir, "logs.txt")

        try:
            with open(logs_path, "r", encoding="utf-8") as f:
                self.logs_text = f.read()
        except Exception as e:
            self.logs_text = f"Could not read logs: {e}"

        try:
            # Use the new device-backed user id implementation
            self.user_id = get_device_user_id()
        except Exception as e:
            # Fall back to a helpful message if retrieval fails
            self.user_id = f"(no device user id: {e})"

    def confirm_clear_uploaded(self):
        """Show a confirmation popup before clearing logs and uploaded archive."""
        content = BoxLayout(orientation='vertical', spacing=12, padding=12)
        msg = Label(text='This will clear logs.txt and reset saved_uploaded_games.json to {}. Continue?', halign='center', valign='middle')
        msg.text_size = (self.width * 0.9, None)
        msg.size_hint_y = None
        msg.height = '80dp'
        content.add_widget(msg)

        buttons = BoxLayout(size_hint_y=None, height='48dp', spacing=12)
        btn_cancel = RoundedButton(text='Cancel', b_color=(0.9,0.9,0.9,1))
        btn_confirm = RoundedButton(text='Confirm', b_color=(1.0,0.65,0.65,1))
        buttons.add_widget(btn_cancel)
        buttons.add_widget(btn_confirm)
        content.add_widget(buttons)

        popup = Popup(title='Confirm Clear', content=content, size_hint=(0.8, None), height='200dp', auto_dismiss=False)

        btn_cancel.bind(on_release=lambda *_: popup.dismiss())
        btn_confirm.bind(on_release=lambda *_: (popup.dismiss(), self.clear_uploaded_data()))

        popup.open()

    def clear_uploaded_data(self):
        """Clear the log file and reset the uploaded games archive to an empty dict."""
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)
        logs_path = os.path.join(data_dir, "logs.txt")
        uploaded_path = os.path.join(data_dir, "saved_uploaded_games.json")

        try:
            # Truncate logs
            with open(logs_path, 'w', encoding='utf-8') as f:
                f.write('')
            # Reset uploaded games archive
            with open(uploaded_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, indent=2)

            # Refresh UI
            self.logs_text = ''
            try:
                self.user_id = get_device_user_id()
            except Exception:
                pass

            printtologs("Cleared logs and saved_uploaded_games.json")
        except Exception as e:
            printtologs(f"Failed to clear logs/uploaded archive: {e}")


class ImposterApp(App):
    """Main application class."""
    def build(self):
        
        wake_backend()
        
        # Load the KV design string
        Builder.load_string(KV_CODE)
        self.user_id = get_device_user_id()
        # Set up the Screen Manager
        sm = ScreenManager()
        sm.add_widget(StartScreen(name='start'))
        sm.add_widget(PlayerNamesScreen(name='player_names')) # ADDED
        sm.add_widget(WordScreen(name='word'))
        sm.add_widget(DiscussionScreen(name='discussion'))
        sm.add_widget(RevealScreen(name='reveal')) # ADDED
        sm.add_widget(DebugScreen(name='debug'))

        # Set initial values for the start screen
        start_screen = sm.get_screen('start')

        # Safely choose a default category that exists and is not empty
        available_categories = [k for k, v in GAME_DATA.items() if v]
        if available_categories:
            # MODIFIED: Select a list with one random item
            start_screen.selected_categories = [random.choice(available_categories)]
        else:
            start_screen.selected_categories = [] # MODIFIED

        # Set initial player counts
        # MODIFIED: Removed total_players_str
        start_screen.imposter_count_str = "1"
        start_screen.chaos_mode = False
        start_screen.hide_imposter_clue = False # ADDED

        # Run validation to set up initial is_ready state
        start_screen.validate_settings()
        start_screen.check_ready()

        return sm

if __name__ == '__main__':
    ImposterApp().run()