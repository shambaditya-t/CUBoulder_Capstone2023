import React from 'react';
import CouponCanvas from 'renderer/components/CouponCanvas';
import MeasurementView from 'renderer/components/MeasurementView';
import TDRGraph from 'renderer/components/TDRGraph';
import FooterBar from '../components/FooterBar';

function PageTest() {
  return (
    <div className="page container-fluid">
      <CouponCanvas />
      <MeasurementView />
      <TDRGraph />
      <FooterBar />
    </div>
  );
}

export default PageTest;
