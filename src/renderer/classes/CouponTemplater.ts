interface CouponMeasurementResults {
  avg_ohms: number;
  std_ohms: number;
  min_ohms: number;
  max_ohms: number;
}

interface CouponMeasurement {
  measure_index: number;
  identifer: string;
  ohms_nominal: number;
  tolerance_plus: number;
  tolerance_minus: number;
  differential: boolean;
  results?: CouponMeasurementResults;
}

class CouponTemplater {
  updateHook: () => void;

  template: Array<CouponMeasurement>;

  constructor(updateHook: () => void) {
    this.updateHook = updateHook;
    this.template = [];
  }

  addSingleMeasurement(
    identifer: string,
    ohms_nominal: number,
    tolerance_plus: number,
    tolerance_minus: number,
    differential: boolean
  ) {
    const newMeas: CouponMeasurement = {
      measure_index: this.template.length,
      identifer,
      ohms_nominal,
      tolerance_plus,
      tolerance_minus,
      differential,
    };
    this.template.push(newMeas);
    this.updateHook();
  }
}

export default CouponTemplater;
