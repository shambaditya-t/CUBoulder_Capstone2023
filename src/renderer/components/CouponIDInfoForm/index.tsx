import React, { useContext, useRef } from 'react';
import { Button, Form } from 'react-bootstrap';
import { CouponContext } from 'renderer/classes/CouponContext';
import RegexFormControl from '../RegexFormControl';

function CouponIDInfoForm() {
  const ctx = useContext(CouponContext);
  if (ctx === undefined) return null;
  const { couponTemplater } = ctx;
  const formRef = useRef<HTMLFormElement>(null);
  const handleFormSubmit = () => {
    if (formRef.current === undefined) return;
    // Pull values from the form ref
    const { Serial, DateCode, Job, Customer } = formRef.current;
    console.log(Serial.value, DateCode.value, Job.value, Customer.value);
    // couponTemplater.addSingleMeasurement()
  };

  return (
    <Form>
      <Form.Group>
        <Form.Label>Serial #</Form.Label>
        <RegexFormControl name="Serial" regex={/^([0-9]*)$/} />
      </Form.Group>
      <Form.Group>
        <Form.Label>Date Code</Form.Label>
        <RegexFormControl name="DateCode" regex={/^([0-9]{4})$/} />
      </Form.Group>
      <Form.Group>
        <Form.Label>Job #</Form.Label>
        <RegexFormControl name="Job" regex={/^([0-9]{10})$/} />
      </Form.Group>
      <Form.Group>
        <Form.Label>Customer</Form.Label>
        <RegexFormControl name="Customer" regex={/^([A-Za-z0-9 ]*)$/} />
      </Form.Group>
      <Button onClick={handleFormSubmit} variant="primary">
        Submit
      </Button>
    </Form>
  );
}

export default CouponIDInfoForm;
