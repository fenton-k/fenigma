# Fenigma - Geolocation-based Enigma Finder
Fenigma is a web-based application that allows users to input starting and destination points, geocode them, and search for locations using an API. Based on the coordinates, the app then finds related "enigmas" (places or items of interest), displaying the results dynamically in a visually engaging card format.

## Features
- Interactive UI: Input starting and destination points, and get results displayed on interactive cards with rotating images.
- API Integration: Fetch search results from a backend API to display related enigmas.
- Responsive Design: Optimized for a variety of screen sizes, with a flexible grid-based layout.

## Usage
To view the live demo, visit https://fenton-k.github.io/fenigma/, hosted right here on [GitHub pages](https://pages.github.com/)!

To use the tool, enter a starting point (e.g., an address or place) and a destination. You can use addresses, cities, and (some) places of interest!

Once both fields have valid locations (their coordinates will be displayed), click the "Find enigmas" button.

Results will be shown as clickable cards, each representing an enigma. Cards are styled with images and text, and will rotate randomly for a dynamic effect.

## Configuration
The application fetches geolocation data using the Geoapify API. To use this service, you will need a valid API key, which can be inserted in the JavaScript code at the line:

```js
Copy
"https://api.geoapify.com/v1/geocode/search?text=" + el.value + "&format=json&apiKey=YOUR_API_KEY"
Replace YOUR_API_KEY with your own API key.
```

## API
The app makes use of a custom Python backend, hosted as a Flask application. 

Routes can be customized based on site needs, but current functions include:
- Converting locations to latitude/longitude pairs and calculate the distance between two locations.
- Generating Google Maps direction links between two locations.
- Computing a series of intermediate geographic points between two locations, useful for creating travel routes or paths.
- Identifiying destinations within a given radius by processing geolocation data from a CSV file, returning the nearest destinations.

For fenigma, the api returns a JSON list of enigmas based on two destinations, given as coordinate pairs.
- title: The name of the enigma.
- subtitle: A short description.
- location: The location of the enigma.
- thumbnail_url: A URL for an image associated with the enigma.
- url: A link to more information about the enigma.

## Contributing
Contributions are welcome! If you have any suggestions, bug fixes, or improvements, feel free to open an issue or submit a pull request.

## Acknowledgements
Geoapify API: For providing geocoding services.
Sophos Websites: The development and design credit goes to Sophos Websites.
