const fetchStockSuggestions = async (searchTerm: string) => {
    const apiKey = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;
    const API_URL = 'https://www.alphavantage.co/query';
    const FUNCTION = 'symbol_SEARCH';
  
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
      .filter((item: any) => {
        const currency = item['8. currency'];
        // Filter for US and Canadian stocks
        return currency === 'USD' || currency === 'CAD';
      })
      .map((item: any) => ({
        symbol: item['1. symbol'],
        name: item['2. name'],
        currency: item['8. currency']
      }));
  
    return suggestions;
  };
  

  const fetchStockData = async (suggestion: any) => {
    const apiKey = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;
    const API_URL = 'https://www.alphavantage.co/query';
    const QUOTE_FUNCTION = 'GLOBAL_QUOTE';
    const OVERVIEW_FUNCTION = 'OVERVIEW';
  
    const quoteResponse = await fetch(
      `${API_URL}?function=${QUOTE_FUNCTION}&symbol=${suggestion.symbol}&apikey=${apiKey}`
    );
    const quoteData = await quoteResponse.json();
  
    const overviewResponse = await fetch(
      `${API_URL}?function=${OVERVIEW_FUNCTION}&symbol=${suggestion.symbol.split('.')[0]}&apikey=${apiKey}`
    );
    const overviewData = await overviewResponse.json();

    const stockData = {
      "symbol": suggestion.symbol,
      "name": suggestion.name,
      "price": Number(quoteData["Global Quote"]["05. price"]).toFixed(2),
      "currency": suggestion.currency,
      "percentChange": Number(quoteData["Global Quote"]["10. change percent"].slice(0, -1)).toFixed(2),
      "dividendYield": overviewData["DividendYield"] ? (Number(overviewData["DividendYield"]) * 100).toFixed(2) : "N/A",
      "peRatio": overviewData["PERatio"] && overviewData["PERatio"] !== "None" ? Number(overviewData["PERatio"]).toFixed(2) : "N/A",
      "beta": overviewData["Beta"] ? Number(overviewData["Beta"]).toFixed(2) : "N/A",
    }
    return stockData
  }

  const fetchStockHistoricalData = async (symbol: string) => {
    const apiKey = process.env.REACT_APP_ALPHA_VANTAGE_API_KEY;
    const API_URL = 'https://www.alphavantage.co/query';
    const FUNCTION = 'TIME_SERIES_DAILY_ADJUSTED';
    const response = await fetch(
      `${API_URL}?function=${FUNCTION}&symbol=${symbol}&outputsize=compact&apikey=${apiKey}`
    );
    const data = await response.json();
  
    if (!data['Time Series (Daily)']) {
      console.error('Invalid API response:', data);
      return [];
    }

    const timeSeriesData = data['Time Series (Daily)'];

    const dates = Object.keys(timeSeriesData);
    const adjustedClosingPrices = dates.map((date) => parseFloat(timeSeriesData[date]['5. adjusted close']).toFixed(2));
    
    const historicalData = {
        "stock": data["Meta Data"]["2. Symbol"],
        "labels": dates,
        "data": adjustedClosingPrices
    }
  
    return historicalData;
  };
  
const fetchPortfolio = async (watchlist: any) => {
  const response = await fetch('http://127.0.0.1:5000/portfolio', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(watchlist),
  });

  if (!response.ok) {
    throw new Error('An error occurred while calculating the portfolio');
  }

  const data = await response.json();
  console.log(data)
  return data;
};

  
  export { fetchStockSuggestions, fetchStockData, fetchStockHistoricalData, fetchPortfolio};
  