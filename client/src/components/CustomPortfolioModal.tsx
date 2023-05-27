import React from 'react';
import { Button, Modal } from 'react-bootstrap';

interface CustomPortfolioModalProps {
  show: boolean;
  onHide: () => void;
  portfolio: any;
}

const CustomPortfolioModal = ({ show, onHide, portfolio }: CustomPortfolioModalProps) => {

  function formatNumber(num: number) {
    return new Intl.NumberFormat('en-CA').format(num);
  }

  return (
    <Modal show={show} onHide={onHide} size="xl">
      <Modal.Header closeButton>
        <div>
          <Modal.Title>Custom Portfolio</Modal.Title>
          <p>Generated a custom $100,000 portfolio based on your stock watchlist</p>
        </div>
      </Modal.Header>
      <Modal.Body>
        <table className="table table-striped table-dark">
          <thead>
            <tr>
              <th>Symbol</th>
              <th>Company Name</th>
              <th>Price</th>
              <th>Currency</th>
              <th>Shares</th>
              <th>Book Value (CAD)</th>
              <th>Book Value (Local)</th>
            </tr>
          </thead>
          <tbody>
            {portfolio.map((stock: any) => (
              <tr key={stock.symbol}>
                  <td>{stock.symbol}</td>
                  <td>{stock.name}</td>
                  <td>{stock.price}</td>
                  <td>{stock.currency}</td>
                  <td>{stock.shares}</td>
                  <td>{formatNumber(stock.bookValueCAD)}</td>
                  <td>{formatNumber(stock.bookValueLocal)}</td>
                </tr>
            ))}
          </tbody>
        </table>
      </Modal.Body>
      <Modal.Footer>
        <Button variant="secondary" onClick={onHide}>
          Close
        </Button>
      </Modal.Footer>
    </Modal>
  );
};

export default CustomPortfolioModal;
