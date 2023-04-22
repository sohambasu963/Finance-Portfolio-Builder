import React from 'react';
import './StockWatchlist.css';
import { Button } from 'react-bootstrap';

const StockWatchlist = ({ stocks, onRemoveStock }) => {
  return (
    <table className="table table-dark table-striped stock-table">
      <thead>
        <tr>
          <th>Symbol</th>
          <th>Company Name</th>
          <th>Current Price</th>
          <th>Open to Close % Change</th>
          <th>Dividend Yield</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
          <tr key={stock.symbol}>
            <td>{stock.symbol}</td>
            <td>{stock.name}</td>
            <td>{stock.currentPrice}</td>
            <td>{stock.percentageChange.toFixed(2)}%</td>
            <td>{stock.dividendYield.toFixed(2)}%</td>
            <td>
              <Button
                variant="danger"
                size="sm"
                onClick={() => onRemoveStock(stock.symbol)}
              >
                -
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default StockWatchlist;
