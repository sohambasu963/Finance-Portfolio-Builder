const fetchStockSuggestions = async (searchTerm) => {
    const apiKey = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;
    const API_URL = 'https://www.alphavantage.co/query';
    const FUNCTION = 'SYMBOL_SEARCH';
    
    const response = await fetch(
      `${API_URL}?function=${FUNCTION}&keywords=${searchTerm}&apikey=${apiKey}`
    );
    const data = await response.json();
  
    if (!data.bestMatches) {
      console.error('Invalid API response:', data);
      return [];
    }
  
    // Extract stock suggestions from the API response
    const suggestions = data.bestMatches
      .filter((item) => {
        const region = item['4. region'];
        // Filter for US and Canadian stocks
        return region === 'United States' || region === 'Canada';
      })
      .map((item) => item['1. symbol']);
  
    return suggestions;
  };

const fetchStockData = async (symbol) => {
    const apiKey = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;
    const API_URL = 'https://www.alphavantage.co/query';
    const QUOTE_FUNCTION = 'GLOBAL_QUOTE';
    const OVERVIEW_FUNCTION = 'OVERVIEW';

    const quoteResponse = await fetch(
        `${API_URL}?function=${QUOTE_FUNCTION}&symbol=${symbol}&apikey=${apiKey}`
    );
    const quoteData = await quoteResponse.json();

    const overviewResponse = await fetch(
        `${API_URL}?function=${OVERVIEW_FUNCTION}&symbol=${symbol}&apikey=${apiKey}`
    );
    const overviewData = await overviewResponse.json();

    const stockData = {
        "Symbol": overviewData["Symbol"],
        "Name": overviewData["Name"],
        "Price": quoteData["Global Quote"]["05. price"],
        "Currency": overviewData["Currency"],
        "PercentChange": quoteData["Global Quote"]["10. change percent"],
        "DividendYield": (Number(overviewData["DividendYield"]) * 100).toFixed(2).toString() + "%",
        "PERatio": overviewData["PERatio"],
        "Beta": overviewData["Beta"],
    }
    return stockData

}
  
  export { fetchStockSuggestions, fetchStockData };
  