import { CircularProgress, Progress } from '@nextui-org/react';
import React from 'react';

const Rating = ({
  data,
}: {
  data: {
    rating: number;
    criteria1: number;
    criteria2: number;
    criteria3: number;
  };
}) => {
  let evaluation;
  let color;

  if (data.rating < 50) {
    evaluation = 'Your CV needs improvement!';
    color = 'text-red-500';
  } else if (data.rating >= 50 && data.rating <= 70) {
    evaluation = 'Your CV is fine, but it can be better!';
    color = 'text-yellow-500';
  } else {
    evaluation = 'Your CV is great!';
    color = 'text-green-500';
  }

  return (
    <div className="w-full h-fit flex flex-col justify-center items-center text-black gap-5">
      <span className={`text-2xl font-bold ${color}`}>{evaluation}</span>
      <div className="w-full h-fit flex flex-row justify-center items-center text-black gap-4">
        <div className="w-fit">
          <CircularProgress
            classNames={{
              svg: 'w-36 h-36 drop-shadow-md',

              track: 'stroke-gray-300',
              value: 'text-3xl font-semibold text-black',
            }}
            value={Math.round(data.rating)}
            color="primary"
            showValueLabel={true}
          />
        </div>

        <div className="w-[30%] h-full flex flex-col  items-center justify-center gap-2">
          <Progress
            label="Criteria 1"
            size="md"
            value={data.criteria1}
            color="primary"
            showValueLabel={true}
            className="max-w-md"
          />
          <Progress
            label="Criteria 2"
            size="md"
            value={data.criteria3}
            color="primary"
            showValueLabel={true}
            className="max-w-md"
          />
          <Progress
            label="Criteria 2"
            size="md"
            value={data.criteria3}
            color="primary"
            showValueLabel={true}
            className="max-w-md"
          />
        </div>
      </div>
    </div>
  );
};

export default Rating;
