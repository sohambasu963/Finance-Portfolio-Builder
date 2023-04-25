import React from 'react';
import { Button, Modal } from 'react-bootstrap';

const CustomPortfolioModal = ({ show, onHide }) => {
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
            {/* Add table rows with data here */}
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
