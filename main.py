from flask import Flask, jsonify, render_template
import random
import string
import requests

app = Flask(__name__)

def generate_hwid(length=16):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def generate_fluxus_hwid():
    # Generate 64-character HWID like the example
    return generate_hwid(64)

@app.route('/api/trigon', methods=['GET'])
def generate_trigon():
    hwid = generate_hwid()
    link = f"https://trigonevo.fun/whitelist/?HWID={hwid}"
    return jsonify({"link": link})

@app.route('/api/fluxus', methods=['GET'])
def generate_fluxus():
    hwid = generate_fluxus_hwid()
    link = f"https://flux.li/android/external/start.php?HWID={hwid}"
    return jsonify({"link": link})

@app.route('/api/rerollfruit', methods=['GET'])
def reroll_fruit():
    fruits = ["Rocket", "Spike", "Chop", "Spring", "Bomb", "Smoke", "Spin", "Flame", "Falcon", "Ice", "Sand", "Dark", "Diamond", "Light", "Rubber", "Barrier", "Magma", "Quake", "Buddha", "Love", "Spider", "Phoenix", "Portal", "Rumble", "Pain", "Gravity", "Dough", "Shadow", "Venom", "Control", "Spirit", "Dragon", "Leopard"]
    fruit = random.choice(fruits)
    chance = f"1 in {random.randint(2, 10)}"
    return jsonify({"fruit": fruit, "chance": chance})

@app.route('/api/fakeip', methods=['GET'])
def generate_fake_ip():
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
    return jsonify({"fake_ip": ip})

@app.route('/api/password', methods=['GET'])
def generate_password():
    length = random.randint(8, 16)
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))
    strength = random.choice(["Weak", "Medium", "Strong", "Very Strong"])
    return jsonify({"password": password, "length": length, "strength": strength})

@app.route('/api/color', methods=['GET'])
def generate_color():
    hex_color = f"#{random.randint(0, 16777215):06x}"
    rgb = {
        "r": random.randint(0, 255),
        "g": random.randint(0, 255),
        "b": random.randint(0, 255)
    }
    return jsonify({"hex": hex_color, "rgb": rgb})

@app.route('/api/nitro', methods=['GET'])
def generate_nitro_code():
    # Generate fake Discord Nitro code (16 characters)
    chars = string.ascii_letters + string.digits
    code = ''.join(random.choice(chars) for _ in range(16))
    full_link = f"https://discord.gift/{code}"
    return jsonify({
        "code": code,
        "link": full_link,
        "type": "Discord Nitro",
        "status": "fake"
    })

@app.route('/api/github/<username>', methods=['GET'])
def get_github_user(username):
    try:
        response = requests.get(f"https://api.github.com/users/{username}")
        if response.status_code == 404:
            return jsonify({"error": "User not found"}), 404
        elif response.status_code != 200:
            return jsonify({"error": "GitHub API error"}), response.status_code

        user_data = response.json()
        return jsonify({
            "username": user_data.get("login"),
            "name": user_data.get("name"),
            "avatar_url": user_data.get("avatar_url"),
            "bio": user_data.get("bio"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "following": user_data.get("following"),
            "created_at": user_data.get("created_at"),
            "location": user_data.get("location"),
            "blog": user_data.get("blog"),
            "company": user_data.get("company")
        })
    except requests.RequestException:
        return jsonify({"error": "Failed to connect to GitHub API"}), 500

@app.route('/api/meme', methods=['GET'])
def get_meme():
    try:
        response = requests.get("https://meme-api.com/gimme")
        if response.status_code == 200:
            meme_data = response.json()
            return jsonify({
                "title": meme_data.get("title"),
                "url": meme_data.get("url"),
                "subreddit": meme_data.get("subreddit"),
                "author": meme_data.get("author"),
                "ups": meme_data.get("ups"),
                "nsfw": meme_data.get("nsfw"),
                "spoiler": meme_data.get("spoiler"),
                "postLink": meme_data.get("postLink")
            })
        else:
            return jsonify({"error": "Failed to fetch meme"}), response.status_code
    except requests.RequestException as e:
        return jsonify({"error": f"Request failed: {str(e)}"}), 500

@app.route('/api/pokemon', methods=['GET'])
def get_pokemon():
    try:
        from flask import request
        pokemon_name = request.args.get('name')

        if not pokemon_name:
            return jsonify({"error": "Pokemon name parameter is required"}), 400

        # Fetch Pokemon data from PokeAPI
        response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}")

        if response.status_code == 404:
            return jsonify({"error": "Pokemon not found"}), 404
        elif response.status_code != 200:
            return jsonify({"error": "PokeAPI error"}), response.status_code

        pokemon_data = response.json()

        # Extract abilities
        abilities = [ability['ability']['name'] for ability in pokemon_data['abilities']]

        # Extract stats
        stats = {}
        for stat in pokemon_data['stats']:
            stat_name = stat['stat']['name']
            stats[stat_name] = stat['base_stat']

        # Extract types
        types = [type_info['type']['name'] for type_info in pokemon_data['types']]

        return jsonify({
            "abilities": abilities,
            "id": pokemon_data['id'],
            "name": pokemon_data['name'],
            "stats": stats,
            "types": types
        })

    except requests.RequestException as e:
        return jsonify({"error": f"Failed to connect to PokeAPI: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Failed to fetch Pokemon data: {str(e)}"}), 500

# Simple URL storage for demonstration
url_storage = {}

@app.route('/api/shorten', methods=['GET', 'POST'])
def shorten_url():
    try:
        from flask import request

        # Handle GET request with query parameters
        if request.method == 'GET':
            original_url = request.args.get('url')
            if not original_url:
                return jsonify({"error": "URL parameter is required"}), 400
        # Handle POST request with JSON body
        else:
            data = request.get_json()
            if not data or 'url' not in data:
                return jsonify({"error": "URL is required"}), 400
            original_url = data['url']

        # Validate URL format
        if not original_url.startswith(('http://', 'https://')):
            return jsonify({"error": "URL must start with http:// or https://"}), 400

        # Generate short code
        short_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(8))

        # Store URL mapping
        url_storage[short_code] = original_url

        # Get the base URL (you might want to use your actual domain)
        base_url = request.host_url.rstrip('/')
        short_url = f"{base_url}/s/{short_code}"

        return jsonify({
            "original_url": original_url,
            "short_url": short_url,
            "short_code": short_code,
            "created_at": "now"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to shorten URL: {str(e)}"}), 500

@app.route('/s/<short_code>', methods=['GET'])
def redirect_url(short_code):
    from flask import redirect
    if short_code in url_storage:
        return redirect(url_storage[short_code])
    else:
        return jsonify({"error": "Short URL not found"}), 404

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/api', methods=['GET'])
def list_endpoints():
    endpoints = {
        "/api/trigon": "Generate Trigon whitelist link",
        "/api/fluxus": "Generate Fluxus link",
        "/api/rerollfruit": "Get random Blox Fruits reroll chance",
        "/api/fakeip": "Generates a random fake IP address",
        "/api/password": "Generate secure random passwords",
        "/api/color": "Generate random colors",
        "/api/nitro": "Generate fake Discord Nitro codes",
        "/api/github/<username>": "Get GitHub user information",
        "/api/meme": "Get random memes from Reddit",
        "/api/pokemon?name=": "Get Pokemon information",
        "/api/shorten?url=": "Shorten long URLs (GET with ?url= or POST request)",
    }
    return jsonify(endpoints)

if __name__ == "__main__":
    app.run(host='0.0.0.0', 
            port=5000)
