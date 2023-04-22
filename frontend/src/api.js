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
  
  export { fetchStockSuggestions };
  