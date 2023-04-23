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
          <th>Price</th>
          <th>Currency</th>
          <th>Change (%)</th>
          <th>Dividend Yield (%)</th>
          <th>P/E Ratio</th>
          <th>Beta</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
            <tr key={stock.symbol}>
                <td>{stock.symbol}</td>
                <td>{stock.name}</td>
                <td>{stock.price}</td>
                <td>{stock.currency}</td>
                <td>{stock.percentChange}</td>
                <td>{stock.dividendYield}</td>
                <td>{stock.peRatio}</td>
                <td>{stock.beta}</td>
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
