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

##  How to set up Firestore Database and Open AI api key
Login with a google account to https://firebase.google.com/ and press Get started<br>
1. Create a project:
![Step 1](https://media3.giphy.com/media/PTy6LOet4IT3kFsp5o/giphy.gif)

2. Create a Firestore Database:
![Step 2](https://media0.giphy.com/media/h3E2lqsB3n6wJNg9ks/giphy.gif)

3. Download Firestore-key json for python applications:
![Step 3](https://media4.giphy.com/media/npzDv3zQrS4MZl1OfU/giphy.gif)




