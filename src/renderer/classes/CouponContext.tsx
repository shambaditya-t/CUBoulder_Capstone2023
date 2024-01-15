import React, { createContext, ReactNode } from 'react';
import CouponTemplater from './CouponTemplater';

type CouponContextType = {
  couponTemplater: CouponTemplater;
};

const CouponContext = createContext<CouponContextType | undefined>(undefined);

type Props = {
  children: ReactNode;
};

class CouponContextProvider extends React.Component<Props> {
  couponTemplater: CouponTemplater;

  constructor(props: Props) {
    super(props);
    this.state = {};
    this.couponTemplater = new CouponTemplater(() => this.updateSelf());
  }

  updateSelf() {
    this.setState({});
  }

  render() {
    const { children } = this.props;
    return (
      <CouponContext.Provider
        value={{
          couponTemplater: this.couponTemplater,
        }}
      >
        {children}
      </CouponContext.Provider>
    );
  }
}

export { CouponContextProvider, CouponContext };
