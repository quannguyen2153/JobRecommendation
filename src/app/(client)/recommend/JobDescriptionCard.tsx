import React from 'react';
import Image from 'next/image';
import { Button, ScrollShadow } from '@nextui-org/react';
import { AssetSvg } from '@/assets/AssetSvg';
import { calculateDueTime } from '@/lib/utils';

const JobDescriptionCard = ({
  data,
}: {
  data: {
    job_title: string;
    job_url: string;
    company_name: string;
    company_url: string;
    location: string;
    post_date: Date;
    due_date: Date | null;
    fields: string;
    salary: string | null;
    experience: string | null;
    position: string;
    benefits: string[];
    job_description: string;
    requirements: string;
  };
}) => {
  return (
    <ScrollShadow
      hideScrollBar
      className="w-[660px] z-0 h-[450px] border-3 rounded-md flex flex-col gap-3 bg-white shadow-md text-black p-3"
    >
      <div className="flex flex-row gap-5 items-center">
        <Image
          className="w-[8%]"
          src="https://images.vietnamworks.com/img/company-default-logo.svg"
          width={40}
          height={40}
          alt="Company logo"
        ></Image>

        <div className="w-[70%] h-fit flex flex-col gap-1">
          <p className="font-bold text-md">{data.job_title}</p>
          <p className="text-sm">{data.company_name}</p>
          <div className="w-fit h-fit flex flex-row items-center justify-center gap-2 text-xs text-primary">
            <div className="flex-shrink-0">{AssetSvg.location()}</div>
            <p className="min-w-[10ch]">{data.location}</p>
          </div>
          <div className="w-full h-fit flex flex-row gap-2 mt-1 justify-between text-xs text-primary">
            <div className="w-fit flex flex-row items-center justify-center gap-2">
              <div className="flex-shrink-0">{AssetSvg.human()}</div>
              <p className="min-w-[10ch]">{data.position}</p>
            </div>

            <div className="w-fit flex flex-row items-center justify-center gap-2">
              <div className="flex-shrink-0">{AssetSvg.money()}</div>
              <p className="min-w-[10ch]">{data.salary}</p>
            </div>

            <div className="w-fit flex flex-row justify-between gap-1">
              <div className="flex-shrink-0">{AssetSvg.calendar()}</div>
              <p className="min-w-[10ch]">{calculateDueTime(data.due_date!)}</p>
            </div>
          </div>
        </div>
        <Button
          radius="sm"
          color="primary"
          size="md"
          aria-label="Apply now"
          className="text-sm lg:text-md"
          endContent={AssetSvg.forward()}
          onClick={() => window.open(data.job_url, '_blank')}
        >
          Apply now
        </Button>
      </div>

      <div className="w-fit h-fit">
        <div className="w-full flex flex-col gap-3">
          <div className="w-full h-fit flex flex-col gap-2">
            <p className="font-bold">Fields</p>
            <p>{data.fields}</p>
          </div>
          <div className="w-full h-fit flex flex-col gap-2">
            <p className="font-bold">Job Descriptions</p>
            <p>{data.job_description}</p>
          </div>
          <div className="w-full h-fit flex flex-col gap-2">
            <p className="font-bold">Requirements</p>
            <p>{data.requirements}</p>
          </div>

          <div className="w-full h-fit flex flex-col gap-2">
            <p className="font-bold">Salary</p>
            <p>{data.salary}</p>
          </div>
          <div className="w-full h-fit flex flex-col gap-2">
            <p className="font-bold">Benefits</p>
            <p>{data.benefits}</p>
          </div>
        </div>
      </div>
    </ScrollShadow>
  );
};

export default JobDescriptionCard;