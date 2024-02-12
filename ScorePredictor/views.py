from django.shortcuts import render
from .helper import teams, city
from django.contrib import messages
import pandas as pd
import pickle

pipe = pickle.load(open('ScorePredictor\ipl_score_prediction_pipe_without_last_five.pkl','rb'))

City = city()
Team = teams()

def home(request):
    context = {"teams": Team, "cities": City}  # Include the cities in the context
    if request.method == "POST":
        try:
            batting_team = request.POST.get('batting_team')
            bowling_team = request.POST.get('bowling_team')
            city_selected = request.POST.get('city')
            wickets = int(request.POST.get('wickets', 0))
            current_score = int(request.POST.get('current_score', 0))
            overs = float(request.POST.get('overs', 0))
            balls = int(request.POST.get('balls', 0))

            # Validate input
            if not (batting_team and bowling_team and city_selected):
                raise ValueError("Please select all required fields.")

            if not (0 <= wickets <= 10 and current_score >= 0 and overs >= 0 and 0 <= balls <= 5):
                raise ValueError("Invalid input values.")

            total_balls = overs * 6 + balls

            input_df = pd.DataFrame({
                "batting_team": [batting_team],
                "bowling_team": [bowling_team],
                "city": [city_selected],
                "current_score": [current_score],
                "balls_left": [120 - total_balls],
                "wickets_left": [10 - wickets],
                "crr": [current_score * 6 / total_balls],
            })


            result = pipe.predict(input_df)

            return render(request, 'ScorePredictor/home.html', {'result': round(result[0]), 'cities': City, "teams": Team, 
                                                                "cities": City, 'batting_team':batting_team,
                                                                'bowling_team':bowling_team, 'wickets':wickets,
                                                                'balls':balls, 'overs':overs, 
                                                                'city':city_selected, 'current_score':current_score,
                                                                })  # Pass cities to the template
        except ValueError as ve:
            messages.info(request, str(ve))
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            
    return render(request, 'ScorePredictor/home.html', context)
