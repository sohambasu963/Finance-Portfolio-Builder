import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import StockWatchlist from './components/StockWatchlist';
import { fetchStockSuggestions, fetchStockData, fetchStockHistoricalData } from './api';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [watchlist, setWatchlist] = useState([]);

  const handleSearch = async (searchTerm) => {
    // Fetch stock suggestions from the API
    var newSuggestions = await fetchStockSuggestions(searchTerm);
    return newSuggestions;
    // return ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB', 'TSLA', 'NFLX', 'NVDA', 'PYPL', 'ADBE'];
  };

  const handleSuggestionSelect = async (suggestion) => {
    setSearchTerm(suggestion);
    // Handle the suggestion selection, e.g., fetch stock data
    // if suggestion not in watchlist
    if (watchlist.some((stock) => stock.symbol === suggestion.symbol)) {
      return;
    }
    const stockData = await fetchStockData(suggestion);
    setWatchlist([...watchlist, stockData]);
  };

  const handleRemoveStock = (symbol) => {
    setWatchlist(watchlist.filter((stock) => stock.symbol !== symbol));
  };

  return (
    <div className="App">
      <div className='dashboard'>
        <h1>Stock Watchlist</h1>
        <p>Research stocks for your own custom portfolio</p>
        <SearchBar
        onSearch={handleSearch}
        onSuggestionSelect={handleSuggestionSelect}
        watchlist={watchlist}
        />
        <StockWatchlist stocks={watchlist} onRemoveStock={handleRemoveStock}/>
      </div>
    </div>
  );
}

export default App;
