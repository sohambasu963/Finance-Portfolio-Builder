import React, { useEffect, useRef } from 'react';
import { Modal } from 'react-bootstrap';
import ChartJS from 'chart.js/auto';
import { Chart, TimeScale } from 'chart.js';
import 'chartjs-adapter-date-fns';
import { enUS } from 'date-fns/locale'; 

ChartJS.register(TimeScale);

interface StockDetailsModalProps {
  show: boolean;
  onHide: () => void;
  historicalData: any;
}

const StockDetailsModal = ({ show, onHide, historicalData }: StockDetailsModalProps) => {
  const chartRef = useRef(null);
  const chartInstance = useRef<Chart | null>(null);

  useEffect(() => {
    if (chartRef && chartRef.current) {
      if (chartInstance.current) {
        chartInstance.current.destroy();
      }

      const chartConfig: any = {
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
            plugins: {
                legend: {
                    display: false,
                },
                tooltip: {
                    callbacks: {
                        title: function(tooltipItem: any) {
                            const label = tooltipItem[0].label.split(',');
                            return label[0] + ',' + label[1];
                        }
                    }
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
