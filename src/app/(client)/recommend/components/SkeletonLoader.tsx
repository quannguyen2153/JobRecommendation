import { Card } from '@nextui-org/react';
import React from 'react';
import Skeleton from 'react-loading-skeleton';
import 'react-loading-skeleton/dist/skeleton.css';

const SkeletonLoader = () => {
  return (
    <div className="w-[50%] h-full">
      <div className="w-full h-full rounded-2xl flex flex-col">
        {Array.from({ length: 4 }).map((_, index) => (
          <div
            id={index.toString()}
            className="w-full h-32 flex flex-col items-center rounded-2xl my-4 border-3 shadow-sm"
          >
            <div className="w-full h-full p-3 flex flex-row items-center justify-between">
              <Skeleton width={75} height={75} baseColor="#acacac" />
              <div className="w-[85%] h-full p-3 flex flex-col items-center justify-between">
                <Skeleton containerClassName="w-full" baseColor="#acacac" />
                <Skeleton containerClassName="w-full" baseColor="#acacac" />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default SkeletonLoader;
