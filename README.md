# Stock-Analyzer

A React frontend client to handle ticker search, stock performance charts, and portfolio generation, paired with a Python Flask backend that queries data and uses optimization algorithms to generate portfolios and suggested stocks

Note: Currently in the process of converting the frontend client from Javascript to Typescript


Local Install Instructions:

1. In a directory of your choice, run the following command
```
git clone https://github.com/sohambasu963/Finance-Portfolio-Builder.git
```
2. Open this folder using Visual Studio Code or another editor of your choice

3. Get an API key for Alpha Vantage API from the following website:
   https://www.alphavantage.co/support/#api-key

Backend Setup:
*** Please complete these steps within the backend folder of the repository ***

1. Install all necessary python modules/libraries within the backend directory using the following command:
```
pip3 install module1 module2 ...
```
 
2. Create a .env.local file and add the following line to the file and replace the API key placeholder with your API key:
```
ALPHA_VANTAGE_API_KEY="your_api_key_here"
```

Frontend Setup:
*** Please complete these steps within the frontend folder of the repository ***

1. Install all necessary npm modules/dependencies within the frontend directory using the following command:
```
npm install module1 module2 ...
```
2. Create a .env.local file and add the following line ot the file and replace the API key placeholder with your API key:
```
REACT_ALPHA_VANTAGE_API_KEY="your_api_key_here"
```
3. Run the following command to launch the web app, it should open on port 3000:
```
npm start
```

