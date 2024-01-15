import { useState } from 'react';
import { Button } from 'react-bootstrap';
import { Play, Pause, SkipForward, SkipEnd } from 'react-bootstrap-icons';

function TestController() {
  const [isPaused, setIsPaused] = useState(false);
  return (
    <div className="TestController">
      {isPaused ? (
        <Button variant="danger" onClick={() => setIsPaused(false)}>
          <Pause />
        </Button>
      ) : (
        <Button variant="success" onClick={() => setIsPaused(true)}>
          <Play />
        </Button>
      )}
      <Button variant="secondary" size="sm" className="ms-1">
        <SkipForward />
      </Button>
      <Button variant="secondary" size="sm" className="ms-1">
        <SkipEnd />
      </Button>
    </div>
  );
}

export default TestController;
