# ChefGPT
A Streamlit app that connects to Open AI's GPT-3 API to generate cooking recipes

## Installation

First, clone the repository and install the dependencies.

```bash
git clone https://github.com/eitangreenb/ChefGPT.git
cd ChefGPT
pip install -r requirements.txt
```

You will need to add your own firebase firestore-key json to the ChatGPT folder.<br>
Edit the `secrets.json` file with your own secret keys:
```bash
{
    "FIREBASE_JSON": "the path to your firestore-key json file",
    "OPENAI_KEY": "your own openai api key"
}
```

To run the app localy use the following command:
```bash
streamlit run .\app\Home.py
```

##  How to set up Firestore Database
Login with a google account to https://firebase.google.com/ and press Get started<br>
1. Create a project:<br>
![Step 1](https://media3.giphy.com/media/PTy6LOet4IT3kFsp5o/giphy.gif)

2. Create a Firestore Database:<br>
![Step 2](https://media0.giphy.com/media/h3E2lqsB3n6wJNg9ks/giphy.gif)

3. Download Firestore-key json for python applications:<br>
![Step 3](https://media4.giphy.com/media/npzDv3zQrS4MZl1OfU/giphy.gif)

## How to set up Open AI api key
Login with your account to https://openai.com/api/<br>
1. Go to Personal > View API keys:<br>
![Step 1](https://i.ibb.co/7g47BB8/Open-AI-key-1.png)

2. Generate a new key:<br>
![Step 2](https://i.ibb.co/ZXzCnk0/Open-AI-key.png)






