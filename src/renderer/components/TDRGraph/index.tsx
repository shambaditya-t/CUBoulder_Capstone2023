import React from 'react';
import { xTestM, yTestOhm } from 'renderer/test_data';
import UplotReact from 'uplot-react';
import 'uplot/dist/uPlot.min.css';

export default function TDRGraph({}) {
  const yLow = yTestOhm.map((_) => 30);
  const yHigh = yTestOhm.map((_) => 70);
  const data = [xTestM, yTestOhm, yLow, yHigh];
  // const data = [
  //   [0, 1, 2],
  //   [10, 20, 30],
  // ];

  return (
    <UplotReact
      options={{
        title: 'Impedance vs. Distance',
        id: 'tdr-graph',
        width: 800,
        height: 600,
        series: [
          {
            label: 'x',
          },
          {
            show: true,
            label: 'Measured Impedance',
            stroke: 'red',
          },
          {
            label: "Low",
            fill: "rgba(0, 255, 0, 0.2)",
            band: true,
          },
          {
            label: "High",
            fill: "rgba(255, 0, 0, 0.2)",
            band: true,
          },
        ],
        scales: {
          x: {
            time: false,
          },
        },
      }}
      data={data}
    />
  );

  // const SVGRef = useRef(null);

  // return (
  //   <div ref={SVGRef} />
  // );
}
