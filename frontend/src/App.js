import logo from './logo.svg';
import './App.css';
import SearchBar from './components/SearchBar';
import { useState } from 'react';

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleSearch = (searchTerm) => {
    return ['AAPL', 'GOOGL', 'MSFT'];
  };

  const handleSuggestionSelect = (suggestion) => {
    setSearchTerm(suggestion);
    // Handle the suggestion selection, e.g., fetch stock data
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
      </div>
    </div>
  );
}

export default App;
