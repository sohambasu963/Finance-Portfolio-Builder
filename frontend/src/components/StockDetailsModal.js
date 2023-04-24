import React, { useEffect, useRef } from 'react';
import { Modal } from 'react-bootstrap';
import ChartJS from 'chart.js/auto';
import { Chart, TimeScale } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { enUS } from 'date-fns/locale'; 

ChartJS.register(TimeScale);

const StockDetailsModal = ({ show, onHide, historicalData }) => {
  const chartRef = useRef(null);
  const chartInstance = useRef(null);

  useEffect(() => {
    if (chartRef && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const chartConfig = {
        type: 'line',
        data: {
          labels: historicalData.labels,
          datasets: [
            {
              label: 'Adjusted Close',
              data: historicalData.data,
              borderColor: 'rgba(75, 192, 192, 1)',
              tension: 0.1,
            },
          ],
        },
        options: {
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'month',
              },
              adapters: { 
                date: {
                  locale: enUS, 
                },
              }, 
            },
          },
        },
      };

      chartInstance.current = new Chart(chartRef.current, chartConfig);
    }

    return () => {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }
    };
  }, [show, historicalData]);

  return (
    <Modal show={show} onHide={onHide} size="lg" centered>
      <Modal.Header closeButton>
        <Modal.Title>{historicalData.stock} Historical Performance</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <canvas ref={chartRef} />
      </Modal.Body>
    </Modal>
  );
};

export default StockDetailsModal;
