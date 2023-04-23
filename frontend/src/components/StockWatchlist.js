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
          <th>Percentage Change</th>
          <th>Dividend Yield</th>
          <th>P/E Ratio</th>
          <th>Beta</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {stocks.map((stock) => (
            <tr key={stock.Symbol}>
                <td>{stock.Symbol}</td>
                <td>{stock.Name}</td>
                <td>{stock.Price}</td>
                <td>{stock.Currency}</td>
                <td>{stock.PercentChange}</td>
                <td>{stock.DividendYield}</td>
                <td>{stock.PERatio}</td>
                <td>{stock.Beta}</td>
                <td>
                    <Button
                    variant="danger"
                    size="sm"
                    onClick={() => onRemoveStock(stock.Symbol)}
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
