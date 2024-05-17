'use client';
import React, { useEffect, useState } from 'react';
import Filter from './Filter';
import {
  Button,
  Input,
  Link,
  Pagination,
  Select,
  SelectItem,
} from '@nextui-org/react';
import { AssetSvg } from '@/assets/AssetSvg';
import JobListItem from './JobListItem';
import JobDescriptionCard from './JobDescriptionCard';
import { FileDialog } from '@/components/FileDialog';
import ChatInput from './ChatInput';
import ChatHeader from './ChatHeader';
import ChatMessages from './ChatMessages';
import { useUser } from '@/hooks/useUser';
import { useQuery } from '@tanstack/react-query';
import { useJob } from '@/hooks/useJob';
import { Loader } from 'lucide-react';
import { FaLink } from 'react-icons/fa6';

const RecommendPage = () => {
  //Pagination params
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);
  const [totalPage, setTotalPage] = useState(null);

  const { onGetJobs } = useJob();

  // Define a query key and fetch function for fetching job list data
  const fetchJobListKey = ['job list page ' + currentPage];
  const fetchJobListFunction = async () => {
    const fetchJobListData = await onGetJobs(currentPage);
    return fetchJobListData;
  };

  // Fetch review data
  const {
    data: jobData,
    isFetched,
    isFetching,
    refetch,
  } = useQuery({ queryKey: fetchJobListKey, queryFn: fetchJobListFunction });

  //Set total page when data is fetched
  useEffect(() => {
    if (jobData) {
      console.log('🚀 ~ useEffect ~ jobData:', jobData);
      setTotalPage(Math.round(jobData.total / itemsPerPage));
    }
  }, [jobData]);

  //Page change when click on pagination
  const onPageChange = (page) => {
    setCurrentPage(page);
  };

  //Set state of fitlers
  const [filter, setFilter] = useState(new Set([]));
  const filterOptions = [
    { id: 1, option: 'Newest' },
    { id: 2, option: 'Oldest' },
  ];

  //Selected job description data
  const [selectedJob, setSelectedJob] = useState(null);

  //CV state
  const [cvFile, setCvFile] = useState([]);
  const [uploadedcvLink, setUploadedCvLink] = useState(undefined); //uploaded cv file link
  //useUser hook
  const { onGetCv, onPostCv } = useUser();

  const uploadedcvFileFunc = async () => {
    await onGetCv((response) => {
      setUploadedCvLink(response.data.data.download_url);
    });
  };

  useEffect(() => {
    uploadedcvFileFunc();
  }, []);

  //CV modal state
  const [open, setOpen] = useState(false);

  const onUploadingCv = async () => {
    if (cvFile.length > 0) {
      console.log('uploading', cvFile[0]);
      const formData = new FormData();
      formData.append('file', cvFile[0]);

      try {
        const response = await onPostCv(formData, (response) => {
          console.log(response.data);
          //Get url of uploaded cv file
          uploadedcvFileFunc();
        });

        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  };

  //Job description modal state
  const [showJobDescriptionModal, setShowJobDescriptionModal] = useState(false);

  return (
    <div className="w-full h-full flex flex-col justify-center items-center gap-4">
      {!uploadedcvLink ? (
        <div className="w-full h-fit flex flex-col justify-center items-center pt-8 gap-4">
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
                  className={`
             border-orange w-32 m-4`}
                  variant="bordered"
                  radius="sm"
                  onClick={() => {
                    setOpen(true);
                  }}
                >
                  Modify
                </Button>
                <Button
                  className={`
                  bg-orange
             border-orange w-32 m-4`}
                  variant="bordered"
                  radius="sm"
                  onClick={onUploadingCv}
                >
                  Save
                </Button>
              </div>
            </div>
          ) : (
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
          )}
        </div>
      ) : (
        <div className="w-full h-fit flex flex-col items-center justify-center gap-4">
          <div className="w-full h-fit flex flex-col justify-center items-center gap-5 mt-8">
            <p className="text-[#858585]">
              Thanks for uploading your CV. You can modify it anytime
            </p>
            <Button
              color="primary"
              startContent={<FaLink />}
              onClick={() => window.open(uploadedcvLink, '_blank')}
            >
              Your CV Link
            </Button>
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
                Modify
              </Button>
              <Button
                className={`
                  bg-orange
             border-orange w-32 m-4`}
                variant="bordered"
                radius="sm"
                onClick={onUploadingCv}
              >
                Save
              </Button>
            </div>
          </div>
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

      {jobData ? (
        <div className="w-full h-fit flex flex-row gap-3 bg-secondary mt-8 z-0">
          <div className="w-[50%] h-full mx-8 my-16 flex flex-col z-10">
            <div className="w-full h-fit flex flex-row justify-between items-center">
              <p className="font-bold text-lg text-black">
                {jobData?.total} Jobs
              </p>
              <Select
                className="w-fit"
                style={{ width: '15rem', zIndex: 0 }}
                key={'type'}
                radius={'md'}
                size="lg"
                color="primary"
                autoFocus={false}
                startContent={AssetSvg.filter()}
                placeholder={'Filter by'}
                onSelectionChange={setFilter}
                aria-label="Filter"
              >
                {filterOptions?.map((c) => (
                  <SelectItem
                    key={c.id}
                    value={c.option}
                    className="text-black"
                    onMouseEnter={() => {}}
                  >
                    {c.option}
                  </SelectItem>
                ))}
              </Select>
            </div>
            <div className="w-full flex flex-col justify-center items-center">
              {' '}
              {/* {isFetching ? (
              <Spinner
                className=""
                label="Đang tải..."
                color="warning"
                labelColor="warning"
              />
            ) : ( */}
              {
                <div className="w-full h-fit z-0">
                  {Array.isArray(jobData?.data) &&
                    jobData?.data.map((item) => (
                      <div
                        key={item.job_url}
                        className={`w-full h-fit flex flex-row items-center justify-between my-2 relative ${
                          showJobDescriptionModal &&
                          selectedJob?.job_url === item.job_url
                            ? 'z-20'
                            : 'z-0'
                        }`}
                        // onClick={() => onJobClick(item)}
                        onMouseEnter={() => {
                          setShowJobDescriptionModal(true);
                          setSelectedJob(item);
                        }}
                        onMouseLeave={() => {
                          setShowJobDescriptionModal(false);
                        }}
                      >
                        <JobListItem
                          data={item}
                          isSelected={selectedJob?.job_url === item.job_url}
                        />{' '}
                        {showJobDescriptionModal &&
                          selectedJob?.job_url === item.job_url && (
                            <div className="z-10 absolute -top-16 right-0 w-1/5">
                              <JobDescriptionCard data={item} />
                            </div>
                          )}
                      </div>
                    ))}
                </div>
              }
              <Pagination
                color="primary"
                showControls
                total={totalPage!}
                initialPage={1}
                onChange={(page) => {
                  onPageChange(page);
                }}
                page={currentPage}
              />
            </div>
          </div>

          <div className="z-0 w-[50%] h-[600px] mx-8 my-16 flex flex-col rounded-lg bg-white">
            <div className="h-[80%] w-full flex flex-col ">
              <ChatHeader></ChatHeader>
              <ChatMessages></ChatMessages>
            </div>

            <ChatInput className="w-full h-[15%] p-3 z-0"></ChatInput>
          </div>

          {/* <div className="w-[50%] h-full mx-8 my-16">
          <JobDescriptionCard data={selectedJob}></JobDescriptionCard>
        </div> */}
        </div>
      ) : (
        <Loader />
      )}
    </div>
  );
};

export default RecommendPage;
