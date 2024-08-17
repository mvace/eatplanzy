
# EATPLANZY

This Django project is a website that showcases recipes sourced from the BBC dataset. It serves as a platform for users to explore and share their favorite recipes. As a part of my learning journey, I've incorporated features such as user authentication, profile management, recipe creation, liking, and commenting. Users can also connect with each other through messaging.

The app was build with a goal to practice Python, Django and Object Oriented Programming. The main focus was on the backend part. I realize that the code can be cleaner and more efficient but I am still a beginner and I build these projects to improve and get better.




## Key Features
- Recipe Showcase:

    Every user has access to a diverse collection of recipes sourced from the BBC dataset.

- User Authentication:

    Users can create accounts to unlock personalized features and interactions.

- Profile Management:

    Once registered, users can customize their profiles, providing a glimpse into their culinary preferences and expertise.

- Recipe Creation:

    Account holders have the ability to add their own recipes, contributing to the growing community of food enthusiasts.

- Interactivity:

    Users can engage with recipes by liking, commenting, and adding them to their favorites.

- Social Connection:

    Connect with other users through messaging, creating a network of like-minded individuals passionate about food.

- Recipe Editing:

    Recipe creators can easily edit and update their recipes to share new insights or improvements.

- API Access:

    The platform provides a RESTful API, allowing users to interact programmatically with the recipes. Users can retrieve the list of all recipes, view detailed information about a specific recipe, and manage (create, update, delete) their own recipes.


    

## How It Works
- Recipe Exploration:

    All users can freely explore the extensive collection of recipes available on EatPlanzy.

- Account Creation:

    Users can create accounts to unlock additional features and personalize their experience.

- Recipe Interaction:

    Account holders can like, comment, and add recipes to their favorites, fostering a sense of community engagement.

- Recipe Contribution:

    Registered users have the privilege to contribute by adding their own recipes to the platform.

- Profile Enhancement:

    Users can update their profiles to showcase their culinary expertise and preferences.

- Social Connectivity:

    Messaging functionality allows users to connect with each other, share tips, and build a network within the community.

- API Usage:

    Developers can access the EatPlanzy API to programmatically interact with recipes. The API supports operations like fetching all recipes, getting details of a specific recipe, and managing (create, update, delete) recipes that they own.


## Installation

To run the project locally, follow these steps:

#### 1. Clone the repository:


```bash
git clone https://github.com/mvace/eatplanzy
```

#### 2. Navigate to the project directory:

```bash
cd eatplanzy
```

#### 3. Create and Activate a Virtual Environment

```bash
python -m venv venv
```
#### On Windows:
```bash
.\venv\Scripts\activate
```

#### On macOS and Linux:
```bash
source venv/bin/activate
```

#### 4. Install dependencies:

```bash
pip install -r requirements.txt
```

#### 5. Run the Development Server

```bash
python manage.py runserver
```

#### 6. Access the Application
Visit http://localhost:8000 in your web browser to access the app.

