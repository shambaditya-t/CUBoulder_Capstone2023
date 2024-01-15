enum DetectionStatus {
  DETECTION_STATUS_NONE      = 'DETECTION_STATUS_NONE',
  DETECTION_STATUS_PARTIAL   = 'DETECTION_STATUS_PARTIAL',
  DETECTION_STATUS_FULL      = 'DETECTION_STATUS_FULL',
  DETECTION_STATUS_CONFIRMED = 'DETECTION_STATUS_CONFIRMED',
}

enum TestStatus {
  TEST_STATUS_NONE        = 'TEST_STATUS_NONE',
  TEST_STATUS_PARTIAL     = 'TEST_STATUS_PARTIAL',
  TEST_STATUS_PAUSED      = 'TEST_STATUS_PAUSED',
  TEST_STATUS_FULL        = 'TEST_STATUS_FULL',
  TEST_STATUS_SKIPPED     = 'TEST_STATUS_SKIPPED',
  TEST_STATUS_DONE_FAILED = 'TEST_STATUS_DONE_FAILED',
  TEST_STATUS_DONE_PASSED = 'TEST_STATUS_DONE_PASSED',
}

enum PadType {
  PAD_TYPE_ANODE   = 'ANODE',
  PAD_TYPE_CATHODE = 'CATHODE',
}

type PadDetection = {
  type: PadType;
  x   : number;
  y   : number;
};

enum TextType {
  TEXT_TYPE_UNKOWN,
  TEXT_TYPE_MO,
  TEXT_TYPE_SN,
  TEXT_TYPE_CUST,
  TEXT_TYPE_REV,
}

type TextDetection = {
  type  : TextType;
  text  : string;
  x     : number;
  y     : number;
  width : number;
  height: number;
};

type CouponInfo = {
  uid   : string;
  status: {
    instructionsLoaded: boolean;
    mechanicallyLoaded: boolean;
    imaged            : boolean;
    detections        : DetectionStatus;
    test              : TestStatus;
  };
  instructions: unknown;
  imagePath   : string;
  detections  : {
    text: Array<TextDetection>;
    pads: Array<PadDetection>;
  };
  test: unknown;
};

type TestInfo = {
  status : TestStatus;
  coupons: Array<CouponInfo>;
};

export {
  DetectionStatus,
  TestStatus,
  PadType,
  PadDetection,
  TextType,
  TextDetection,
  CouponInfo,
  TestInfo,
};
