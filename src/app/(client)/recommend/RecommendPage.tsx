'use client';
import React, { useEffect, useState } from 'react';
import { Spinner } from '@nextui-org/react';
import { FileDialog } from '@/components/FileDialog';
import { useUser } from '@/hooks/useUser';
import { useQuery } from '@tanstack/react-query';
import { useJob } from '@/hooks/useJob';
import DialogCustom from '@/components/ui/dialogCustom';
import CvUploader from './components/CvUploader';
import { toast } from 'react-toastify';
import JobList from './components/JobList';
import Chat from './components/Chat';
import SkeletonLoader from './components/SkeletonLoader';

const RecommendPage = () => {
  //Loading state for fetching data
  const [loading, setLoading] = useState(true);

  //Pagination params
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(5);
  const [totalPage, setTotalPage] = useState<number | null>(null);
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
      //Set selected job as first job in the list
      setSelectedJob(jobData.data[0]);
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
  const [hoveredJob, setHoveredJob] = useState(null);
  const [selectedJob, setSelectedJob] = useState(null);
  console.log('🚀 ~ RecommendPage ~ selectedJob:', selectedJob);

  //CV state
  const [cvFile, setCvFile] = useState([]);
  const [uploadedcvLink, setUploadedCvLink] = useState(''); //uploaded cv file link
  const [uploadedcvName, setUploadedCvName] = useState(''); //uploaded cv file name
  const [uploadedcvSize, setUploadedCvSize] = useState(''); //uploaded cv file size
  const [uploadedcvAt, setUploadedCvAt] = useState<number>(
    new Date().getMilliseconds()
  ); //uploaded cv file at [date]
  //useUser hook
  const { onGetCv, onPostCv } = useUser();
  const getUploadedcvFile = async () => {
    await onGetCv((response) => {
      if (response.status != 404) {
        setUploadedCvLink(response.file_url);
        setUploadedCvName(response.file_name);
        setUploadedCvSize(response.file_size);
        setUploadedCvAt(response.uploaded_at);
      }
      console.log('🚀 ~ getUploadedcvFile ~ response:', response);
      setLoading(false);
    });
  };
  useEffect(() => {
    getUploadedcvFile();
  }, []);
  //CV modal state
  const [open, setOpen] = useState(false);
  const [uploading, setUploading] = useState(false);
  //Message for uploading cv loader
  const messages = [
    'Uploading your CV...',
    'Processing your CV...',
    'Finding the most suitable jobs...',
  ];
  const [currentMessageIndex, setCurrentMessageIndex] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentMessageIndex((prevIndex) => (prevIndex + 1) % messages.length);
    }, 4000); // Change text every 4 seconds

    return () => clearInterval(timer); // Clean up timer on component unmount
  }, []);

  useEffect(() => {
    if (!uploading) {
      setCurrentMessageIndex(0); // Reset index when upload completes
    }
  }, [uploading]);

  const onUploadingCv = async () => {
    if (cvFile.length > 0) {
      console.log('uploading', cvFile[0]);
      const formData = new FormData();
      formData.append('file', cvFile[0]);

      try {
        setUploading(true);
        const response = await onPostCv(formData, (response) => {
          toast.success('CV uploaded successfully');
          console.log(response.data);
          //Get url of uploaded cv file
          getUploadedcvFile();
          setUploading(false);
        });

        console.log(response.data);
      } catch (error) {
        console.error(error);
      }
    }
  };
  useEffect(() => {
    refetch();
  }, [uploading]);

  //Job description modal state
  const [showJobDescriptionModal, setShowJobDescriptionModal] = useState(false);
  return (
    <div className="w-full h-full flex flex-col justify-center items-center gap-4">
      {loading ? (
        <DialogCustom
          className="w-[90%] lg:w-[50%] h-fit items-center justify-center"
          isModalOpen={loading}
          notShowClose={true}
        >
          <div className="flex flex-col gap-3 items-center justify-center">
            <Spinner
              className="w-full h-full flex justify-center items-center"
              color="primary"
              labelColor="primary"
            />
            <div className="text-center font-semibold text-xs sm:text-sm text-black">
              Getting data...
            </div>
          </div>
        </DialogCustom>
      ) : uploading ? (
        <DialogCustom
          className="w-[90%] lg:w-[50%] h-fit items-center justify-center"
          isModalOpen={uploading}
          notShowClose={true}
        >
          <div className="flex flex-col gap-3 items-center justify-center">
            <Spinner
              className="w-full h-full flex justify-center items-center"
              color="primary"
              labelColor="primary"
            />
            <div className="text-center font-semibold text-xs sm:text-sm text-black">
              {messages[currentMessageIndex]}
            </div>
          </div>
        </DialogCustom>
      ) : (
        <div className="w-full h-full flex flex-col justify-center items-center">
          <CvUploader
            uploadedcvLink={uploadedcvLink}
            uploadedcvName={uploadedcvName}
            uploadedcvSize={uploadedcvSize}
            uploadedcvAt={uploadedcvAt}
            onUploadingCv={onUploadingCv}
            cvFile={cvFile}
            setOpen={setOpen}
          />
          {(uploadedcvLink && !jobData) || isFetching ? (
            <SkeletonLoader />
          ) : uploadedcvLink && jobData ? (
            <div className="w-full h-fit p-8 flex flex-row gap-3 bg-secondary z-0">
              <div className="w-[50%]">
                <JobList
                  jobData={jobData}
                  filterOptions={filterOptions}
                  setFilter={setFilter}
                  showJobDescriptionModal={showJobDescriptionModal}
                  selectedJob={selectedJob}
                  setShowJobDescriptionModal={setShowJobDescriptionModal}
                  hoveredJob={hoveredJob}
                  setHoveredJob={setHoveredJob}
                  setSelectedJob={setSelectedJob}
                  totalPage={totalPage}
                  currentPage={currentPage}
                  onPageChange={onPageChange}
                ></JobList>
              </div>
              <div className="w-[50%]">
                <Chat selectedJob={selectedJob} />
              </div>
            </div>
          ) : null}

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
        </div>
      )}
    </div>
  );
};

export default RecommendPage;
