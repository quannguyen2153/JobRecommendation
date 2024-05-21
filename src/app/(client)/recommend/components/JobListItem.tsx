import React from 'react';
import Image from 'next/image';
import { AssetSvg } from '@/assets/AssetSvg';
import { removeBrackets } from '@/lib/utils';
import { FaRobot } from 'react-icons/fa6';
import { Icon } from 'lucide-react';

const JobListItem = ({
  data,
  isSelected,
}: {
  data: {
    job_title: string;
    job_url: string;
    company_name: string;
    company_url: string;
    company_img_url: string;
    location: string | null;
    post_date: Date;
    due_date: Date | null;
    fields: string;
    salary: string | null;
    experience: string | null;
    position: string;
    benefits: string;
    job_description: string;
    requirements: string;
  };
  isSelected: boolean;
}) => {
  //Format strings
  const location = data.location ? removeBrackets(data.location) : '';
  return (
    <div
      className={`w-full h-fit rounded-md p-3 flex flex-row items-center justify-around  border-3 ${
        isSelected ? 'border-primary' : 'hover:border-primary-300'
      }  text-black bg-white shadow-sm  `}
    >
      <Image
        className="w-[10%]"
        src={
          data.company_img_url
            ? data.company_img_url
            : `https://images.vietnamworks.com/img/company-default-logo.svg`
        }
        width={40}
        height={40}
        alt="Company logo"
      ></Image>
      <div className="w-[80%] h-full flex flex-col gap-2">
        <p className="font-bold text-md">{data.job_title}</p>
        <p className="text-sm">{data.company_name}</p>

        <div className="w-full h-fit flex flex-row gap-2 mt-1 justify-between text-xs text-primary">
          <div className="h-8 w-fit flex flex-row items-center justify-center gap-2">
            <div className="flex-shrink-0">{AssetSvg.location()}</div>
            <p>{location}</p>
          </div>
          <div className="h-8 w-fit flex flex-row items-center justify-center gap-2">
            {AssetSvg.money()}
            <p className="min-w-[16ch]">{data.salary}</p>
          </div>
        </div>
      </div>
      {isSelected && (
        <div className="absolute bottom-0 right-0 rounded-full border-2 border-primary p-2 mb-3 mr-3 text-primary">
          {<FaRobot />}
        </div>
      )}
    </div>
  );
};

export default JobListItem;
