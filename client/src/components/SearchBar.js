import React, { useState, useRef, useEffect } from 'react';
import { Form, InputGroup, Dropdown } from 'react-bootstrap';
import { Search } from 'react-bootstrap-icons';

const SearchBar = ({ onSearch, onSuggestionSelect, watchlist }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const searchBarRef = useRef(null);

  const handleSearch = async (e) => {
    const term = e.target.value;
    setSearchTerm(term);
    
    if (term.trim() === '') {
      setSuggestions([]);
    } else {
      const newSuggestions = await onSearch(term);
      // console.log(newSuggestions)
      setSuggestions(newSuggestions || []);
    }
  };

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchBarRef.current && !searchBarRef.current.contains(event.target)) {
        setSearchTerm('');
        setSuggestions([]);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div ref={searchBarRef}>
      <Form onSubmit={(e) => e.preventDefault()}>
        <InputGroup size="lg" style={{ width: "50rem" }}>
          <Form.Control
            type="text"
            placeholder="Search for stocks..."
            value={searchTerm}
            onChange={handleSearch}
          />
          <InputGroup.Text>
            <Search />
          </InputGroup.Text>
        </InputGroup>
        {suggestions.length > 0 && (
          <Dropdown.Menu show>
            {suggestions.map((suggestion, index) => (
              <Dropdown.Item 
                style={{ width: "50rem" }}
                key={index}
                onClick={async () => {
                  await onSuggestionSelect(suggestion);
                  // setSuggestions([]);
                }}
              >
                <div className="d-flex justify-content-between align-items-center">
                  <div>
                    <strong>{suggestion.symbol}</strong> - {suggestion.name}
                    <br />
                    <small>
                      {suggestion.currency}
                    </small>
                  </div>
                  {watchlist.some((stock) => stock.symbol === suggestion.symbol) ? (
                    <i className="bi bi-check-circle" style={{ color: "green", fontSize: "1.5rem" }}></i>
                  ) : (
                    <i className="bi bi-plus-circle" style={{ color: "green", fontSize: "1.5rem" }}></i>
                  )}
                </div>
              </Dropdown.Item>
            ))}
          </Dropdown.Menu>
        )}
      </Form>
    </div>
  );
};

export default SearchBar;