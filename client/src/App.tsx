import React, { useState } from 'react';
import './App.css';
import SearchBar from './components/SearchBar';
import StockWatchlist from './components/StockWatchlist';
import CustomPortfolioModal from './components/CustomPortfolioModal';
import { Button } from 'react-bootstrap';
import { fetchStockSuggestions, fetchStockData, fetchPortfolio, fetchWatchlist } from './api';

type SuggestionData = {
  symbol: string;
  name: string;
  currency: string;
};

function App() {
  const [watchlist, setWatchlist] = useState<any>([]);
  const [showPortfolioModal, setShowPortfolioModal] = useState(false);
  const [portfolio, setPortfolio] = useState([]);


  const handleSearch = async (searchTerm: string) => {
    // Fetch stock suggestions from the API
    const newSuggestions = await fetchStockSuggestions(searchTerm);
    return newSuggestions;
  };

  const handleSuggestionSelect = async (suggestion: SuggestionData) => {
    if (watchlist.some((stock: any) => stock.symbol === suggestion.symbol)) {
      return;
    }
    const stockData = await fetchStockData(suggestion);
    setWatchlist([...watchlist, stockData]);
  };

  const handleRemoveStock = (symbol: string) => {
    setWatchlist(watchlist.filter((stock: any) => stock.symbol !== symbol));
  };

  const handleGenerateWatchlist = async () => {
    const watchlistStocks = await fetchWatchlist();
    console.log(watchlistStocks);
  };  

  const handleClosePortfolioModal = () => {
    setShowPortfolioModal(false);
  };

  const handleShowPortfolioModal = async () => {
    try {
      const portfolioData = await fetchPortfolio(watchlist);
      setPortfolio(portfolioData);
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
          portfolio={portfolio}
        />
      </div>
    </div>
  );
}
// Symbol, Company Name, Price, Currency, Shares, Book Value (CAD), Book Value (Local)
export default App;
