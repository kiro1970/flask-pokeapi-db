print('LOADING ROUTES')
from urllib import response
from app import app
from flask import render_template, request,jsonify
import requests
import json
print('LOADING ROUTES 2')
from app import services
from .forms import PokeForm, PokeResults
from app import db
from app.models import BattleDB
#from services import Pokemon
#from services import getpokedata
print('LOADING ROUTES 3')

@app.route('/')
def home():
    print('IN HOME RUTE!!!!!!')
    return render_template('index.html', title="PokeAPI BattlerXXX!")

@app.route('/howitworks')
def about():
    return render_template('howitworks.html', title="Learn how to battle!")

@app.route('/letsbattle')
def view():
    form = PokeForm()
    pokemon1 = None
    pokemon2 = None
    return render_template('letsbattle.html', title="Let's Battle!", form=form, pokemon1 = pokemon1, pokemon2 = pokemon2)

@app.route('/letsbattle', methods=['POST'])
def battle():
    form = PokeForm()
    pokemon1input = request.form.get("pokemon1input")
    pokemon2input = request.form.get("pokemon2input")
    
    pokemon1 = services.getpokedata(pokemon1input)
    pokemon1 = services.Pokemon(pokemon1)
    pokemon2 = services.getpokedata(pokemon2input)
    pokemon2 = services.Pokemon(pokemon2)
    outcome1 = pokemon1.attack - pokemon2.defense
    outcome2 = pokemon2.attack - pokemon1.defense
    if outcome1 > outcome2:
        winner = pokemon1
    elif outcome2 > outcome1:
        winner = pokemon2
    elif pokemon1.hp > pokemon2.hp:
        winner = pokemon1
    else:
         winner = pokemon2
    print(winner.name)
    battle = BattleDB(YourPokemon=pokemon1.name, OpponentsPokemon=pokemon2.name, Winner=winner.name)
    db.session.add(battle)
    db.session.commit()
    return render_template('letsbattle.html', form=form, title="Let's Battle!", winner=winner, pokemon1=pokemon1, pokemon2=pokemon2)

@app.route('/results', methods=['POST', 'GET']) 
def results():
    form = PokeResults()
    lines = BattleDB.query.all()
    return render_template('results.html', form=form, lines=lines)
    

