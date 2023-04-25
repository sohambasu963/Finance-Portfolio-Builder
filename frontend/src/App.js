import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import StockWatchlist from './components/StockWatchlist';
import CustomPortfolioModal from './components/CustomPortfolioModal';
import { Button, Modal } from 'react-bootstrap';

import { fetchStockSuggestions, fetchStockData, fetchStockHistoricalData, fetchPortfolio } from './api';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [watchlist, setWatchlist] = useState([]);
  const [showPortfolioModal, setShowPortfolioModal] = useState(false);


  const handleSearch = async (searchTerm) => {
    // Fetch stock suggestions from the API
    var newSuggestions = await fetchStockSuggestions(searchTerm);
    return newSuggestions;
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

  const handleGenerateWatchlist = () => {
    // Add your logic to generate the watchlist here
  };  

  const handleClosePortfolioModal = () => {
    setShowPortfolioModal(false);
  };

  const handleShowPortfolioModal = async () => {
    try {
      const portfolioData = await fetchPortfolio(watchlist);
      // Pass the portfolioData to the CustomPortfolioModal component, e.g., using a state variable
      setShowPortfolioModal(true);
    } catch (error) {
      console.error('Error while generating the portfolio:', error);
    }
  };


  return (
    <div className="App">
      <div className='dashboard'>
        <h1>Stock Watchlist</h1>
        <p className='subheading'>Research stocks for your own custom portfolio</p>
        <SearchBar
        onSearch={handleSearch}
        onSuggestionSelect={handleSuggestionSelect}
        watchlist={watchlist}
        />
        <StockWatchlist stocks={watchlist} onRemoveStock={handleRemoveStock} />
        <Button
          className="generate-watchlist-btn"
          variant="success"
          size="lg"
          onClick={handleGenerateWatchlist}
        >
          Generate Watchlist
        </Button>
        <Button
          className="generate-portfolio-btn"
          variant="success"
          size="lg"
          onClick={handleShowPortfolioModal}
        >
          Generate Portfolio
        </Button>
        <CustomPortfolioModal
          show={showPortfolioModal}
          onHide={handleClosePortfolioModal}
        />
      </div>
    </div>
  );
}
// Symbol, Company Name, Price, Currency, Shares, Book Value (CAD), Book Value (Local)
export default App;
