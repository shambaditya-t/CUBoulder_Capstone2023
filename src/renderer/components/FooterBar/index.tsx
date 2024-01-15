import { useState } from 'react';
import { Button } from 'react-bootstrap';
import TestController from '../TestController';
import './FooterBar.css';

function FooterBar() {
  const [status, setStatus] = useState('Feeding Next Coupon');
  return (
    <footer className="Footer">
      <div className="FooterItem" style={{ width: '250px' }}>
        <div className="TestStatusText">{status}</div>
      </div>
      <div className="FooterItem">
        <TestController />
      </div>
      <div className="FooterItem" style={{ width: '250px' }}>
        <Button variant="danger" size="sm" style={{ float: 'right' }}>
          Stop
        </Button>
      </div>
    </footer>
  );
}

export default FooterBar;
