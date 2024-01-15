import React, { useContext } from 'react';
import { CouponContext } from 'renderer/classes/CouponContext';

function MeasurementView() {
  const ctx = useContext(CouponContext);
  if (ctx === undefined) return;
  const { couponTemplater } = ctx;
  // couponTemplater.addSingleMeasurement('test', 50, 10, 10, true);
  return (
    <div>
      {couponTemplater.template.map((v) => (
        <li>{`${v.measure_index} ${v.identifer}`}</li>
      ))}
    </div>
  );
}

export default MeasurementView;
