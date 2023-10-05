from django.shortcuts import render
import urllib.request
import urllib.error
import json
import urllib.parse

def index(request):
    # Initialize the data dictionary to store the context for rendering the template
    data = {}
    
    if request.method == 'POST':
        # Retrieve the city name entered by the user in the form.
        city = request.POST.get('city', '')
        
        if city:
            try:
                # Replace with your OpenWeatherMap API key
                api_key = '38e19855da536113006fd4aa01261bf4'

                # Encode the city name to ensure it's URL-safe.
                encoded_city = urllib.parse.quote(city)

                # Construct the API URL for retrieving weather data.
                url = f'https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&units=metric&lang=sr&appid={api_key}'
                
                # Fetch weather data from the API.
                with urllib.request.urlopen(url) as source:
                    list_of_data = json.load(source)

                # Prepare data for rendering in the template.
                data = {
                    "country_code": list_of_data['sys']['country'],
                    "coordinate": f"{list_of_data['coord']['lon']}, {list_of_data['coord']['lat']}",
                    "temp": f"{list_of_data['main']['temp']} °C",
                    "pressure": list_of_data['main']['pressure'],
                    "humidity": list_of_data['main']['humidity'],
                    'description': list_of_data['weather'][0]['description'],
                    'icon': list_of_data['weather'][0]['icon'],
                }
            except urllib.error.HTTPError as e:
                if e.code == 404:
                    # Handle the case when the city is not found.
                    data['error_message'] = f"City '{city}' not found."
                else:
                    # Handle other HTTP errors.
                    data['error_message'] = f"An error occurred while fetching data for '{city}'."

    # Render the template with the data.
    return render(request, "main/index.html", data)
