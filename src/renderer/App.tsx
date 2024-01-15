import { MemoryRouter as Router, Routes, Route, Link } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import { Button } from 'react-bootstrap';
import PageTest from './pages/PageTest';
import { CouponContextProvider } from './classes/CouponContext';
// import PageLoad from './pages/PageLoad';
import PageSettings from './pages/PageSettings';

const MainMenu = () => {
  return (
    <div className="PageRoot w-100 h-100">
      <div className="MainMenu">
        {/* <Link to="Test">
          <Button className="MainMenuItem">Align / Calibrate</Button>
        </Link> */}
        {/* <Link to="Load">
          <Button className="MainMenuItem">Load Coupons</Button>
        </Link> */}
        <Link to="Test">
          <Button className="MainMenuItem">Manual Test</Button>
        </Link>
        <Link to="Settings">
          <Button className="MainMenuItem">Settings</Button>
        </Link>
      </div>
    </div>
  );
};

export default function App() {
  return (
    <CouponContextProvider>
      <Router>
        <Routes>
          <Route path="/" element={<MainMenu />} />
          <Route path="/Test" element={<PageTest />} />
          <Route path="/Load" element={<PageSettings />} />
        </Routes>
      </Router>
    </CouponContextProvider>
  );
}
