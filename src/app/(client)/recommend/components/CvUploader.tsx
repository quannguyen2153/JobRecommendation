import { AssetSvg } from '@/assets/AssetSvg';
import { Button } from '@nextui-org/react';
import React from 'react';
import { FaLink } from 'react-icons/fa6';

const CvUploader = ({
  uploadedcvLink,
  uploadedcvName,
  uploadedcvSize,
  uploadedcvAt,
  cvFile,
  onUploadingCv,
  setOpen,
}: {
  uploadedcvLink: string;
  uploadedcvName: string;
  uploadedcvSize: string;
  uploadedcvAt: Date;
  cvFile: File[];
  onUploadingCv: () => void;
  setOpen: (value: boolean) => void;
}) => {
  return (
    <div
      className={`w-full h-full flex flex-col justify-center items-center pt-8 gap-4  ${
        uploadedcvLink ? 'bg-bg-1 bg-contain bg-no-repeat bg-left-bottom' : ''
      }`}
    >
      {!uploadedcvLink ? (
        <div className="w-full h-full flex flex-col justify-center items-center gap-5 mt-8">
          <p className="text-[#858585]">
            Upload your CV to find the best jobs for you
          </p>
          {cvFile.length > 0 ? (
            <div className="w-full h-fit flex flex-col justify-center items-center gap-4">
              <Button
                color="primary"
                onClick={() => window.open(cvFile[0]?.preview, '_blank')}
              >
                Your CV Link
              </Button>
              <div className="w-full h-fit flex flex-row justify-center items-center gap-4">
                <Button
                  className="border-orange w-32 m-4"
                  variant="bordered"
                  radius="sm"
                  onClick={() => {
                    setOpen(true);
                  }}
                >
                  Modify
                </Button>
                <Button
                  className="bg-orange border-orange w-32 m-4"
                  variant="bordered"
                  radius="sm"
                  onClick={onUploadingCv}
                >
                  Save
                </Button>
              </div>
            </div>
          ) : (
            <div className="w-full h-full flex justify-center items-center gap-4">
              <Button
                radius="sm"
                color="primary"
                size="lg"
                aria-label="Upload your CV"
                className="w-[35%] md:w-[25%] lg:w-[20%] xl:w-[15%] text-sm lg:text-large"
                startContent={AssetSvg.upload()}
                onClick={async () => {
                  setOpen(true);
                }}
              >
                Upload your CV
              </Button>
            </div>
          )}
        </div>
      ) : (
        <>
          <div className="w-full h-fit flex flex-col justify-center items-center gap-5 mt-8">
            <p className="text-[#858585]">
              Thanks for uploading your CV. You can modify it at anytime!
            </p>
            <Button
              color="primary"
              startContent={<FaLink />}
              onClick={() => window.open(uploadedcvLink, '_blank')}
            >
              {uploadedcvName} ( {uploadedcvSize} )
            </Button>
            <p className="text-[#858585]">
              Last modified: {new Date(uploadedcvAt).toUTCString()}{' '}
            </p>
            <div className="w-full h-fit flex flex-row justify-center items-center gap-4">
              <Button
                className="border-orange w-32 m-4"
                variant="bordered"
                radius="sm"
                onClick={() => {
                  setOpen(true);
                }}
              >
                Modify
              </Button>
              <Button
                className="bg-orange border-orange w-32 m-4"
                variant="bordered"
                radius="sm"
                onClick={onUploadingCv}
              >
                Save
              </Button>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default CvUploader;
