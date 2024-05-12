'use client';
import { AssetSvg } from '@/assets/AssetSvg';
import FileCard from '@/components/FileCard/FileCard';
import { FileDialog } from '@/components/FileDialog';
import { Button } from '@nextui-org/react';
import React, { useEffect, useLayoutEffect, useState } from 'react';
import Rating from './Rating';
import ChatbotPopup from '../recommend/ChatbotPopup';

const sampleRatingData = {
  rating: 65.3,
  criteria1: 80,
  criteria2: 60,
  criteria3: 70,
};

const page = () => {
  //CV state
  const [cvFile, setCvFile] = useState([]);
  const [lastModifiedTime, setLastModifiedTime] = useState<Date>();

  useEffect(() => {
    if (cvFile.length > 0) {
      const file = cvFile[0];
      setLastModifiedTime(new Date());
    }
  }, [cvFile]);

  //Dialog state
  const [open, setOpen] = useState(false);

  const [chatOpen, setChatOpen] = useState(false);
  return (
    <div className="w-full h-full flex flex-col justify-center items-center gap-4">
      {cvFile.length == 0 ? (
        <div className="w-full h-fit flex flex-col justify-center items-center pt-8 gap-4">
          <p className="text-[#858585]">
            Upload your CV to find the best jobs for you
          </p>

          <Button
            radius="sm"
            color="primary"
            size="lg"
            aria-label="Upload your CV"
            className="w-[35%] md:w-[25%] lg:w-[20%] xl:w-[15%] text-sm lg:text-large"
            startContent={AssetSvg.upload()}
            onClick={() => setOpen(true)}
          >
            Upload your CV
          </Button>
        </div>
      ) : (
        <div className="w-full h-fit flex flex-col items-center justify-center gap-4">
          {cvFile.length > 0 ? (
            <div className="w-full h-fit flex flex-col justify-center items-center gap-5">
              <FileCard
                key={'cv'}
                files={cvFile}
                setFiles={setCvFile}
                file={cvFile[0]}
              />
              <div className="w-full h-fit flex flex-row mt-3 text-black justify-center items-center gap-8 font-bold">
                <span>Chỉnh sửa lần cuối</span>
                <span>{lastModifiedTime?.toLocaleString()}</span>
              </div>
              <div className="w-full h-fit flex flex-row justify-center items-center gap-4">
                <Button
                  className={`
             border-orange w-32 m-4`}
                  variant="bordered"
                  radius="sm"
                  onClick={() => {
                    setOpen(true);
                  }}
                >
                  Chỉnh sửa
                </Button>
                {/* <Button
                className={`
                  bg-orange text-white
             border-orange w-32 m-4`}
                variant="bordered"
                radius="sm"
                onClick={onSubmit}
              >
                Lưu
              </Button> */}
              </div>
            </div>
          ) : null}
        </div>
      )}

      <div className="flex h-0 w-0 flex-col gap-y-4 justify-center overflow-hidden">
        <div className="flex flex-row gap-x-4 items-center font-bold ">
          <FileDialog
            className="text-black"
            name="Images"
            maxFiles={1}
            maxSize={1024 * 1024 * 4}
            files={cvFile}
            setFiles={setCvFile as any}
            disabled={false}
            open={open}
            onOpenChange={() => setOpen(false)}
          />
        </div>
      </div>

      <div className="w-full h-fit flex items-center justify-center">
        <Rating data={sampleRatingData}></Rating>
      </div>

      <div className="w-[25%] h-fit flex flex-row fixed bottom-0 right-0 mr-4">
        <div className={` ${chatOpen ? 'animate-in duration-200' : 'hidden'}`}>
          <ChatbotPopup />
        </div>
        <Button
          isIconOnly
          color="primary"
          aria-label="Like"
          radius="full"
          size="lg"
          onClick={() => setChatOpen(!chatOpen)}
          className="mr-4 mb-10"
        >
          {AssetSvg.chat()}
        </Button>
      </div>
    </div>
  );
};

export default page;
