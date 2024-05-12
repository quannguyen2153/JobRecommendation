import { Loader } from 'lucide-react';
import React from 'react';

function loading() {
  return (
    <div className="w-full h-full flex items-center justify center">
      <Loader />
    </div>
  );
}

export default loading;
