import { useEffect, useLayoutEffect, useRef, useState } from 'react';
import test_coupon from '../../../../assets/img/test_coupon.png';
// import './CouponCanvas.css'

function CouponCanvas() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [l, setL] = useState(0);

  // useEffect(() => {
  //   setTimeout(() => setL(l + 0.1), 1000);
  // }, [l]);

  useLayoutEffect(() => {
    // Initialize canvas element
    const { current } = canvasRef;
    if (current === null) return;
    const ctx = current.getContext('2d');
    if (ctx === null) return;

    // Create image and display on canvas
    // const couponImg = <img src={test_coupon} alt="coupon" />;
    const couponImg = new Image();
    couponImg.src = test_coupon;
    // ctx.fillStyle = 'rgb(200, 0, 0)';
    // ctx.fillRect(10, 10, 50, 50);

    // ctx.fillStyle = 'rgba(0, 0, 200, 0.5)';
    // ctx.fillRect(30, 30, 50, 50);

    // const img = ctx.getImageData(0, 0, current.width, current.height);
    // const { data } = img;
    // const X_CENTER = current.width / 2;
    // const Y_CENTER = current.height / 2;
    // const MAX_RADIUS = Math.max(current.width, current.height);
    // for (let i = 0; i < current.width; i += 1) {
    //   for (let j = 0; j < current.height; j += 1) {
    //     // Center relative
    //     const x = i - X_CENTER;
    //     const y = j - Y_CENTER;
    //     // Convert to polar coords
    //     const theta =
    //       // Math.atan(y / x + l) + (y <= Y_CENTER ? Math.PI : Math.PI / 2);
    //       Math.atan(y / x + l);
    //     const A = Math.sqrt(x ** 2 + y ** 2);
    //     ctx.fillStyle = `rgb(${(255 * theta) / Math.PI / 2}, ${
    //       (255 * A) / MAX_RADIUS
    //     }, 0)`;
    //     data[(j * current.width + i) * 4 + 0] = (255 * theta) / Math.PI;
    //     data[(j * current.width + i) * 4 + 1] = (255 * A) / MAX_RADIUS;
    //     data[(j * current.width + i) * 4 + 2] = 255;
    //     data[(j * current.width + i) * 4 + 3] = 255;
    //   }
    // }
    // ctx.putImageData(img, 0, 0);
    ctx.fillStyle = '#aaaaaa';
    couponImg.addEventListener('load', () => ctx.drawImage(couponImg, 0, 0));
    ctx.fillRect(10, 10, 40, 40);
  });

  return (
    <div className="CouponCanvas">
      {/* <canvas ref={canvasRef} width="480" height="270" /> */}
      <canvas ref={canvasRef} width="960" height="540" />
    </div>
  );
}

export default CouponCanvas;
