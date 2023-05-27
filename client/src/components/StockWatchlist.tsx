import React from 'react';
import { useState } from 'react';
import './StockWatchlist.css';
import { Button } from 'react-bootstrap';
import StockDetailsModal from './StockDetailsModal';
import { fetchStockHistoricalData } from '../api';

interface StockWatchlistProps {
    stocks: any;
    onRemoveStock: (symbol: string) => void;
  }

const StockWatchlist = ({ stocks, onRemoveStock }: StockWatchlistProps) => {

    const [showModal, setShowModal] = useState(false);
    const [historicalData, setHistoricalData] = useState({ labels: [], data: [] });

    const handleStockClick = async (symbol: string) => {
        const data: any = await fetchStockHistoricalData(symbol);
        setHistoricalData(data);
        setShowModal(true);
      };
      
    return (
        <>
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
                {stocks.map((stock: any) => (
                    <tr key={stock.symbol}>
                        <td>
                            <a href="#/" onClick={(e) => { e.preventDefault(); handleStockClick(stock.symbol); }}>
                                {stock.symbol}
                            </a>
                        </td>
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
            <StockDetailsModal
            show={showModal}
            onHide={() => setShowModal(false)}
            historicalData={historicalData}
            />
        </>
    );
};

export default StockWatchlist;
