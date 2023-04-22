import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import StockWatchlist from './components/StockWatchlist';
import { fetchStockSuggestions } from './api';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [watchlist, setWatchlist] = useState([]);

  const handleSearch = async (searchTerm) => {
    // Fetch stock suggestions from the API
    // var newSuggestions = await fetchStockSuggestions(searchTerm);
    // return newSuggestions;
    return ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB', 'TSLA', 'NFLX', 'NVDA', 'PYPL', 'ADBE'];
  };

  const handleSuggestionSelect = (suggestion) => {
    setSearchTerm(suggestion);
    // Handle the suggestion selection, e.g., fetch stock data
    // if suggestion not in watchlist
    if (!watchlist.some((stock) => stock.symbol === suggestion)) {
      const stockData = {
        symbol: suggestion,
        name: 'Example Company Name', // Replace with fetched company name
        currentPrice: 123.45, // Replace with fetched current price
        percentageChange: 1.23, // Replace with fetched open to close % change
        dividendYield: 2.34, // Replace with fetched dividend yield
      };
      watchlist.push(stockData);
      setWatchlist(watchlist);
    }
  };

  const handleRemoveStock = (symbol) => {
    console.log(symbol)
    setWatchlist(watchlist.filter((stock) => stock.symbol !== symbol));
  };

  return (
    <div className="App">
      <div className='dashboard'>
        <h1>Stock Watchlist</h1>
        <p className='subheading'>Search for stocks below to add them to your watchlist</p>
        <SearchBar
        onSearch={handleSearch}
        onSuggestionSelect={handleSuggestionSelect}
        />
        <StockWatchlist stocks={watchlist} onRemoveStock={handleRemoveStock}/>
      </div>
    </div>
  );
}

export default App;
